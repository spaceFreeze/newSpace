import datetime
import decimal
import json

import pandas as pd
import sqlalchemy.exc
from flask import Blueprint

from hynix import db
from hynix.models import News
from hynix.views.hash_views import li1_hash, li2_hash

from datetime import datetime, timedelta


def alchemyencoder(obj):
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)


# 데이터프레임 -> DB에 저장
def add_new(new_df, i):
    new_event = News(new_df.iloc[i][0], new_df.iloc[i][1], new_df.iloc[i][2],
                     new_df.iloc[i][3], new_df.iloc[i][4], new_df.iloc[i][5],
                     new_df.iloc[i][6], new_df.iloc[i][7], new_df.iloc[i][8],
                     new_df.iloc[i][9], int(new_df.iloc[i][10]), int(new_df.iloc[i][11]),
                     int(new_df.iloc[i][12]), new_df.iloc[i][13], new_df.iloc[i][14],
                     new_df.iloc[i][15], new_df.iloc[i][16], new_df.iloc[i][17], new_df.iloc[i][18])
    db.session.add(new_event)
    print("새로운 데이터 추가!")


# 기사제목으로 중복제거 & 추천반응수 순 리스트 return
def rm_dupli(section="all", name="all"):
    n_li = []
    if section == "all" and name == "all":  # 모든 쿼리 - 메인 화면
        news_list = News.query.order_by(News.recom_react_cnt.desc())
    elif section != "all":  # 특정 section
        news_list = News.query.filter(News.section == section).order_by(News.recom_react_cnt.desc())
    else:   # 특정 회사
        news_list = News.query.filter(News.name == name).order_by(News.recom_react_cnt.desc())
    for news in news_list:
        n_li.append(dict(news.serialize))

    origin_df = pd.DataFrame.from_records(n_li)
    origin_df = origin_df.drop_duplicates(['title'])    # 중복 제거 - 기사제목
    # print(len(origin_df))
    no_dup_li = origin_df.to_dict('records')
    return no_dup_li


# 페이지별로 8개씩 return
def page_show(no_dup_li, pagenum):
    fir = (pagenum - 1) * 8
    sec = (pagenum * 8)
    # return json.dumps(no_dup_li[fir:sec], default=alchemyencoder, ensure_ascii=False, indent=4)
    return no_dup_li[fir:sec]


# list2(금주의 키워드) 및 list3(오늘의 이슈) 만든 후
# 최종 json return
def res_json(li_1, section, name, pagenum, count):
    ex_li_3 = rm_dupli()
    li_3 = []
    for i in ex_li_3[:10]:  # 상위 10개만
        li_3.append({'url': i['url'], 'title': i['title'], 'recom_react_cnt': i['recom_react_cnt']})

    li_2 = li2_hash(section, name, count)

    # 최종 json
    res_dic = {
        'list1': {
            'total': count,     # 쿼리 수(/8 = 총 페이지 개수)
            "page": pagenum,    # 현재 페이지 넘버
            "list": li_1        # list1
        },
        'list2': li_2,
        'list3': li_3}

    # # json파일로 저장해보기
    # with open("C:\projects\sksk\_res.json", 'w') as f:
    #     json.dump(res_dic, f, default=alchemyencoder, ensure_ascii=False, indent=4)
    if pagenum <= (count/8 + 1):
        return json.dumps(res_dic, default=alchemyencoder, ensure_ascii=False, indent=4)
    else:
        return "page error!"


# 기존 url에 새롭게 추가하고 싶을 때 @bp.route를 추가하면 됨
bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/test')
def test():
    try:
        # now = datetime.now()
        # last = (now - timedelta(weeks=1)).strftime("%Y/%m/%d")  # 일주일 전 날짜
        # print(last)     # ex)2022/03/31

        # 일단 csv에 있는 날짜로 테스트
        today = "2022/03/16"
        last = "%{}%".format(today)
        print(last)
        
        ex_news = News.query.filter(News.date.like(last)).all()
        for o in ex_news:   # ex_news는 News 객체들 리스트
            db.session.delete(o)
        db.session.commit()
        print("쿼리 삭제!")
        return "쿼리 삭제 성공!"
    except sqlalchemy.exc.SQLAlchemyError as e:
        # db.session.rollback()
        return f'error! {e}'


