from typing import Optional
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from watchlist.extensions import db


class User(db.Model,UserMixin):
    __tablename__ = 'user' # 定义表名称
    id: Mapped[int] = mapped_column(primary_key=True)  # 主键
    name: Mapped[str] = mapped_column(String(20))  # 名字
    username: Mapped[str] = mapped_column(String(20))  # 用户名
    password_hash: Mapped[Optional[str]] = mapped_column(String(255))  # 密码散列值 Optional标记为可选字段 ，Python 版本是 3.10 及以上版本，可以使用管道符号搭配 None 来表示可选 -->  password_hash: Mapped[str | None] = mapped_column(String(128))

    def set_password(self, password):  # 用来设置密码的方法，接受密码作为参数
        self.password_hash = generate_password_hash(password)  # 将生成的密码保持到对应字段

    def validate_password(self, password):  # 用于验证密码的方法，接受密码作为参数
        return check_password_hash(self.password_hash, password)  # 返回布尔值

class Movie(db.Model):  # 表名将会是 movie
    __tablename__ = 'movie'
    id: Mapped[int] = mapped_column(primary_key=True)  # 主键
    title: Mapped[str] = mapped_column(String(60))  # 电影标题
    year: Mapped[str] = mapped_column(String(4))  # 电影年份


