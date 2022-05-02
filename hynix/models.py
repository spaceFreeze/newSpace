from hynix import db


class News(db.Model):   # list1용 DB(뉴스기사 본문 관련)
    __tablename__ = 'news_content'

    news_id = db.Column(db.Integer, primary_key=True)           # 자동 증가하는 index
    press = db.Column(db.String(20), nullable=False)            # 언론사
    press_url = db.Column(db.String(50), nullable=False)        # 언론사 url
    logo_url = db.Column(db.String(200), nullable=False)        # 언론사 로고 url
    date = db.Column(db.String(40), nullable=False)             # 날짜
    title = db.Column(db.String, nullable=False)                # 기사명
    section = db.Column(db.String(10), nullable=False)          # 섹션
    content = db.Column(db.String(20), nullable=False)          # 기사본문
    url = db.Column(db.String(20), nullable=False)              # 기사본문 url
    name = db.Column(db.String(20), nullable=False)             # 회사명
    types = db.Column(db.String(10), nullable=False)            # 회사종류
    like_cnt = db.Column(db.Integer, nullable=False)            # 좋아요 10
    recom_react_cnt = db.Column(db.Integer, nullable=False)     # 추천반응수 11
    com_cnt = db.Column(db.Integer, nullable=False)             # 댓글 수 12
    img_url = db.Column(db.String(200), nullable=False)         # 첫번째 이미지 url
    summaries = db.Column(db.String, nullable=False)            # 요약문
    hash1 = db.Column(db.String(10), nullable=False)            # 해시태그1
    hash2 = db.Column(db.String(10), nullable=False)            # 해시태그2
    hash3 = db.Column(db.String(10), nullable=False)            # 해시태그3
    hash4 = db.Column(db.String(10), nullable=False)            # 해시태그4

    def __init__(self, press, press_url, logo_url, date, title, section, content, url,
                 name, types, like_cnt, recom_react_cnt, com_cnt, img_url, summaries,
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
        self.like_cnt = like_cnt
        self.recom_react_cnt = recom_react_cnt
        self.com_cnt = com_cnt
        self.img_url = img_url
        self.summaries = summaries
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
            'like_cnt': self.like_cnt,
            'recom_react_cnt': self.recom_react_cnt,
            'com_cnt': self.com_cnt,
            'img_url': self.img_url,
            'summaries': self.summaries,
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
            'summaries': self.summaries,    # 한줄 요약
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

        # 밑에는 무시--------------------------------------------------------------------------
        # 'date': base64.b64encode(self.date.encode("UTF-8")).decode("UTF-8"),
        # 'title': base64.b64encode(self.title.encode("UTF-8")).decode("UTF-8"),
        # 'section': base64.b64encode(self.section.encode("UTF-8")).decode("UTF-8"),
        # 'contents': base64.b64encode(self.contents.encode("UTF-8")).decode("UTF-8"),
        # 'url': base64.b64encode(self.url.encode("UTF-8")).decode("UTF-8"),
        # 'name': base64.b64encode(self.name.encode("UTF-8")).decode("UTF-8"),
        # 'types': base64.b64encode(self.types.encode("UTF-8")).decode("UTF-8"),

        # return {
        #     'date': self.date, 'title': self.title,
        #     'section': self.section, 'contents': self.contents, 'url': self.url,
        #     'name': self.name, 'types': self.types, 'rec_cnt': self.rec_cnt,
        #     'good_cnt': self.good_cnt, 'smile_cnt': self.smile_cnt, 'sad_cnt': self.sad_cnt,
        #     'angry_cnt': self.angry_cnt, 'next_cnt': self.next_cnt, 'react_cnt': self.react_cnt,
        #     'recom_react_cnt': self.recom_react_cnt, 'com_cnt': self.com_cnt
        # }

    # def as_dict(self):
    #     return {x.name: getattr(self, x.name) for x in self.__table__.columns}

    # @property
    # def json(self):
    #     return to_json(self, self.__class__)

    # @property
    # def columns_li(self):
    #     return ['date', 'title', 'section', 'contents', 'url', 'name', 'types',
    #             'rec_cnt', 'good_cnt', 'smile_cnt', 'sad_cnt', 'angry_cnt',
    #             'next_cnt', 'react_cnt', 'recom_react_cnt', 'com_cnt']

    # def as_dict(self):
    #     return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    # def serialize(self):
    #     d = Serializer.serialize(self)
    #     return d

# class Serializer(object):
#     def serialize(self):
#         return {c: getattr(self, c) for c in inspect(self).attrs.keys()}
#
#     @staticmethod
#     def serialize_list(l):
#         return [m.serialize() for m in l]


# def to_json(inst, cls):
#     convert = dict()
#     d = dict()
#     for c in cls.__table__.columns:
#         v = getattr(inst, c.name)
#         if c.type in convert.keys() and v is not None:
#             try:
#                 d[c.name] = convert[c.type](v)
#             except:
#                 d[c.name] = "Error:  Failed to covert using ", str(convert[c.type])
#         elif v is None:
#             d[c.name] = str()
#         else:
#             d[c.name] = v
#     return json.dumps(d)

# class Summary(db.Model):
#     __tablename__ = 'news_summary'
