from pathlib import Path

import click
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////" + str(
    Path(app.root_path) / "data.db"
)


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(app, model_class=Base)


class User(db.Model):
    __tablename__ = "user"  # 定义表名称
    id: Mapped[int] = mapped_column(primary_key=True)  # 主键
    name: Mapped[str] = mapped_column(String(20))  # 名字


class Movie(db.Model):  # 表名将会是 movie
    __tablename__ = "movie"
    id: Mapped[int] = mapped_column(primary_key=True)  # 主键
    title: Mapped[str] = mapped_column(String(60))  # 电影标题
    year: Mapped[str] = mapped_column(String(4))  # 电影年份


@app.route("/")
def index():
    user = db.session.execute(select(User)).scalar()  # 读取用户记录
    movies = db.session.execute(select(Movie)).scalars().all()  # 读取所有电影记录
    return render_template("index.html", user=user, movies=movies)


@app.cli.command("init-db")  # 注册为命令，传入自定义命令名
@click.option("--drop", is_flag=True, help="Create after drop.")  # 设置选项
def init_database(drop):
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

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m["title"], year=m["year"])
        db.session.add(movie)

    db.session.commit()
    click.echo("Done.")
