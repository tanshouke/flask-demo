from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
  pass # 语法占位	无操作，仅保持结构完整

# db实例
db = SQLAlchemy(model_class=Base)

# 实例化扩展类 管理登录状态
login_manager = LoginManager()

# 登录拦截
# 果未登录的用户访问对应的 URL，Flask-Login 会把用户重定向到登录页面，并显示一个错误提示。为了让这个重定向操作正确执行，我们还需要把 login_manager.login_view 的值设为我们程序的登录视图端点（函数名）
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数，接受用户 ID 作为参数
    from watchlist.models import User
    user = db.session.get(User, int(user_id))  # 用 ID 作为 User 模型的主键查询对应的用户
    return user  # 返回用户对象