# 최초로 한 번만 실행해주기! (일단 테스트용으로 csv 읽어와서 DB에 저장함)
# 데이터프레임 -> DB에 저장
# http://127.0.0.1:5000/first
@bp.route('/first')
def first_db():
    try:
        new_df = pd.read_csv("[2022.03.11]All_to_result.csv")
        # 기존 db에 반복되는 내용이 있는지 체크한 후 DB에 추가
        # query -> dataframe
        n_li = []
        news_list = News.query.all()
        for news in news_list:
            n_li.append(dict(news.serialize))
        original_data = pd.DataFrame.from_records(n_li)
        # print(original_data)
        # print(original_data.iloc[0][7])

        # print(new_df.iloc[0][0])
        # print(new_df.iloc[0][7])    # 회사종류
        # print(new_df.iloc[0][8])    # 좋아요 수

        for i in range(len(new_df)):
            if not original_data.empty:  # 기존 DB에 내용이 있고
                # 기존 DB와 내용(기사제목 & 회사명)이 겹친다면 데이터 추가 불허용
                if new_df.iloc[i][2] in original_data['title'].unique()\
                        and new_df.iloc[i][6] in original_data['name'].unique():
                    print("중복!")
                else:   # 중복되는 내용이 없으면 데이터 추가 허용
                    add_new(new_df, i)
            else:   # 기존 DB가 비어있으면 데이터 추가 허용
                add_new(new_df, i)

        # # 중복 생각하지 X 바로 DB에 추가
        # for i in range(len(new_df)):
        #     add_new(new_df, i)
        #     # print(new_df.iloc[i][10])
        # db.session.commit()
        db.session.commit()

        # 현재 쌓인 query 개수
        q = News.query.count()
        return f'count : {q}'
    except sqlalchemy.exc.SQLAlchemyError as e:
        return f'error! {e}'


# list1
# http://127.0.0.1:5000/all/all/1         # 메인화면
# http://127.0.0.1:5000/IT/all/1          # IT(특정 섹션)
# http://127.0.0.1:5000/all/삼성전자/1      # 삼성전자(특정 회사)
@bp.route('/<section>/<name>/<int:pagenum>')
def sec_com_search(section, name, pagenum):
    ex_li_1 = rm_dupli(section, name)
    count = len(ex_li_1)    # 메인/해당 섹션/기업별 쿼리 수
    if count == 0:  # 해당 내용이 아무것도 없을 때
        li_1 = "nothing!"
    else:
        li_1 = page_show(ex_li_1, pagenum)
    return res_json(li_1, section, name, pagenum, count)


# 키워드(해시태그) 클릭 시 보이는 내용
# list1 - 특정 키워드(해시태그)
# http://127.0.0.1:5000/hash/all/삼성전자/중국/1
# http://127.0.0.1:5000/hash/all/all/시장/1
@bp.route('/hash/<section>/<name>/<hashtag>/<int:pagenum>')
def hash_search(section, name, hashtag, pagenum):
    ex_li_1 = li1_hash(section, name, hashtag)
    count = len(ex_li_1)
    if count == 0:
        li_1 = "nothing!!"
    else:
        li_1 = page_show(ex_li_1, pagenum)

    res_dic = {
        'list1': {
            'total': count,
            "page": pagenum,
            "list": li_1
        }
    }
    return json.dumps(res_dic, default=alchemyencoder, ensure_ascii=False, indent=4)


##############################################################################
# list3
# 전체 섹션+회사에 대해 가장 추천반응수가 높은 기사 순 제목+반응수 -> 오늘의 이슈
# http://127.0.0.1:5000/all/today
# @bp.route('/all/today')
# def today_issue():
#     no_dup_li = rm_dupli()
#     n_li = []
#     for i in no_dup_li:
#         n_li.append({'url': i['url'], 'title': i['title'], 'recom_react_cnt': i['recom_react_cnt']})
#
#     return json.dumps(n_li, default=alchemyencoder, ensure_ascii=False, indent=2)

    # 추천반응수 순 특정 열로만 새로운 dict 출력
    # n_li = []
    # news_list = News.query.order_by(News.recom_react_cnt.desc())    # 추천반응수 순
    #
    # for i in news_list:
    #     # print(i.news_id)
    #     n_li.append({'url': i.url, 'title': i.title, 'recom_react_cnt': i.recom_react_cnt})
    #
    # return json.dumps(n_li, default=alchemyencoder, ensure_ascii=False, indent=2)

    # 모든 기사 추천반응수 순으로 page별 8개씩 보여주기(시도)
    # n_li = []
    # news_list = News.query.order_by(News.recom_react_cnt.desc())    # 추천반응수 순
    # for news in news_list:
    #     n_li.append(dict(news.serialize))
    # fir = (pagenum - 1) * 8
    # sec = (pagenum * 8)
    # return json.dumps(n_li[fir:sec], default=alchemyencoder, ensure_ascii=False, indent=4)


##############################################################################
# 기존 db에 반복되는 내용이 있는지 체크한 후 db에 추가
# query -> dataframe

