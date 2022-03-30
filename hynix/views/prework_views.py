# from flask import Blueprint
# import pandas as pd
#
# from numpy import dot
# from numpy.linalg import norm
# from sentence_transformers import SentenceTransformer
#
# from konlpy.tag import Okt
# from tqdm import tqdm
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.cluster import AgglomerativeClustering
#
# import key_extract
# # from konlpy.tag import Komoran
# from konlpy.tag import Kkma
# import nltk
# from nltk.tokenize import sent_tokenize
# import re
# from sklearn.preprocessing import MinMaxScaler
#
#
# nltk.download('punkt')
# model = SentenceTransformer('sentence-transformers/xlm-r-100langs-bert-base-nli-stsb-mean-tokens')
# n_cluster = 40
#
#
# bp = Blueprint('prework', __name__, url_prefix='/prework')
#
#
# @bp.route('/embedding')
# def embedding():
#     # 데이터 전처리 준비
#     data_path = "C:\projects\sksk\[220112]삼성전자.csv"
#     data = pd.read_csv(data_path)
#     data = pd.DataFrame(data.loc[:, '본문'])
#     # 'sentence-transformers/all-mpnet-base-v2'
#     data['임베딩'] = data.apply(lambda row: model.encode(row.본문), axis=1)
#     origin_data = pd.read_csv(data_path)
#     data2 = pd.concat([origin_data, data['임베딩']], axis=1)
#     # return data2.to_html()
#     return data2
#
#
# @bp.route('/clustering')
# def clustering():
#     def tokenizer(raw, pos=["Noun", "Alpha", "Number"], stopword=[]):  # 현재는 "Verb" 제외
#         return [
#             word for word, tag in okt.pos(
#                 raw,
#                 norm=True,
#                 stem=True
#             )
#             if len(word) > 1 and tag in pos and word not in stopword
#         ]
#
#     okt = Okt()  # 형태소 분석기 객체 생성
#     noun_list = []
#     data = embedding()
#
#     for content in tqdm(data['본문']):
#         nouns = okt.nouns(content)  # 명사만 추출하기, 결과값은 명사 리스트
#         noun_list.append(nouns)
#
#     # noun_list
#     data['nouns'] = noun_list
#
#     # 비어있는 명사 리스트 삭제
#     drop_index_list = []  # 지워버릴 index를 담는 리스트
#     for i, row in data.iterrows():
#         temp_nouns = row['nouns']
#         if len(temp_nouns) == 0:  # 만약 명사리스트가 비어 있다면
#             drop_index_list.append(i)  # 지울 index 추가
#     data = data.drop(drop_index_list)  # 해당 index를 지우기
#     # index를 지우면 순회시 index 값이 중간중간 비기 때문에 index를 다시 지정
#     data.index = range(len(data))
#
#     # 문서를 명사 집합으로 보고 문서 리스트로 치환 (tfidfVectorizer 인풋 형태를 맞추기 위해)
#     text = [" ".join(noun) for noun in data['nouns']]
#
#     tfidf_vectorizer = TfidfVectorizer(min_df=5, ngram_range=(1, 5))
#     tfidf_vectorizer.fit(text)
#     vector = tfidf_vectorizer.transform(text).toarray()
#
#     cluster = AgglomerativeClustering(n_clusters=n_cluster, affinity='euclidean', linkage='ward')
#     result = cluster.fit_predict(vector)
#     data['labels'] = result
#
#     # return data.to_html()
#     return data
#
#
# @bp.route('/similarity')
# def similarity():
#     # 코사인 유사도
#     def cos_sim(a, b):
#         return dot(a, b) / (norm(a) * norm(b))
#
#     # 코사인
#     def cos_sim_news(cluster, content):
#         data1 = cluster.copy()
#         embedding = model.encode(content)
#         data1['유사도'] = data1.apply(lambda x: cos_sim(x['임베딩'], embedding),
#                                    axis=1)  # print(data.loc[data['유사도'].idxmax()])
#         most_sim = data1.sort_values(by='유사도', ascending=False).head(10)  # return data.loc[data['유사도'].idxmax()]['본문']
#         return most_sim
#
#     data = clustering()
#
#     # 클러스터별로 데이터 나눠담기
#     clusters = []
#     for i in range(n_cluster):
#         clusters.append(data[data['labels'] == i])
#         clusters[i].index = range(len(clusters[i]))
#         temp = pd.DataFrame([0 for j in range(len(clusters[i]))])
#         temp.columns = ['sim_score']
#         clusters[i] = pd.concat([clusters[i], temp], axis=1)
#
#     # 유사도 점수(sim_score 계산)
#     for k in range(len(clusters)):
#         for i in range(len(clusters[k])):
#             for idx in cos_sim_news(clusters[k], clusters[k]['본문'][i]).index:
#                 clusters[k]['sim_score'][idx] = clusters[k]['sim_score'][idx] + 1
#
#     # 각 클러스터에서 가장 유사도 점수가 높은 기사만 남기기
#     max_sim_content = []
#     for j in range(len(clusters)):
#         max_sim_value = clusters[j]['sim_score'].max()
#         max_sim_idx = -1
#         for i in range(len(clusters[j])):
#             if clusters[j]['sim_score'][i] == max_sim_value:
#                 max_sim_idx = i
#                 break
#         max_sim_content.append(pd.DataFrame(clusters[j].iloc[max_sim_idx, :]).T)
#
#     result = []
#     for i in range(n_cluster):
#         result.append(max_sim_content[i].iloc[0, :].tolist())
#         print('cluster', i, '기사명:', result[i][3])
#
#     result_df = pd.DataFrame(result)
#     result_df.columns = ['언론사', '로고url', '날짜', '기사명', '섹션', '본문', 'url', '회사명', '회사종류', '추천수', '좋아요', '훈훈해요', '슬퍼요',
#                          '화나요', '후속기사 원해요',
#                          '반응수', '추천반응수', '댓글 수', '임베딩', 'nouns', 'labels', 'sim_score']
#     return result_df
#
#
# @bp.route('/summary')
# def summary():
#     # ### Komoran ###
#     # komoran = Komoran()
#     # def komoran_tokenizer(sent):
#     #     words = komoran.pos(sent, join=True)
#     #     words = [w for w in words if ('/NN' in w or '/XR' in w or '/VA' in w or '/VV' in w)]
#     #     return words
#
#     ### KKma ###
#     kkma = Kkma()
#
#     def kkma_tokenizer(sent):
#         words = kkma.pos(sent, join=True)
#         words = [w for w in words if ('/NN' in w or '/XR' in w or '/VA' in w or '/VV' in w)]
#         return words
#
#     data = similarity()
#     news = []
#     for i in range(len(data)):
#         news.append(sent_tokenize(data['본문'][i]))
#
#     summarizer = key_extract.KeysentenceSummarizer(tokenize=kkma_tokenizer, min_sim=0.3)
#     word_summarizer = key_extract.KeywordSummarizer(tokenize=kkma_tokenizer)
#
#     result = []
#     result_keyword = []
#     for i in range(len(news)):
#         try:
#             keywords = word_summarizer.summarize(news[i])
#             result_keyword.append(keywords)
#
#             if len(news[i]) <= 3:
#                 result.append(news[i])
#             else:
#                 keysents = []
#                 newsents = summarizer.summarize(news[i], topk=3)
#                 for idx in newsents:
#                     keysents.append(news[i][idx[0]])
#                 result.append(keysents)
#                 print(i)
#         except ValueError:
#             result.append('None')
#
#     for i in range(len(result_keyword)):
#         # keyword 상위 15개만 추출
#         result_keyword[i] = result_keyword[i][:15]
#         keyword_top3 = []
#         for j in range(len(result_keyword[i])):
#             # 본 데이터 형태: [(원/NNM, 2.6058335563285993), (매출/NNG, 2.401123896173394), (영업/NNG, 2.401123896173394), (이익/NNG, 2.401123896173394), ...]
#             # 전처리 후: ['원', '매출', '영업', '이익', ...]
#             result_keyword[i][j] = re.sub('[^가-힣]', '', result_keyword[i][j][0])
#             # 상위 10개 중 1글자 이하인 keyword 제외
#             if len(result_keyword[i][j]) >= 2:
#                 keyword_top3.append(result_keyword[i][j])
#             # 2자 이상인 keyword 중 상위 4개 keyword 추출, result_keyword 대체
#             if len(keyword_top3) == 4:
#                 result_keyword[i] = keyword_top3
#                 print('keyword_top3: ', keyword_top3)
#                 print('result_keyword[i]: ', result_keyword[i])
#                 break
#
#     data['요약문'] = result
#     data['키워드'] = result_keyword
#
#     # 본문 길이 60자 제한
#     for i in range(len(data)):
#         data['본문'][i] = data['본문'][i][:60]
#
#     # 추천반응수 0~10 사이 정규화
#     transformer = MinMaxScaler()
#     x_data = data['추천반응수'].values.reshape(-1, 1)
#     transformer.fit(x_data)
#     scaled_value = transformer.transform(x_data)  # 0~1
#     scaled_value = pd.DataFrame(scaled_value).mul(10)  # 0~10
#     data['정규추천반응수'] = scaled_value
#
#     # 불필요한 열 제거
#     data = data.drop(['추천수', '좋아요', '훈훈해요', '슬퍼요', '화나요', '후속기사 원해요', '반응수', '임베딩', 'nouns', 'labels', 'sim_score', '정규추천반응수'],
#                      axis='columns')
#     # data.to_csv('C:/projects/sanhak/pybo/[2022.01.12]All_to_result_1.csv', encoding='utf-8-sig')
#
#     return data.to_html()
    # data.to_csv("C:\projects\sksk\_total_test.csv", encoding='utf-8-sig')


