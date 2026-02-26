from select import select

from flask import Blueprint, request, flash, redirect, url_for, render_template, current_app
from flask_login import login_required, current_user

from watchlist.extensions import db
# 注册蓝本，对路由分组
from watchlist.models import Movie, User

main_bp = Blueprint('main', __name__)


@main_bp.route('/',methods=['GET','POST']) # 表示同时接受 GET 和 POST 请求。
def index():
    current_app.logger.debug('11111111111111111111111111 Visited index page')
    if request.method=='POST':
        if not current_user.is_authenticated:  # 如果当前用户未认证
            return redirect(url_for('main.index'))  # 重定向到主页
        title=request.form.get('title').strip()
        year=request.form.get('year').strip()
        if not title or not year or len(year)>4 or len(title)>60:
            flash('Invalid input.')
            return redirect(url_for('main.index'))
        movie=Movie(title=title,year=year)
        db.session.add(movie)
        db.session.commit()
        flash('Item created.')
        return redirect(url_for('main.index'))
    movies=  Movie.query.all()
    return render_template('index.html', movies=movies)


@main_bp.route('/add_user/<name>/<username>/<password>')
def add_user(name,username,password):
    new_user = User(name=name,username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return '用户添加成功!'

@main_bp.route('/delete_user/<id>')
def delete_user(id):
    user = User.query.filter_by(id=id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return '用户删除成功!'
    return '用户不存在!'


@main_bp.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required  # 登录保护
def edit(movie_id):
    movie = db.get_or_404(Movie, movie_id)
    print('movie: ',movie.title,movie.year)
    if request.method == 'POST':  # 处理编辑表单的提交请求
        title = request.form.get('title').strip()
        year = request.form.get('year').strip()

        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('main.edit', movie_id=movie_id))  # 重定向回对应的编辑页面

        movie.title = title  # 更新标题
        movie.year = year  # 更新年份
        db.session.commit()  # 提交数据库会话
        flash('Item updated.')
        return redirect(url_for('main.index'))  # 重定向回主页

    return render_template('edit.html', movie=movie)  # 传入被编辑的电影记录

@main_bp.route('/movie/delete/<int:movie_id>', methods=['POST'])  # 限定只接受 POST 请求
@login_required  # 登录保护
def delete(movie_id):
    movie = db.get_or_404(Movie, movie_id)  # 获取电影记录
    db.session.delete(movie)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash('Item deleted.')
    return redirect(url_for('main.index'))  # 重定向回主页

@main_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('main.settings'))

        user = db.session.get(User, current_user.id)
        user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('main.index'))

    return render_template('settings.html')