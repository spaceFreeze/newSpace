import datetime
import decimal
import json

import pandas as pd
import sqlalchemy.exc
from flask import Blueprint
from sqlalchemy import or_
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
    hashtag = str("#") + hashtag
    # 특정 해시태그를 포함하고 있는지 확인
    conds = [News.hash1 == hashtag, News.hash2 == hashtag, News.hash3 == hashtag, News.hash4 == hashtag]
    if section == "all" and name == "all":  # 모든 쿼리 - 메인화면에서 해시태그 눌렀을 때
        news_list = News.query.filter(or_(*conds))\
            .order_by(News.recom_react_cnt.desc())
    elif section != "all":  # 특정 section
        news_list = News.query.filter(News.section == section) \
            .filter(or_(*conds))\
            .order_by(News.recom_react_cnt.desc())
    else:  # 특정 회사
        news_list = News.query.filter(News.name == name) \
            .filter(or_(*conds))\
            .order_by(News.recom_react_cnt.desc())
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
            df1.columns = ['text']
            df2.columns = ['text']
            df3.columns = ['text']
            df4.columns = ['text']
            df = pd.concat([df1, df2, df3, df4])

            c_df = df['text'].value_counts()  # 키워드별 카운트
            res = c_df.reset_index()
            res.columns = ['text', 'size']
            res = res.reindex(columns=['size', 'text'])
            # h_li = c_df.index.tolist()
            # [ "#울트라", "#삼성전자", "#시장", ..., "#출시" ]
            h_li = res.to_dict('records')

        return h_li[:15]
        # return json.dumps(h_li[:15], default=alchemyencoder, ensure_ascii=False, indent=4)


# 기존 url에 새롭게 추가하고 싶을 때 @bp.route를 추가하면 됨
bp = Blueprint('hash_tag', __name__, url_prefix='/hash')


# 해시태그 및 가중치 데이터
# 최초로 한 번만 실행해주기! (일단 테스트용으로 csv 읽어와서 DB에 저장함)
# 추후에 자동으로 추가하는 코드와 연결해야됨!
# http://127.0.0.1:5000/hash/first
@bp.route('/first')
def hash_db():
    try:
        new_df = pd.read_csv("[2022.02.16]All_hashtag.csv")
        # 기존 db에 반복되는 내용이 있는지 체크한 후 DB에 추가
        # query -> dataframe
        n_li = []
        hash_list = Hash.query.all()
        for hashs in hash_list:
            n_li.append(dict(hashs.serialize))
        original_data = pd.DataFrame.from_records(n_li)
        # print(new_df.iloc[0][0])
        # print(new_df.iloc[0][1])

        for i in range(len(new_df)):
            if not original_data.empty:  # 기존 DB에 내용이 있고
                # 기존 DB와 내용이 겹친다면 데이터 추가 불허용
                if new_df.iloc[i][1] in original_data['hashtag'].unique():
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


# # http://127.0.0.1:5000/hash/test/IT/all
# @bp.route('/test/<section>/<name>')
# def test(section, name):
#     h_li = []
#     if section == "all" and name == "all":  # 모든 쿼리 - 메인화면에서의 금주의 키워드
#         hash_list = Hash.query.order_by(Hash.weight.desc())
#         for hashs in hash_list:
#             h_li.append(dict(hashs.serialize))
#
#     else:
#         if section != "all":  # 특정 section
#             news_list = News.query.filter(News.section == section)
#         else:  # 특정 회사
#             news_list = News.query.filter(News.name == name)
#         n_li = []
#         for news in news_list:  # 해시태그 열만 가져옴
#             n_li.append(dict(news.hash_count))
#
#         # hash1~4 열 데이터 합치고 키워드 별 value_count
#         o_df = pd.DataFrame.from_records(n_li)
#         df1 = pd.DataFrame(o_df.iloc[:, 0])
#         df2 = pd.DataFrame(o_df.iloc[:, 1])
#         df3 = pd.DataFrame(o_df.iloc[:, 2])
#         df4 = pd.DataFrame(o_df.iloc[:, 3])
#         df1.columns = ['text']
#         df2.columns = ['text']
#         df3.columns = ['text']
#         df4.columns = ['text']
#         df = pd.concat([df1, df2, df3, df4])
#
#         c_df = df['text'].value_counts()    # 키워드 별 카운트
#         res = c_df.reset_index()
#         res.columns = ['text', 'size']
#         res = res.reindex(columns=['size', 'text'])
#         # h_li = c_df.index.tolist()
#         h_li = res.to_dict('records')
#
#     return json.dumps(h_li[:15], default=alchemyencoder, ensure_ascii=False, indent=4)
#     # return pd.Series.to_json(c_df, force_ascii=False)
#     # {"#울트라":2,"#삼성전자":2,"#시장":2, ..., "#가격":1,"#포크":1,"#출시":1}


# # 키워드(해시태그) 클릭 시 보이는 기사들
# # 회사 / 섹션 별로 나누고 추천반응수 순으로 보여주기
# # http://127.0.0.1:5000/all/삼성전자/해시태그/1
# @bp.route('/<section>/<name>/<hashtag>/<int:pagenum>')
# def test(section, name, hashtag, pagenum):
#     ex_li_1 = li1_hash(section=section, name=name, hashtag=hashtag)
#     li_1 = page_show(ex_li_1, pagenum)
#     return res_json(li_1)


##############################################################################
# # DB에서 해당 컬럼 값 기준으로 row 읽어오고 json으로 뿌리기
# def search_(col_, col_obj):
#     n_li = []
#     news_list = News.query.filter(col_ == col_obj).all()
#     for news in news_list:
#         n_li.append(dict(news.serialize))
#
#     res = json.dumps(n_li, default=alchemyencoder, ensure_ascii=False, indent=4)
#     return res
#
#
# # 회사명에 따른 레코드 검색
# # http://127.0.0.1:5000/cor/name/퀄컴
# @bp.route('/name/<name>')
# def name_search(name):
#     return search_(News.types, name)
#
#
# # 섹션에 따른 레코드 검색
# # http://127.0.0.1:5000/cor/section/IT
# @bp.route('/section/<section>')
# def section_search(section):
#     return search_(News.section, section)


##############################################################################
    # n_li = []
    # news_list = News.query.filter(News.name == types).all()
    # for news in news_list:
    #     n_li.append(dict(news.serialize))
    #
    # res = json.dumps(n_li, default=alchemyencoder, ensure_ascii=False, indent=4)
    # return res
