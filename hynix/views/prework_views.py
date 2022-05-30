from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import time                     # 소요시간 측정
import pandas as pd
import numpy as np
from apscheduler.schedulers.background import BackgroundScheduler
from selenium import webdriver  # crawling
from bs4 import BeautifulSoup
from tqdm import tqdm
import re
import kss
from time import sleep
from datetime import date, timedelta
from numpy import dot           # similarity
from numpy.linalg import norm
from sentence_transformers import SentenceTransformer
from konlpy.tag import Okt      # clustering
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import AgglomerativeClustering
from kobart import get_kobart_tokenizer
from transformers.models.bart import BartForConditionalGeneration
import torch
import key_extract              # textrank keyword
from konlpy.tag import Kkma     # from konlpy.tag import Komoran
import nltk
from nltk.tokenize import sent_tokenize
from sklearn.preprocessing import MinMaxScaler
import os

pd.set_option('mode.chained_assignment', None) # 경고 off
db = SQLAlchemy()
migrate = Migrate()
driverpath = "C:/projects/sksk/"
csvfilepath = "C:/projects/sksk/"
kobart_model_path = 'C:/projects/sksk/kobart/'
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
nltk.download('punkt')
model = SentenceTransformer('sentence-transformers/xlm-r-100langs-bert-base-nli-stsb-mean-tokens')
n_cluster = 40 # 클러스터 수이자 최종 노출 기사 수
n_keyword = 4 # 해시태그 개수

company_dic = {'하이닉스': 'IDM', '삼성전자': 'IDM', '인텔': 'IDM', '웨스턴디지털': 'IDM', 'TI': 'IDM', 'Renesas': 'IDM',
               '소니': 'IDM', '마이크론': 'IDM', '후지쯔': 'IDM', 'STMicro': 'IDM', 'ST마이크로일렉트로닉스': 'IDM', '도시바': 'IDM',
               '키옥시아': 'IDM',
               'Qualcomm': 'Fabless', '퀄컴': 'Fabless', 'Broadcom': 'Fabless', '브로드컴': 'Fabless', 'Xilinx': 'Fabless',
               '자일링스': 'Fabless', 'NVIDIA': 'Fabless', '엔비디아': 'Fabless', 'AMD': 'Fabless',
               'MediaTek': 'Fabless', '미디어텍': 'Fabless', 'HiSilicon': 'Fabless', '하이실리콘': 'Fabless', 'LX세미콘': 'Fabless',
               'TSMC': 'Foundry', 'GlobalFoundries': 'Foundry', '글로벌파운드리즈': 'Foundry', 'UMC': 'Foundry',
               'SMIC': 'Foundry', 'DB하이텍': 'Foundry'}
modify_name_dic = {'하이닉스': 'SK하이닉스', 'Qualcomm': '퀄컴', 'STMicro': 'ST마이크로', 'Broadcom': '브로드컴', 'Xilinx': '자일링스',
            'NVIDIA': '엔비디아', 'MediaTek': '미디어텍', 'HiSilicon': '하이실리콘', 'GlobalFoundries': '글로벌파운드리즈'}
enterprise_names = set(company_dic.keys())
stopwords = {'반도체', '이날', '전날', '전일', '오전', '원', '일', '어치', '베스트', '산업', '기업', '그룹', '업체', '시장', '국가', '와이', '파이' }

