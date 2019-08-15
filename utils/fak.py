#! -*-coding:utf8-*-
from faker import Faker
import pandas as pd
import pymysql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,relationship



class Faker_t:
    def __init__(self):
        # 选择中文
        self.fake = Faker("zh_CN")

    def get_name(self):
        return self.fake.name()

    def get_phone_number(self):
        return self.fake.phone_number()

    def get_id(self):
        return self.fake.ssn()

    def get_gender(self):
        return self.fake.profile()["sex"]

    def get_age(self):
        return 2019 - int(self.fake.profile()["ssn"][6:10])

    # def get_per(self):
    #     return self.fake.



if __name__ == '__main__':
    # f = Faker_t()
    # print(f.get_name())
    # print(f.get_phone_number())
    # print(f.get_id())
    # print(f.get_gender())
    # print(f.get_per())
    d = pd.date_range(start='5/1/2019 09:00:00', periods=26, freq='30min')
    for item in d:
        print(item, type(item))
        print(pd.date_range(start=item, periods=2, freq='30min')[1])
