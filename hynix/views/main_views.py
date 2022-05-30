import datetime
import decimal
import json

import pandas as pd
import sqlalchemy.exc
from flask import Blueprint

from hynix import db, create_app
from hynix.models import News, Hash
from hynix.views.hash_views import li1_hash, li2_hash
from datetime import datetime, timedelta
from . import prework_views
from sqlalchemy import func

def alchemyencoder(obj):
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)

def add_new(table, data, i):
    if table == 'News':    # News 데이터 추가
        new_event = News(data.iloc[i][0], data.iloc[i][1], data.iloc[i][2],
                         data.iloc[i][3], data.iloc[i][4], data.iloc[i][5],
                         data.iloc[i][6], data.iloc[i][7], data.iloc[i][8],
                         data.iloc[i][9], int(data.iloc[i][10]), int(data.iloc[i][11]),
                         data.iloc[i][12], data.iloc[i][13], data.iloc[i][14],
                         data.iloc[i][15], data.iloc[i][16], data.iloc[i][17],
                         data.iloc[i][18], data.iloc[i][19])
    else:   # Hash 데이터 추가
        new_event = Hash(data.iloc[i][0], float(data.iloc[i][1]))

    db.session.add(new_event)
    print("새로운", data, "데이터 추가!")

# 기사제목으로 중복 제거 & 날짜 순 리스트 return
def rm_dupli(section="all", name="all"):
    n_li = []
    if section == "all" and name == "all":  # 모든 쿼리 - 메인 화면
        news_list = News.query.order_by(func.substr(News.date, -10, 10).desc())
    elif section != "all":  # 특정 section
        news_list = News.query.filter(News.section == section).order_by(func.substr(News.date, -10, 10).desc())
    else:   # 특정 회사
        news_list = News.query.filter(News.name == name).order_by(func.substr(News.date, -10, 10).desc())
    for news in news_list:
        n_li.append(dict(news.serialize))

    origin_df = pd.DataFrame.from_records(n_li)
    origin_df = origin_df.drop_duplicates(['title'])    # 중복 제거 - 기사제목
    no_dup_li = origin_df.to_dict('records')
    return no_dup_li

# 오늘의 이슈(list3) 리스트 return
def li_3_return():
    n_li = []
    news_list = News.query.order_by(News.interest_cnt.desc())
    for news in news_list:
        n_li.append(dict(news.serialize))

    origin_df = pd.DataFrame.from_records(n_li)
    origin_df = origin_df.drop_duplicates(['title'])    # 중복 제거 - 기사제목
    no_dup_li = origin_df.to_dict('records')
    return no_dup_li

# 페이지 별로 8개씩 return
def page_show(no_dup_li, pagenum):
    fir = (pagenum - 1) * 8
    sec = (pagenum * 8)
    return no_dup_li[fir:sec]

# list2(금주의 키워드) 및 list3(오늘의 이슈) 만든 후
# 최종 json return
def res_json(li_1, section, name, pagenum, count):
    # 오늘의 이슈 -> 관심수 정렬
    ex_li_3 = li_3_return()
    li_3 = []
    for i in ex_li_3[:10]:  # 상위 10개만
        li_3.append({'url': i['url'], 'title': i['title'], 'interest_cnt': i['interest_cnt']})

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

    if pagenum <= (count/8 + 1):
        return json.dumps(res_dic, default=alchemyencoder, ensure_ascii=False, indent=4)
    else:
        return "page error!"

def db_to_news_df():
    n_li = []
    news_list = News.query.all()
    for news in news_list:
        n_li.append(dict(news.serialize))
    original_news = pd.DataFrame.from_records(n_li)
    return original_news