# crawling
def preprocessing(data, col):
    data.drop_duplicates(subset=['본문'], inplace=True)  # 중복 제거
    data.reset_index(drop=True, inplace=True)

    for i in tqdm(range(len(data[col]))):
        if col == '본문':
            data.loc[i, col] = re.sub(r'\[[^)]*\]', '', str(data[col][i]))  # 대괄호 및 괄호 안 문자
        data.loc[i, col] = re.sub(r'\＜[^)]*\＞', '', str(data[col][i]))  # 부등호 및 부등호 안 문자
        data.loc[i, col] = re.sub(r'\<[^)]*\>', '', str(data[col][i]))  # 부등호 및 부등호 안 문자
        data.loc[i, col] = re.sub(r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', '', str(data[col][i]))  # 메일 형식
        data.loc[i, col] = re.sub(
            r'((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*', '',
            str(data[col][i]))  # url 형식
        data.loc[i, col] = re.sub(r'\d{4}-\d{2}-\d{2}', '', data[col][i])  # 날짜 yyyy-mm-dd
        data.loc[i, col] = re.sub(r'\d{4}/\d{2}/\d{2}', '', data[col][i])  # 날짜 yyyy/mm/dd
        data.loc[i, col] = re.sub(r'\d{2}:\d{2}', '', data[col][i])  # 시간
        data.loc[i, col] = re.sub(' +', ' ', data[col][i])  # 다중 공백 하나로

    data[col] = data[col].str.replace('\n', " ", regex=True)  # 개행문자
    data[col] = data[col].str.replace("[^가-힣|ㄱ-ㅎ|ㅏ-ㅣ|0-9|a-z|A-Z|(~%)|.]", " ", regex=True)  # 한글+숫자+영어+기타 의미있는 특수문자를 제외한 모든 문자

    data.reset_index(drop=True, inplace=True)
    return data
def sentence_spliter(data, col1, col2) :
    data[col2] = '0' # '본문split' 빈 열 만들기
    drop_list = [] # 문장수가 많거나 적은 기사 index 저장

    print('sentence split 시작')
    sent_split_start = time.time()

    for i, contents in tqdm(enumerate(data[col1])) :
        contents_list = [] # 기사를 3개로 나눈 문장들 저장하는 리스트

        sents = kss.split_sentences(contents)
        index = len(sents)
        # print("\n", i, "번째 기사 문장 개수 :", index, end = " ")

        # 3문장 이하인 기사 제거
        if index <= 3 :
            drop_list.append(i)

        elif index >= 15 and index < 70:
            contents_list = [sents[:int(index/3)], sents[int(index/3):int((index/3)*2)], sents[int((index/3)*2):]]

            contents_list = str(contents_list).replace("\',", "").replace("\'", "")
            contents_list = str(contents_list).replace("[[", "[").replace("]]", "]")

            data.loc[i, col2] = str(contents_list)

        # 70문장 이상인 기사 제거
        elif index >= 70 :
            drop_list.append(i)
            # print(drop_list, end = "")

        # 문장 수가 3개 이상 15개 미만인 경우 분할 x
        else :
            # print('(15개 미만)', end = " ")
            data.loc[i, col2] = '[\'[' + data.loc[i, col1] + ']\']'

    data.drop(drop_list, inplace=True)
    data.reset_index(drop=True, inplace=True)

    print('sentence split  완료, 소요시간 ', end='')
    sent_split_end = time.time()
    print(f"{sent_split_end - sent_split_start:.5f} sec")

    return data
def url_crawler(driver_path, dictionary, ds, de) :
    for keyword in tqdm(dictionary.keys()) :
        try:
            df = pd.read_csv(csvfilepath + '[{}] {}_url.csv'.format(ds, keyword), engine='python')
        except:
            print("현재 검색 키워드 : ", keyword)
            pagenum = 0
            next_page = 0
            url_list = []
            # global driver
            while(True) :
                try :
                    driver = webdriver.Chrome(driver_path + "chromedriver.exe", options=options)
                    url = "https://search.naver.com/search.naver?where=news&sm=tab_opt&photo=0&field=0&pd=3&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&ds={}&de={}&query={}&sort=1".format(
                        ds, de, keyword) + "&start=" + str(int(next_page) * 10 + 1)
                    driver.get(url)
                    time.sleep(2)

                    # 네이버뉴스 url 수집하기
                    things = driver.find_elements_by_link_text('네이버뉴스')

                    for thing in things:
                        url = thing.get_attribute('href')
                        url_list.append(url)

                    # 10개마다 print
                    if(int(next_page) % 10 == 0):
                        print(int(next_page) + 1, '페이지 수집 완료(10페이지 단위로 출력)')

                    try:
                        driver.find_element_by_xpath('//*[@id="main_pack"]/div[2]/div/a[2]').click()
                        # print("다음 페이지 : ", next_page + 2)

                    except:
                        print("마지막 페이지")
                        pagenum = next_page
                        break

                    pagenum = next_page  # 현재 페이지 번호
                    next_page += 1

                    # 다음 페이지 번호가 현재 페이지 번호와 동일할 때 반복 종료
                    if pagenum == next_page:
                        driver.close()
                        break

                except:
                    print("except")
                    continue

                finally:
                    driver.close()

            # url_list 저장
            df = pd.DataFrame({"url":url_list})
            df.to_csv(csvfilepath + '[{}] {}_url.csv'.format(ds, keyword), encoding='utf-8-sig', index=False)
def content_crawler(driver_path, dictionary, ds, de):
    for keyword in tqdm(dictionary.keys()):
        df = pd.read_csv(csvfilepath + '[{}] {}_url.csv'.format(ds, keyword), engine='python')

        try :
            df_content = pd.read_csv(csvfilepath + '[{}] {}.csv'.format(ds, keyword), engine='python')
            content_len = len(df_content)
        except :
            content_len = 0
            pass

        number = len(df['url'])

        # url 하나라도 존재하고 본문 csv는 없을 때 본문 크롤링 시작
        if number != 0 and content_len == 0:
            print("현재 검색 키워드 :", keyword, ', 기사 개수 :', number)

            dict = {}

            # 페이지당 기사 수집
            for i in tqdm(range(number)):
                url = df['url'][i]

                try:
                    driver = webdriver.Chrome(driver_path + "chromedriver.exe", options=options)
                    driver.get(url)
                    time.sleep(0.5)
                    # print(url)

                    header = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36'}
                    sleep(1)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                except Exception as e:
                    print(e)
                    break

                try:
                    # 첫번째 이미지 url(이미지 없을 경우 == naver 로고 이미지 => none)
                    first_img_url = soup.select_one("span.end_photo_org > div > div > img")["src"]
                except:
                    first_img_url = "none"

                try:
                    # print("첫번째 이미지 url : ", first_img_url)

                    date = soup.select_one("span.media_end_head_info_datestamp_time").text
                    if date[12:14] == "오전":
                        meridiem = "AM"
                    elif date[12:14] == "오후":
                        meridiem = "PM"
                    ymd = date[:10].replace('.', '/')  # yyyy/mm/dd 형태로 변환
                    date = date[15:] + " " + meridiem + " " + ymd  # 최종 date 형태 :  5:03 PM 2022/01/12
                    # print(date)

                    title = soup.select_one("h2.media_end_head_headline").text
                    section = soup.select_one("em.media_end_categorize_item").text
                    # print(title, " <", section, ">")

                    content = soup.select_one("div.newsct_article._article_body").text
                except:
                    pass

                try:
                    # 요약문 존재할 경우 본문에서 제거
                    summary = soup.find("strong", class_="media_end_summary").get_text()
                    content = content.replace(summary, "")
                except:
                    # print("요약문 없음")
                    pass

                try:
                    # 영상 존재할 경우 본문에서 제거
                    video_area = soup.find("div", class_="video_area _VIDEO_AREA").get_text()
                    content = content.replace(video_area, "")
                    #                     print(content)
                except Exception as e:
                    # print("영상 없음")
                    pass

                try:
                    # 언론사명, url, 로고 url
                    press_name = soup.select_one("div.media_end_head_top > a > img")["title"]
                    # print('press_name :', press_name)

                    press_url = soup.select_one("div.media_end_head_top > a")["href"]
                    # print('press_url :', press_url)

                    press_logo_url = soup.select_one("div.media_end_head_top > a > img")['src']
                    # print("press_logo_url :", press_logo_url)

                    # 관심수
                    reactions = soup.select("ul.u_likeit_layer > li > a > span.u_likeit_list_count._count")
                    react1 = int(reactions[0].text.replace(',', ""))
                    react2 = int(reactions[1].text.replace(',', ""))
                    react3 = int(reactions[2].text.replace(',', ""))
                    react4 = int(reactions[3].text.replace(',', ""))
                    react5 = int(reactions[4].text.replace(',', ""))

                    review = 0
                    review = int(soup.select("span.u_cbox_count")[0].text.replace(',', ""))
                    # print("review 1 성공")

                except :
                    pass

                try :
                    # 댓글 정책에 따라 보여지지 않는 경우
                    review = int(soup.select("em.simplecmt_num._COMMENT_COUNT_VIEW")[0].text.replace(',', ""))
                    # print("review 2 성공")

                except :
                    pass

                try:
                    #print(react1, react2, react3, react4, react5, review)

                    # 딕셔너리에 저장
                    news_info = {}

                    news_info['날짜'] = date
                    news_info['기사명'] = title
                    news_info['섹션'] = section
                    news_info['본문'] = content
                    news_info['본문url'] = url
                    news_info['언론사'] = press_name
                    news_info['언론사url'] = press_url
                    news_info['언론사로고url'] = press_logo_url
                    news_info['회사명'] = keyword
                    news_info['회사종류'] = dictionary.get(keyword)
                    news_info['관심수'] = react1 + react2 + react3 + react4 + react5
                    news_info['댓글수'] = review
                    news_info['첫번째이미지url'] = first_img_url

                    dict[i] = news_info

                    time.sleep(1)
                except Exception as e:
                    print(e)
                    pass
                finally:
                    driver.close()

            # DataFrame에 저장
            result_df = pd.DataFrame.from_dict(dict, 'index')
            print(len(result_df))
            try:
                # 전처리
                if len(result_df) != 0:
                    result_df = preprocessing(result_df, '본문')
                    print("\n전처리 완료")
                    result_df = sentence_spliter(result_df, '본문', '본문split')
                    print("\n문장 분할 완료")

                result_df.to_csv(csvfilepath+"[{}] {}.csv".format(ds, keyword), encoding="utf-8-sig", index=False)
                print(keyword + " 저장 완료")
            except:
                print(keyword + " 전처리 및 저장 실패")
                continue
def integrate_crawling_data(ds, enterprise_names, modify_name_dic):

    #All 파일 존재하는지 확인
    try:
        file = pd.read_csv("[{}] All.csv".format(ds), encoding="utf-8-sig")
        if len(file) != 0:
            print(ds, "All 파일 존재")

    except:
        print(ds, "All 파일 없음")
        file = pd.DataFrame()

    if len(file) == 0:
        print("try문 실행")

        for keyword in enterprise_names:
            name_pre = "[{}] ".format(ds)
            name = keyword
            name_sub = '.csv'
            try :
                article = pd.read_csv(csvfilepath + name_pre + name + name_sub, engine='python', encoding='utf-8-sig')
                #         article = preprocessing(article, '본문')
                print('[' + name + '] 기사 개수 :', len(article))
                file = pd.concat([file, article])
                file.reset_index(inplace=True, drop=True)
            except:
                print('[' + name + '] 기사 개수 : 0')
                pass

        # 기업명 통일
        for enter_name in modify_name_dic.keys():
            file.loc[file['회사명'] == enter_name, '회사명'] = modify_name_dic.get(enter_name)

        # section 생활/오피니언 삭제
        section_drop_list = file[(file['섹션'] == '생활') | (file['섹션'] == '오피니언')].index
        file.drop(section_drop_list, inplace=True)
        file.reset_index(inplace=True, drop=True)

        file.to_csv(csvfilepath + "[{}] All.csv".format(ds), encoding="utf-8-sig", index=False)

    return "[{}] All.csv".format(ds)
def auto_crawler():
    print('crawling 시작')
    crawling_start = time.time()

    global driverpath, company_dic
    # now = datetime.now()
    # ds = now.strftime('%Y.%m.%d')
    # ds_list = ['2022.05.11', '2022.05.12', '2022.05.13', '2022.05.14']

    # ds = '2022.05.21'
    # de = ds

    ### 어제 날짜 설정
    yesterday = date.today() - timedelta(1)
    yesterday = yesterday.strftime('%Y.%m.%d')
    ds = yesterday
    de = yesterday

    print(ds, "크롤링 시작")
    # url_crawler(driverpath, company_dic, ds, de)
    # content_crawler(driverpath, company_dic, ds, de)
    filename = integrate_crawling_data(ds, enterprise_names, modify_name_dic)

    crawling_end = time.time()
    print('crawling 완료, 소요시간 ', end='')
    print(f"{crawling_end - crawling_start:.5f} sec")

    return filename

# embedding
def embedding(filename):
    print('embedding 시작')
    embedding_start = time.time()

    # 데이터 준비
    data_path = filename
    data = pd.read_csv(csvfilepath + data_path)

    # 임베딩
    content_embed_list = [model.encode(data['본문'][i]) for i in range(len(data))]
    data['임베딩'] = content_embed_list

    print('embedding 완료, 소요시간 ', end='')
    embedding_end = time.time()
    print(f"{embedding_end - embedding_start:.5f} sec")
    return data

# clustering
def clustering(filename):
    okt = Okt()  # 형태소 분석기 객체 생성
    noun_list = []
    data = embedding(filename)

    print('clustering 시작')
    clustering_start = time.time()

    # 기사 본문에 나타난 명사 임베딩 벡터를 이용해 클러스터링 진행
    for content in tqdm(data['본문']):
        nouns = okt.nouns(content)
        noun_list.append(nouns)
    data['nouns'] = noun_list

    # 비어있는 명사 리스트 삭제
    drop_index_list = []
    for i, row in data.iterrows():
        temp_nouns = row['nouns']
        if len(temp_nouns) == 0:  # 명사 리스트가 비어 있을 경우
            drop_index_list.append(i)
    data = data.drop(drop_index_list)  # 해당 index를 삭제
    # index 재지정
    data.index = range(len(data))

    # 문서를 명사 집합으로 보고 문서 리스트로 치환
    text = [" ".join(noun) for noun in data['nouns']]
    # TF-IDF 임베딩 진행
    tfidf_vectorizer = TfidfVectorizer(min_df=5, ngram_range=(1, 5))
    tfidf_vectorizer.fit(text)
    vector = tfidf_vectorizer.transform(text).toarray()

    # SBERT embedding vector 이용하여 클러스터링을 진행할 경우
    # vector = data['임베딩'].to_list()

    # Hierarchical Clustering
    cluster = AgglomerativeClustering(n_clusters=n_cluster, affinity='euclidean', linkage='ward')
    result = cluster.fit_predict(vector)
    data['labels'] = result

    print('clustering 완료')
    clustering_end = time.time()
    print(f"{clustering_end - clustering_start:.5f} sec")
    return data

# similarity
def cos_sim(a, b):                      # 코사인 유사도
    return dot(a, b) / (norm(a) * norm(b))
def cos_sim_news(cluster, content):     # 기사 코사인 유사도
    data1 = cluster.copy()
    embedding = model.encode(content)
    data1['유사도'] = data1.apply(lambda x: cos_sim(x['임베딩'], embedding), axis=1)
    most_sim = data1.sort_values(by='유사도', ascending=False).head(10)
    return most_sim
def similarity(filename):
    data = clustering(filename)

    print('similarity 검사 시작')
    similarity_start = time.time()

    # 클러스터별로 데이터 나눠담기
    print('클러스터별로 데이터 나눠담는 중...')
    clusters = []
    for i in range(n_cluster):
        clusters.append(data[data['labels'] == i])
        clusters[i].index = range(len(clusters[i]))
        temp = pd.DataFrame([0 for j in range(len(clusters[i]))])
        temp.columns = ['sim_score']
        clusters[i] = pd.concat([clusters[i], temp], axis=1)

    # 유사도 점수(sim_score 계산)
    print('유사도 점수(sim_score) 계산 중...')
    for k in range(len(clusters)):
        for i in range(len(clusters[k])):
            for idx in cos_sim_news(clusters[k], clusters[k]['본문'][i]).index:
                clusters[k]['sim_score'][idx] = clusters[k]['sim_score'][idx] + 1

    # 각 클러스터에서 가장 유사도 점수가 높은 기사만 남기기
    print('각 클러스터에서 가장 유사도 점수가 높은 기사만 남기는 중...')
    max_sim_content = []
    for j in range(len(clusters)):
        max_sim_value = clusters[j]['sim_score'].max()
        max_sim_idx = -1
        for i in range(len(clusters[j])):
            if clusters[j]['sim_score'][i] == max_sim_value:
                max_sim_idx = i
                break
        max_sim_content.append(pd.DataFrame(clusters[j].iloc[max_sim_idx, :]).T)

    result = []
    for i in range(n_cluster):
        result.append(max_sim_content[i].iloc[0, :].tolist())
        print('cluster', i, '기사명:', result[i][1])

    result_df = pd.DataFrame(result)
    result_df.columns = ['날짜', '기사명', '섹션', '본문', '본문url', '언론사', '언론사url', '언론사로고url',
                         '회사명', '회사종류', '관심수', '댓글수', '첫번째이미지url', '본문split', '임베딩', 'nouns', 'labels', 'sim_score']

    print('similarity 검사 완료')
    similarity_end = time.time()
    print(f"{similarity_end - similarity_start:.5f} sec")
    return result_df

# summary
kkma = Kkma()
def kkma_tokenizer(sent):
    global kkma
    words = kkma.pos(sent, join=True)
    words = [w for w in words if ('/NN' in w or '/XR' in w or '/VA' in w or '/VV' in w)]
    return words
def kkma_word_tokenizer(sent):
    global kkma
    words = kkma.pos(sent, join=True)
    words = [w for w in words if ('/NN' in w or '/NR' in w or '/NP' in w)]
    return words
def summary(today_data_path, old_data):
    data = similarity(today_data_path)

    print('summary 시작')
    summary_start = time.time()

    kobart_model = BartForConditionalGeneration.from_pretrained(kobart_model_path)
    kobart_tokenizer = get_kobart_tokenizer()

    print('생성 요약 진행 중...')
    for data_index in tqdm(range(len(data))):
        # '본문split'열에 저장된 문자열 배열을 , 기준으로 분리
        text_array = data.loc[data_index, '본문split'].split(",")

        # 문단 수만큼 반복(ex. 문단 3개면 3번 반복하면서 한 문단씩 모델에 input으로)
        for index in range(len(text_array)):
            input_ids = kobart_tokenizer.encode(text_array[index], max_length=1024, truncation=True)
            input_ids = torch.tensor(input_ids)
            input_ids = input_ids.unsqueeze(0)

            # output = kobart_model.generate(input_ids, pad_token_id=1, max_length=512, num_beams=5, early_stopping=True, no_repeat_ngram_size=3, repetition_penalty=1.5)
            output = kobart_model.generate(input_ids, pad_token_id=1, do_sample=True, max_length=512, top_k=50, top_p=0.92, early_stopping=True)
            output = kobart_tokenizer.decode(output[0], skip_special_tokens=True)

            # 요약 대상 문단 3개일 경우
            if len(text_array) == 3:
                data.loc[data_index, '요약문' + str(index + 1)] = output
            # 본문 길이가 짧아 split되지 않은 경우 요약문 2, 3에 공백 저장
            else:
                data.loc[data_index, '요약문1'] = output
                data.loc[data_index, '요약문2'] = ''
                data.loc[data_index, '요약문3'] = ''

    print('summary 완료')
    summrary_end = time.time()
    print(f"{summrary_end - summary_start:.5f} sec")

    news = []

    news = [sent_tokenize(data['본문'][i]) for i in range(len(data))]

    summarizer = key_extract.KeysentenceSummarizer(tokenize=kkma_tokenizer, min_sim=0.3)
    word_summarizer = key_extract.KeywordSummarizer(tokenize=kkma_word_tokenizer)

    print('키워드 추출 중...')
    result_keyword = []  # 기사 키워드

    # for i in tqdm(range(len(news))):
    #     keywords = word_summarizer.summarize(news[i])
    #     result_keyword.append(keywords)
    result_keyword = [word_summarizer.summarize(news[i]) for i in tqdm(range(len(news)))]

    print('주요 키워드 추출 중...')
    # 기사별 주요 키워드 뽑기
    for i in tqdm(range(len(result_keyword))):
        # keyword 상위 15개만 추출
        result_keyword[i] = result_keyword[i][:15]
        keyword_top4 = []
        for j in range(len(result_keyword[i])):
            # 본 데이터 형태: [(원/NNM, 2.6058335563285993), (매출/NNG, 2.401123896173394), (영업/NNG, 2.401123896173394), (이익/NNG, 2.401123896173394), ...]
            # 전처리 후: ['원', '매출', '영업', '이익', ...]
            result_keyword[i][j] = re.sub('[^가-힣]', '', result_keyword[i][j][0])
            # 상위 10개 중 1자 이하인 keyword 제외, 불용어 및 회사명 제외
            if len(result_keyword[i][j]) >= 2:
                if (result_keyword[i][j] not in stopwords) and (result_keyword[i][j] not in enterprise_names):
                    keyword_top4.append(result_keyword[i][j])
            # 2자 이상인 keyword 중 상위 4개 keyword 추출, result_keyword 대체
            if len(keyword_top4) == n_keyword:
                result_keyword[i] = keyword_top4
                # 확인용
                # print('keyword_top4: ', keyword_top4)
                # print('result_keyword[i]: ', result_keyword[i])
                break

    data['키워드'] = result_keyword

    '''### 해시태그/가중치 정리 ###'''

    print('hashtag 정리 시작')
    hashtag_start = time.time()
    print(data)

    # 키워드 dictionary화(중복제거)
    # key = 키워드, value = 관심수
    # {'가격': 4071, '감리': 104, '개발': 231, '거래': 1582, '건수': 1935, ...}
    keyword_dic = {}

    # 당일 기사 키워드
    keyword_df_today = data['키워드']
    keyword_df_today = pd.DataFrame(keyword_df_today, columns=['키워드'])

    for i in range(len(keyword_df_today)):
        for j in range(n_keyword):
            if keyword_df_today['키워드'][i][j] in keyword_dic.keys():  # dictionary에 존재하는 keyword일 경우 value 값 관심수만큼 증가
                keyword_dic[keyword_df_today['키워드'][i][j]] = keyword_dic[keyword_df_today['키워드'][i][j]] + data['관심수'][i]
            else:  # dictionary에 존재하지 않는 keyword일 경우 value에 관심수 대입
                keyword_dic[keyword_df_today['키워드'][i][j]] = data['관심수'][i]

    # 지난 6일 기사 키워드
    # keywork_df_old = old_data['키워드']
    # keywork_df_old = pd.DataFrame(keywork_df_old, columns=['키워드'])

    # ole_data = db에서 불러온 데이터. '키워드' 열 하나로 통합
    # print(old_data.columns)
    if len(old_data) > 0 :
        keyword_df_old = old_data['hashtag']   # [{'hash1': '단어1'}, {'hash2': '단어2'}, {'hash3': '단어3'}, {'hash4': '단어4'}]
        # print(keyword_df_old[0], keyword_df_old[0][0], keyword_df_old[0][0]['hash1'])
        for i in range(len(keyword_df_old)):
            keyword_list = []
            for j in range(n_keyword):
                col_name = 'hash'+str(j+1)
                keyword_list.append(keyword_df_old[i][j][col_name])
            keyword_df_old[i] = keyword_list
        # keywork_df_old = keyword_df_old.drop(['hash2', 'hash3', 'hash4'], axis='columns')
        # keyword_df_old = pd.DataFrame(keyword_df_old, coumns=['키워드'])
        keyword_df_old = keyword_df_old.to_frame(name='키워드')

        for i in range(len(keyword_df_old)):
            for j in range(n_keyword):
                if keyword_df_old['키워드'][i][j] in keyword_dic.keys():  # dictionary에 존재하는 keyword일 경우 value 값 관심수만큼 증가
                    keyword_dic[keyword_df_old['키워드'][i][j]] = keyword_dic[keyword_df_old['키워드'][i][j]] + old_data['interest_cnt'][i]
                else:  # dictionary에 존재하지 않는 keyword일 경우 value에 관심수 대입
                    keyword_dic[keyword_df_old['키워드'][i][j]] = old_data['interest_cnt'][i]

    # print(keyword_dic)
    # print(keyword_dic.items())
    hashtag_df = pd.DataFrame(keyword_dic.items(), columns=['해시태그', '가중치'])
    # print(hashtag_df)

    # 가중치 정규화 --> 정규가중치
    transformer = MinMaxScaler()
    x_data = hashtag_df['가중치'].values.reshape(-1, 1)
    transformer.fit(x_data)
    scaled_value = transformer.transform(x_data)  # 0~1
    scaled_value = pd.DataFrame(scaled_value)
    scaled_value = scaled_value.mul(100)  # 0~10
    # scaled_value = scaled_value[scaled_value > 2].dropna()
    hashtag_df['정규가중치'] = scaled_value
    hashtag_df.sort_values(by='정규가중치', ascending=False)
    # print(hashtag_df)

    # 이상치 제거
    q1, q3 = np.percentile(hashtag_df['가중치'], [25, 75])
    hashtag_df = hashtag_df.drop(hashtag_df[hashtag_df['가중치'] < q1].index)
    hashtag_df = hashtag_df.drop(hashtag_df[hashtag_df['가중치'] > q3].index)
    hashtag_df.reset_index(inplace=True, drop=True)

    # print(hashtag_df)
    print('hashtag 정리 완료')
    # print(hashtag_df)
    hashtag_end = time.time()

    print(f"{hashtag_end - hashtag_start:.5f} sec")




    '''#### 결과 데이터 정리 ####'''

    print('결과 data 정리 시작')
    # 본문 길이 60자 제한
    for i in range(len(data)):
        data.loc[i, '본문'] = data.loc[i, '본문'][:60]

    ### 키워드 리스트를 열로 분리 ###
    # 분리 전: '키워드' 열에 키워드 리스트 전체 저장
    # 키워드 - ['시스코', '디지털', '시장', '코리아']
    # 분리 후: '키워드' 열을 '키워드1', '키워드2', '키워드3', '키워드4' 열로 분리하여 열마다 하나의 키워드 저장(키워드 앞에 # 붙임)
    # 키워드1 - '#시스코', 키워드2 = '#디지털', 키워드3 - '#시장', 키워드4 - '#코리아'
    keyword_df = data['키워드']
    keyword_df = pd.DataFrame(keyword_df, columns=['키워드'])
    # hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')  # 한글과 띄어쓰기를 제외한 모든 글자
    for i in range(len(keyword_df)):
        # print(type(keyword_df['키워드'][i]), keyword_df['키워드'][i])
        # keyword_df['키워드'][i] = ast.literal_eval(keyword_df['키워드'][i])
        # keyword_df['키워드'][i] = hangul.sub('', keyword_df['키워드'][i])  # 한글과 띄어쓰기를 제외한 모든 부분을 제거
        keyword_df['키워드'][i] = ' '.join(keyword_df['키워드'][i])
    for i in range(n_keyword):
        col_name = '키워드' + str(i + 1)
        keyword_df[col_name] = keyword_df.키워드.str.split(' ').str[i]
        # for j in range(len(keyword_df)):
        #     keyword_df[col_name][j] = "#" + keyword_df[col_name][j]
        data[col_name] = keyword_df[col_name]

    # 기사 관련 데이터(article_data)
    # [언론사, 로고url, 날짜, 기사명, 섹션, 본문, url, 회사명, 회사종류, 좋아요, 추천반응수, 댓글수, 요약문, 키워드]
    #
    # result_df.columns = ['날짜', '기사명', '섹션', '본문', '본문url', '언론사', '언론사url', '언론사로고url',
    #                          '회사명', '회사종류', '관심수', '댓글수', '첫번째이미지url', '본문split']
    # article_data = data.drop(
    #     ['추천수', '훈훈해요', '슬퍼요', '화나요', '후속기사 원해요', '반응수', '임베딩', 'nouns', 'labels', 'sim_score', '키워드'],
    #     axis='columns')
    article_data = data.drop(['본문split', '임베딩', 'nouns', 'labels', 'sim_score', '키워드'], axis='columns')
    columns_order = ['언론사', '언론사url', '언론사로고url', '날짜', '기사명', '섹션', '본문', '본문url', '회사명', '회사종류', '관심수', '댓글수', '첫번째이미지url', '요약문1', '요약문2', '요약문3', '키워드1', '키워드2', '키워드3', '키워드4']
    article_data = article_data[columns_order]
    article_data.to_csv(today_data_path[:-8]+'_summary.csv', encoding='utf-8-sig', index=False)

    # 해시태그 관련 데이터(hashtag_data)
    # [해시태그, 정규가중치]
    wordcloud_fontsize_min = 2.5
    wordcloud_fontsize_max = 9
    hashtag_df['정규가중치'] = hashtag_df['정규가중치'] * 10
    hashtag_data = hashtag_df[['해시태그', '정규가중치']]
    hashtag_data = hashtag_data.drop(hashtag_data[hashtag_data['정규가중치'] < 2].index)  # 가중치 2 미만 해시태그 제거
    hashtag_data.reset_index(inplace=True, drop=True)
    for i in range(len(hashtag_data)):
        if hashtag_data['정규가중치'][i] < wordcloud_fontsize_min:
            hashtag_data['정규가중치'][i] = wordcloud_fontsize_min
        elif hashtag_data['정규가중치'][i] > wordcloud_fontsize_max:
            hashtag_data['정규가중치'][i] = wordcloud_fontsize_max
    hashtag_data.to_csv(today_data_path[:-8]+'_hashtag.csv', encoding='utf-8-sig', index=False)

    print('요약 데이터 정리 완료')

    return article_data, hashtag_data
    # return article_data.to_html()
def summ(today_data_path) :
    article_data = pd.read_csv(today_data_path[:-8]+'_summary.csv', encoding='utf-8-sig')
    hashtag_data = pd.read_csv(today_data_path[:-8]+'_hashtag.csv', encoding='utf-8-sig')
    return article_data, hashtag_data

# delete crawling data
def delete_csv_files(today_news_name, enterprise_names):
    file_pre = today_news_name[:-7] # '[2022.00.00] ' <- 공백 포함
    file_middle = enterprise_names
    file_suf = ['.csv', '_url.csv']
    # 회사별 csv 삭제
    for name in file_middle:
        for suf in file_suf:
            file_path = file_pre + name + suf
            if os.path.exists(file_path):
                os.remove(file_path)

    # All csv 삭제
    # file_path = file_pre + 'All.csv'
    # if os.path.exists(file_path):
    #     os.remove(file_path)

    # summary, hashtag csv 삭제
    file_pre = file_pre[:-1]
    file_suf = ['_summary.csv', '_hashtag.csv']
    for suf in file_suf:
        file_path = file_pre + suf
        if os.path.exists(file_path):
            os.remove(file_path)


