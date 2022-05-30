import datetime
import decimal
import pandas as pd
import sqlalchemy.exc
from flask import Blueprint
from sqlalchemy import or_, func
from hynix import db
from hynix.models import News, Hash


def alchemyencoder(obj):
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)


def add_new(new_df, i):
    new_event = Hash(new_df.iloc[i][0], float(new_df.iloc[i][1]))
    db.session.add(new_event)
    print("새로운 데이터 추가!")


# 해시태그 클릭 시 보이는 기사들(json) list1 return
def li1_hash(section, name, hashtag):
    n_li = []
    # 특정 해시태그 포함 여부 확인
    conds = [News.hash1 == hashtag, News.hash2 == hashtag, News.hash3 == hashtag, News.hash4 == hashtag]
    if section == "all" and name == "all":  # 모든 쿼리 - 메인화면에서 해시태그 눌렀을 때
        news_list = News.query.filter(or_(*conds))\
            .order_by(func.substr(News.date, -10, 10).asc())
    elif section != "all":  # 특정 section
        news_list = News.query.filter(News.section == section) \
            .filter(or_(*conds))\
            .order_by(func.substr(News.date, -10, 10).asc())
    else:  # 특정 회사
        news_list = News.query.filter(News.name == name) \
            .filter(or_(*conds))\
            .order_by(func.substr(News.date, -10, 10).asc())
    for news in news_list:
        n_li.append(dict(news.signify))     # list1만 return
    return n_li


# list2(금주의 키워드) return
def li2_hash(section="all", name="all", count=0):
    h_li = []
    if count == 0:
        return "nothing!"
    else:
        # 모든 쿼리 - 메인화면에서의 금주의 키워드
        if section == "all" and name == "all":
            hash_list = Hash.query.order_by(Hash.weight.desc())
            for hashs in hash_list:
                h_li.append(dict(hashs.serialize))

        # 특정 섹션 / 기업에서의 금주의 키워드
        else:
            if section != "all":  # 특정 섹션
                news_list = News.query.filter(News.section == section)
            else:  # 특정 기업
                news_list = News.query.filter(News.name == name)
            n_li = []
            for news in news_list:  # 해시태그 열만 가져옴
                n_li.append(dict(news.hash_count))

            # hash1~4 열 데이터 합치고
            o_df = pd.DataFrame.from_records(n_li)
            df1 = pd.DataFrame(o_df.iloc[:, 0])
            df2 = pd.DataFrame(o_df.iloc[:, 1])
            df3 = pd.DataFrame(o_df.iloc[:, 2])
            df4 = pd.DataFrame(o_df.iloc[:, 3])
            df1.columns = ['hashtag']
            df2.columns = ['hashtag']
            df3.columns = ['hashtag']
            df4.columns = ['hashtag']
            df = pd.concat([df1, df2, df3, df4])

            c_df = df['hashtag'].value_counts()  # 키워드별 카운트
            res = c_df.reset_index()
            res.columns = ['hashtag', 'weight']
            res = res.reindex(columns=['weight', 'hashtag'])
            # h_li = c_df.index.tolist()
            # [ "#울트라", "#삼성전자", "#시장", ..., "#출시" ]
            h_li = res.to_dict('records')

        return h_li[:15]


# 기존 url에 새롭게 추가하고 싶을 때 @bp.route를 추가하면 됨
bp = Blueprint('hash_tag', __name__, url_prefix='/hash')


# 해시태그 및 가중치 데이터
# http://127.0.0.1:5000/hash/first
@bp.route('/first')
def hash_db():
    try:
        new_df = pd.read_csv("[2022.03.11_2022.03.17]All_hashtag.csv", encoding='utf-8-sig')
        # 기존 db에 반복되는 내용이 있는지 체크한 후 DB에 추가
        # query -> dataframe
        n_li = []
        hash_list = Hash.query.all()
        for hashs in hash_list:
            n_li.append(dict(hashs.serialize))
        original_data = pd.DataFrame.from_records(n_li)

        for i in range(len(new_df)):
            if not original_data.empty:  # 기존 DB에 내용이 있고
                # 기존 DB와 내용이 겹친다면 데이터 추가 불허용
                if new_df.iloc[i][0] in original_data['hashtag'].unique():
                    print("중복!")
                else:  # 중복되는 내용이 없으면 데이터 추가 허용
                    add_new(new_df, i)
            else:  # 기존 DB가 비어있으면 데이터 추가 허용
                add_new(new_df, i)
        db.session.commit()

        # 현재 쌓인 query 개수
        q = Hash.query.count()
        return f'count : {q}'
    except sqlalchemy.exc.SQLAlchemyError as e:
        return f'error! {e}'