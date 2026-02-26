# 初始化数据库
import os

from dotenv import load_dotenv


class BaseConfig:  # 创建配置基类
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    # flash() 函数在内部会把消息存储到 Flask 提供的 session 对象里。session 用来在请求间存储数据，它会把数据签名后存储到浏览器的 Cookie 中，所以我们需要设置签名所需的密钥：
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')

    # mysql配置
    # SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:3306/{os.getenv('DB_NAME')}"
    SQLALCHEMY_TRACK_MODIFICATIONS= False
    SQLALCHEMY_ECHO= True  # 开发时显示SQL语句
    # 连接池配置
    SQLALCHEMY_POOL_SIZE = 20
    SQLALCHEMY_POOL_TIMEOUT = 300
    SQLALCHEMY_POOL_RECYCLE = 3600


class DevelopmentConfig(BaseConfig):  # 开发配置
    SQLALCHEMY_DATABASE_URI =f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:3306/{os.getenv('DB_NAME')}"
    SQLALCHEMY_POOL_RECYCLE = 3600

class TestingConfig(BaseConfig):  # 测试配置
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:3306/{os.getenv('DB_NAME')}"
    SQLALCHEMY_POOL_RECYCLE = 600


class ProductionConfig(BaseConfig):  # 生产配置
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:3306/{os.getenv('DB_NAME')}"
    SQLALCHEMY_POOL_RECYCLE = 1800

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}

