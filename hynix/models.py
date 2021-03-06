from hynix import db


class News(db.Model):   # list1용 DB(뉴스 기사 본문 관련)
    __tablename__ = 'news_content'

    news_id = db.Column(db.Integer, primary_key=True)           # 자동 증가하는 index
    press = db.Column(db.String(20), nullable=False)            # 언론사
    press_url = db.Column(db.String(50), nullable=False)        # 언론사 url
    logo_url = db.Column(db.String(200), nullable=False)        # 언론사 로고 url
    date = db.Column(db.String(40), nullable=False)             # 날짜
    title = db.Column(db.String, nullable=False)                # 기사명
    section = db.Column(db.String(10), nullable=False)          # 섹션
    content = db.Column(db.String(20), nullable=False)          # 기사 본문
    url = db.Column(db.String(20), nullable=False)              # 기사 본문 url
    name = db.Column(db.String(20), nullable=False)             # 회사명 8
    types = db.Column(db.String(10), nullable=False)            # 회사 종류 9
    interest_cnt = db.Column(db.Integer, nullable=False)        # 관심 수
    com_cnt = db.Column(db.Integer, nullable=False)             # 댓글 수
    img_url = db.Column(db.String(200), nullable=False)         # 첫번째 이미지 url
    summaries1 = db.Column(db.String, nullable=False)            # 요약문1
    summaries2 = db.Column(db.String, nullable=True)            # 요약문2
    summaries3 = db.Column(db.String, nullable=True)            # 요약문3
    hash1 = db.Column(db.String(10), nullable=False)            # 해시태그1
    hash2 = db.Column(db.String(10), nullable=False)            # 해시태그2
    hash3 = db.Column(db.String(10), nullable=False)            # 해시태그3
    hash4 = db.Column(db.String(10), nullable=False)            # 해시태그4

    def __init__(self, press, press_url, logo_url, date, title, section, content, url,
                 name, types, interest_cnt, com_cnt, img_url, summaries1, summaries2, summaries3,
                 hash1, hash2, hash3, hash4):
        self.press = press
        self.press_url = press_url
        self.logo_url = logo_url
        self.date = date
        self.title = title
        self.section = section
        self.content = content
        self.url = url
        self.name = name
        self.types = types
        self.interest_cnt = interest_cnt
        self.com_cnt = com_cnt
        self.img_url = img_url
        self.summaries1 = summaries1
        self.summaries2 = summaries2
        self.summaries3 = summaries3
        self.hash1 = hash1
        self.hash2 = hash2
        self.hash3 = hash3
        self.hash4 = hash4

    @property
    def serialize(self):
        return {
            'press': self.press,
            'press_url': self.press_url,
            'logo_url': self.logo_url,
            'date': self.date,
            'title': self.title,
            'section': self.section,
            'content': self.content,
            'url': self.url,
            'name': self.name,
            'types': self.types,
            'interest_cnt': self.interest_cnt,
            'com_cnt': self.com_cnt,
            'img_url': self.img_url,
            'summaries': [
                {
                    'summaries1': self.summaries1
                },
                {
                    'summaries2': self.summaries2
                },
                {
                    'summaries3': self.summaries3
                }
            ],
            'hashtag': [
                {
                    'hash1': self.hash1
                },
                {
                    'hash2': self.hash2
                },
                {
                    'hash3': self.hash3
                },
                {
                    'hash4': self.hash4
                }
            ]
        }

    @property
    def signify(self):  # 키워드 페이지 list1 return
        return {
            'summaries': [                  # 세줄 요약
                {
                    'summaries1': self.summaries1
                },
                {
                    'summaries2': self.summaries2
                },
                {
                    'summaries3': self.summaries3
                }
            ],
            'img_url': self.img_url,        # 첫번째 이미지 url
            'url': self.url,                # 기사본문 url
            'title': self.title,            # 기사 제목
            'hashtag': [
                {
                    'hash1': self.hash1
                },
                {
                    'hash2': self.hash2
                },
                {
                    'hash3': self.hash3
                },
                {
                    'hash4': self.hash4
                }
            ]
        }

    @property
    def hash_count(self):   # list2
        return {    # 각 키워드 페이지(섹션/기업)별 키워드 수 count 하기 위해 키워드만 return
            'hash1': self.hash1,
            'hash2': self.hash2,
            'hash3': self.hash3,
            'hash4': self.hash4
        }


class Hash(db.Model):   # list2용 DB(해시태그 - 금주의 키워드 관련)
    __tablename__ = 'news_hashtag'

    hash_id = db.Column(db.Integer, primary_key=True)        # 자동 증가하는 index
    hashtag = db.Column(db.String(10), nullable=False)       # 해시태그
    weight = db.Column(db.Float, nullable=False)             # 정규가중치
    
    def __init__(self, hashtag, weight):
        self.hashtag = hashtag
        self.weight = weight

    @property
    def serialize(self):    # all/all list2 해시태그
        return {
            'weight': round(self.weight, 2),
            'hashtag': self.hashtag
        }