# ###########################################################################################
# @bp.route('/summary')
# def summary():
#     # ### Komoran ###
#     # komoran = Komoran()
#     # def komoran_tokenizer(sent):
#     #     words = komoran.pos(sent, join=True)
#     #     words = [w for w in words if ('/NN' in w or '/XR' in w or '/VA' in w or '/VV' in w)]
#     #     return words
#
#     # KKma
#     kkma = Kkma()
#
#     def kkma_tokenizer(sent):
#         words = kkma.pos(sent, join=True)
#         words = [w for w in words if ('/NN' in w or '/XR' in w or '/VA' in w or '/VV' in w)]
#         return words
#
#     data = similarity()
#     news = []
#     for i in range(len(data)):
#         news.append(sent_tokenize(data['본문'][i]))
#
#     summarizer = key_extract.KeysentenceSummarizer(tokenize=kkma_tokenizer, min_sim=0.3)
#
#     result = []
#     for i in range(len(news)):
#         try:
#             if len(news[i]) <= 3:
#                 result.append(news[i])
#             else:
#                 keysents = []
#                 newsents = summarizer.summarize(news[i], topk=3)
#                 for idx in newsents:
#                     keysents.append(news[i][idx])
#                 result.append(keysents)
#                 print(i)
#         except ValueError:
#             result.append('None')
#
#     data['요약문'] = result
#
#     return data.to_html()
