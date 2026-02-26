from select import select

from flask import Blueprint, request, flash, redirect, url_for, render_template
from flask_login import login_user, logout_user, login_required, current_user

from app import User
from extensions import login_manager,db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('auth.login'))

        user = db.session.execute(select(User).filter_by(username=username)).scalar()
        # 验证密码是否一致
        if user is not None and user.validate_password(password):
            login_user(user)  # 登入用户
            flash('Login success.')
            return redirect(url_for('main.index'))  # 重定向到主页

        flash('Invalid username or password.')  # 如果验证失败，显示错误消息
        return redirect(url_for('auth.login'))  # 重定向回登录页面

    return render_template('login.html')

@auth_bp.route('/logout')
@login_required  # 用于视图保护，后面会详细介绍
def logout():
    logout_user()  # 登出用户
    flash('Goodbye.')
    return redirect(url_for('main.index'))  # 重定向回首页


# 修改用户的名字
@auth_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form.get('name')

        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('auth.settings'))

        current_user.name = name  # 更新当前用户的名字
        # current_user 会返回当前登录用户的数据库记录对象
        # 等同于下面的用法
        # user = db.session.get(User, current_user.id)
        # user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('main.index'))

    return render_template('settings.html')
