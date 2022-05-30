## NewSpace :rocket:

>**_2022 SW산학연계 프로젝트  
"반도체 시장 관련 정보 및 Trend를 제공하는 의사결정 지원도구 개발"_**  


:arrow_forward: **Problem Definition**
-  실시간으로 축적되는 __대량의 뉴스 기사__
-  모든 기사를 사람이 파악, 분석하는 것은 사실상 불가능
-  자동 수집 및 분석으로 __핵심 정보 도출의 필요성__ 증대
  

:arrow_forward: **Development Plan**
- Data collecting & Processing  
- Deduplication & Dealing with Meaningless Data    
- Summarization News Article
- Web Server Building & Web Service Implementation  
  
  
:arrow_forward: **Data Pipeline**
![image](https://user-images.githubusercontent.com/86818579/170230243-77d1ed3b-6ebe-4284-924a-b4251282ca76.png)
  

:one: **Data Crawling & Preprocessing**   
-  매일 자정, 자동 Crawling 진행
-  반도체 공정별 (IDM / Fabless / Foundry) 주요 기업 엄선
-  작일 작성된 네이버 뉴스 기사 URL 수집 (검색 키워드: 기업명)
-  URL 기준으로 기사 관련 데이터 수집

-  기업별 중복 기사 제거
-  원문에 포함된 무의미한 문자열 (ex: 이메일, URL, 날짜) 제거
-  3 문장 이하, 70 문장 이상의 기사 제거
-  요약 모델 Input을 위한 문단 분할 → 원문 기준 3분할
-  전체 기사에 대한 하나의 통합 파일 생성

:two: **Deduplication**   
![image](https://user-images.githubusercontent.com/86818727/170232519-5733d6f5-b1cd-45df-a449-3d234c9ec5ca.png)
-  SBERT를 이용해 기사 본문 임베딩 벡터 추출
-  Hierarchical Clustering으로 유사 주제인 40개의 기사 군집 형성
-  하나의 군집 내에서 특정 기사와 다른 모든 기사 간 코사인 유사도 계산
-  유사도 순 상위 10개 기사 1점씩 부여
-  최종 점수가 가장 높은 기사 → 해당 군집의 대표 기사로 선정
![image](https://user-images.githubusercontent.com/86818727/170232587-c4698f9a-bb50-40fe-85b6-2efa101e006d.png)


:three: **Summarization**   
-  추출 요약(TextRank)과 생성 요약(KoBART) 성능 비교 후 후자 선정
-  AI Hub 추가 데이터를 활용한 Fine-Tuning → KoBART+ 모델 생성
-  3분할 된 문단별 하나의 요약문 생성 → 기사별 3개의 요약문 도출
  -  KoBART : 약 40GB의 한국어 텍스트 데이터를 학습한 Encoder-Decoder 형태의 모델

![image](https://user-images.githubusercontent.com/86818727/170232633-f993a2c0-51cc-44bd-af7f-989356854208.png)
-  TextRank 기반 명사 키워드 추출
-  주요 단어 상위 4개를 해시태그로 설정
-  단어 가중치 값 정규화 → WordCloud의 단어 크기로 설정
  -  단어 가중치: 각 기사의 관심 수

:four: **Service Implementation** 
![image](https://user-images.githubusercontent.com/86818727/170232679-420c3662-9ce0-4083-b2f7-718f8a9af785.png)

➀ 섹션 / 회사별 카드뉴스 ➁ 금주의 키워드 ➂ 오늘의 이슈

  
:arrow_forward: **Project Summary**   
-  축약된 정보 습득을 통한 사용자의 시간 절약 및 검색 효율성 증진
-  키워드 페이지를 활용한 연관 기사 탐색 용이
-  관심 기업 및 카테고리별 트렌드 파악

→  기업 경영진 맞춤형 의사 결정 지원 도구 제공