# n_li = []
# news_list = News.query.all()
# for news in news_list:
#     n_li.append(dict(news.serialize))
# original_data = pd.DataFrame.from_records(n_li)
#
# for i in range(len(new_df)):
#     if not original_data.empty:  # 기존 DB에 내용이 있고
#         # 기존 DB와 내용이 겹친다면 데이터 추가 불허용
#         if new_df.iloc[i][1] in original_data['title'].unique():
#             print("중복!")
#         else:   # 중복되는 내용이 없으면 데이터 추가 허용
#             add_new(new_df, i)
#     else:   # 기존 DB가 비어있으면 데이터 추가 허용
#         add_new(new_df, i)


##############################################################################
    # # 쿼리 하나는 성공
    # news_list = News.query.order_by(News.recom_react_cnt.desc()).first().news_id
    # return str(news_list)

    # 실패
    # [ [ null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null ] ]
    # news_list = News.query.order_by(News.recom_react_cnt.desc())
    # x = [[r.as_dict for r in news_list.all()]]
    # return json.dumps(x, default=alchemyencoder, ensure_ascii=False, indent=4)

    # ----------------------------------------------------------
    # # 중복 제거
    # q = News.query.all()
    # df = pd.read_sql_query(q.statement, q.session.bind)
    # return jsonify(json.loads(df).to_json())

    # ================================================================
    # news_list = News.query.filter(News.title).distinct() # 빈 리스트가 나옴..
    # 출력은 되지만 제대로 중복 제거 X
    # news_list = News.query.distinct(News.section)
    # news_list = News.query.all().distinct(News.section)
    # news_list = News.query.from_statement(sqlalchemy.text(
    #     "SELECT DISTINCT * FROM news_content")).all()
    # ----------------------------------------------------------
    # news_list = News.query.from_statement(
    #     "SELECT DISTINCT * FROM news_content")

    # ================================================================
    # news_list = News.query.filter(News.section == '경제').all()
    # for news in news_list:
    #     n_li.append(dict(news.serialize))

    # n_set = set(n_li)
    # n_li = list(n_set)
    # res = json.dumps(n_li, default=alchemyencoder, ensure_ascii=False, indent=4)
    # return res
##############################################################################
##############################################################################
    # 성공한 내용!!===============================================
    # n_li = []
    # n = News.query.filter(News.section == 'IT').first()
    # n2 = News.query.filter(News.section == '경제').first()
    # n_li.append(dict(n.serialize))
    # n_li.append(dict(n2.serialize))
    # # print(type(n))                  #hynix.models.News
    # # print(type(n.serialize))        #dict
    # # print(type(dict(n.serialize)))  #dict
    #
    # res = json.dumps(n_li, default=alchemyencoder, ensure_ascii=False, indent=4)
    # # print(type(res))    #json(str 타입)
    # return res

    # json 파일로 저장해보기
    # with open("test.json", "w") as json_file:
    #     json.dump(n_li, json_file, default=alchemyencoder, ensure_ascii=False, indent=4)
    # ---------------------------------------------------------------------
    # n = News.query.filter(News.section == 'IT').first()
    # return json.dumps([dict(n.serialize)], default=alchemyencoder, ensure_ascii=False)
    # ---------------------------------------------------------------------

    # 시도해봤던 내용 =============================================================
    # for news in news_list:
    #     print(obj_as_dict(news))
    # return 'success!'

    # =============================================================
    # news_arr = []
    # for news in news_list:
    #     news_arr.append(news.toDict())
    # return jsonify(news_arr)

    # =============================================================
    # df2 = pd.read_sql(news_list.statement, news_list.session.bind)
    # return json.loads(df2.to_json(orient='records'))

    # =============================================================
    # news_list = News.query.all()  # News의 모든 튜플 저장
    # return render_template('test.html', news_list=news_list)

# ===========================================================
# def obj_as_dict(obj):
#     return {c.key: getattr(obj, c.key)
#             for c in inspect(obj).mapper.column_attrs}


# =============================================================================
# @bp.route('/post', methods=['GET', 'POST'])
# def post():
#     if request.method == 'POST':
#         value = request.form['input']
#         msg = '%s 님 환영합니다.' % value
#         return msg
#
#     if request.method == 'GET':
#         return render_template('index.html')

# from flask import Blueprint, jsonify, redirect, url_for
# @bp.route('/')
# def index():
#     return render_template('index.html')

# @bp.route('/test/<name>')
# def test(name):
#     if name == 'json':
#         return redirect(url_for('main.json_test'))  # /json 페이지로 이동
#
#
# @bp.route('/json')  # jsonify 연습
# def json_test():
#     p = [
#         {'name': 'jai', 'birth': 2020},
#         {'name': 'eun', 'birth': 1999}
#     ]
#     return jsonify(p)
#
#
# @bp.route('/hello/<user>')  # url path값 활용; 전달받은 값 활용
# def hello(user):
#     return f'Hello! {user}'
