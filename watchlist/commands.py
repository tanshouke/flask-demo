import click
from watchlist.extensions import db
from watchlist.models import User



def register_commands(app):
    @app.cli.command('init-db')  # 注册为命令，传入自定义命令名 flask init-db
    @click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
    def init_database(drop):
        """Initialize the database."""
        if drop:  # 判断是否输入了选项 flask init-db --drop
            db.drop_all()
        db.create_all()
        click.echo('Initialized database.')  # 输出提示信息

    # 命令行进行账户管理
    @app.cli.command()
    @click.option('--name', prompt=True, help='The name.')
    @click.option('--username', prompt=True, help='The username used to login.')
    @click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True,
                  help='The password used to login.')
    def admin(name, username, password):
        user = User.query.filter_by(username=username).first()
        if user is not None:
            click.echo('Updating user...')
            user.username = username
            user.set_password(password)  # 设置密码
        else:
            click.echo('Creating user...')
            user = User(username=username, name=name)
            user.set_password(password)  # 设置密码
            db.session.add(user)

        db.session.commit()  # 提交数据库会话
        click.echo('Done.')
