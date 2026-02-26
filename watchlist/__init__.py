from flask import Flask
from sqlalchemy import select
from watchlist.blueprints.main import main_bp
from watchlist.blueprints.auth import auth_bp
from watchlist.commands import register_commands
from watchlist.extensions import login_manager, db
from watchlist.errors import register_errors
from watchlist.blueprints.main import main_bp
from watchlist.extensions import db
from watchlist.models import User



# 启动程序 工厂模式
from watchlist.settings import config


def create_app(config_name='development'):
    app = Flask(__name__)  # 传入存储当前模块名称的特殊变量 __name__
    # 将配置更新到程序中
    app.config.from_object(config[config_name])

    print("1111111 config load: ",app.config.get('SQLALCHEMY_DATABASE_URI'),app.config.get('SQLALCHEMY_POOL_RECYCLE'))

    # 注册异常处理
    register_errors(app)

    # 注册命令行
    register_commands(app)

    # 注册蓝本
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    # db 初始化扩展
    db.init_app(app)

    login_manager.init_app(app)

    # 上下文处理函数
    @app.context_processor
    def inject_user():
        user = db.session.execute(select(User)).scalar()
        return dict(user=user)
    return app
