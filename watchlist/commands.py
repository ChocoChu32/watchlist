import click
from sqlalchemy import select

from watchlist.extensions import db
from watchlist.models import Movie, User


def register_commands(app):
    @app.cli.command("init-db")  # 注册为命令，传入自定义命令名
    @click.option("--drop", is_flag=True, help="Create after drop.")  # 设置选项
    def initdb(drop):
        """Initialize the database."""
        if drop:  # 判断是否输入了选项
            db.drop_all()
        db.create_all()
        click.echo("Initialized database.")  # 输出提示信息

    @app.cli.command()
    def forge():
        """Generate fake data."""
        db.drop_all()
        db.create_all()

        name = "Choco Chu"
        movies = [
            {"title": "肖申克的救赎", "year": "1994"},
            {"title": "霸王别姬", "year": "1993"},
            {"title": "泰坦尼克号", "year": "1997"},
            {"title": "阿甘正传", "year": "1994"},
            {"title": "千与千寻", "year": "2001"},
            {"title": "美丽人生", "year": "1997"},
            {"title": "星际穿越", "year": "2014"},
            {"title": "这个杀手不太冷", "year": "1994"},
            {"title": "盗梦空间", "year": "2010"},
            {"title": "楚门的世界", "year": "1998"},
        ]

        user = User(name=name, username="admin")
        user.set_password("123456")
        db.session.add(user)
        for m in movies:
            movie = Movie(title=m["title"], year=m["year"])
            db.session.add(movie)

        db.session.commit()
        click.echo("Done.")

    @app.cli.command()
    @click.option("--username", prompt=True, help="The username used to login.")
    @click.option(
        "--password",
        prompt=True,
        hide_input=True,
        confirmation_prompt=True,
        help="The password used to login.",
    )
    def admin(username, password):
        """Create user."""
        db.create_all()

        user = db.session.execute(select(User)).scalar()
        if user is not None:
            click.echo("Updating user...")
            user.username = username
            user.set_password(password)  # 设置密码
        else:
            click.echo("Creating user...")
            user = User(username=username, name="Admin")
            user.set_password(password)  # 设置密码
            db.session.add(user)

        db.session.commit()  # 提交数据库会话
        click.echo("Done.")