def every_work():
    start = prework_views.time.time()

    today_news_name = prework_views.auto_crawler()
    # today_news_name = '[2022.05.10] All_summ.csv'
    with create_app().app_context():
        # News DB delete
        try:
            now = datetime.now()
            last = (now - timedelta(weeks=1)).strftime("%Y/%m/%d")  # 일주일 전 날짜
            # 일주일 전보다 더 오래된 쿼리 삭제
            ex_news = News.query.filter(func.substr(News.date, -10, 10) <= last).all()
            for o in ex_news:
                db.session.delete(o)
            db.session.commit()
            print("일주일 전 기사 삭제 완료!")
        except sqlalchemy.exc.SQLAlchemyError as e:
            # db.session.rollback()
            print(e)

        old_news_df = db_to_news_df()

        article_data, hashtag_data = prework_views.summary(today_news_name, old_news_df)
        # article_data, hashtag_data = prework_views.summ(today_news_name)

        # News DB add
        for i in range(len(article_data)):
            if not old_news_df.empty:  # 기존 DB에 내용이 있고
                # 기존 DB와 내용(기사 제목 & 회사명)이 겹친다면 데이터 추가 불허용
                if article_data.iloc[i][4] in old_news_df['title'].unique() and article_data.iloc[i][8] in old_news_df['name'].unique():
                    print("중복!")
                else:  # 중복되는 내용이 없으면 데이터 추가 허용
                    add_new('News', article_data, i)
            else:  # 기존 DB가 비어 있으면 데이터 추가 허용
                add_new('News', article_data, i)
        db.session.commit()
        print('News DB add')

        # Hashes DB delete
        deleted_hashes = Hash.query.all()
        for i in deleted_hashes:
            db.session.delete(i)
        db.session.commit()
        print('Hashes DB delete')

        # Hashes DB add
        for i in range(len(hashtag_data)):
            add_new('Hash', hashtag_data, i)
        db.session.commit()

    # csv file delete
    prework_views.delete_csv_files(today_news_name, prework_views.enterprise_names)

    end = prework_views.time.time()
    print(f"총 소요 시간: {end - start:.5f} sec")
    print(article_data)
    print(hashtag_data)
    return article_data, hashtag_data


# 백그라운드 스케쥴러 등록(지정 시간 크롤링)
sched = prework_views.BackgroundScheduler()
sched.add_job(every_work, trigger='cron', hour='10', minute='25')
sched.start()


# 기존 url에 새롭게 추가하고 싶을 때 @bp.route를 추가하면 됨
bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/test')
def test():
    try:
        now = datetime.now()
        last = (now - timedelta(weeks=1)).strftime("%Y/%m/%d")  # 일주일 전 날짜
        print(last)     # ex)2022/03/31

        # 일단 csv에 있는 날짜로 테스트
        # today = "2022/03/16"
        # last = "%{}%".format(today)
        # print(last)

        ex_news = News.query.filter(News.date.like(last)).all()
        for o in ex_news:   # ex_news는 News 객체들 리스트
            db.session.delete(o)
        db.session.commit()
        print("쿼리 삭제!")
        return "쿼리 삭제 성공!"
    except sqlalchemy.exc.SQLAlchemyError as e:
        # db.session.rollback()
        return f'error! {e}'


# 데이터프레임 -> DB에 저장
# http://127.0.0.1:5000/first
@bp.route('/first')
def first_db():
    try:
<<<<<<< HEAD
        new_df = pd.read_csv("[2022.05.10] All.csv", encoding='utf-8-sig')
=======
        new_df = pd.read_csv("[2022.03.11]All_to_result.csv", encoding='utf-8-sig')
>>>>>>> 8651dd5a29957cc1ea950b3a7efa04ff9a4f9f97
        # 기존 db에 반복되는 내용이 있는지 체크한 후 DB에 추가
        # query -> dataframe
        # n_li = []
        # news_list = News.query.all()
        # for news in news_list:
        #     n_li.append(dict(news.serialize))
        # original_data = pd.DataFrame.from_records(n_li)
        original_data = db_to_news_df()

        for i in range(len(new_df)):
            if not original_data.empty:  # 기존 DB에 내용이 있고
                # 기존 DB와 내용(기사제목 & 회사명)이 겹친다면 데이터 추가 불허용
                if new_df.iloc[i][4] in original_data['title'].unique()\
                        and new_df.iloc[i][8] in original_data['name'].unique():
                    print("중복!")
                else:   # 중복되는 내용이 없으면 데이터 추가 허용
                    add_new('News', new_df, i)
            else:   # 기존 DB가 비어있으면 데이터 추가 허용
                add_new('News', new_df, i)

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