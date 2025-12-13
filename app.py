from pathlib import Path

import click
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////" + str(
    Path(app.root_path) / "data.db"
)
app.config["SECRET_KEY"] = "dev"
login_manager = LoginManager(app)  # 实例化扩展类
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数，接受用户 ID 作为参数
    user = db.session.get(
        User, int(user_id)
    )  # 用 ID 作为 User 模型的主键查询对应的用户
    return user  # 返回用户对象


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("无效输入。")
            return redirect(url_for("login"))

        user = db.session.execute(select(User).filter_by(username=username)).scalar()
        # 验证密码是否一致
        if user is not None and user.validate_password(password):
            login_user(user)  # 登入用户
            flash("登陆成功。")
            return redirect(url_for("index"))  # 重定向到主页

        flash("用户名或密码错误。")  # 如果验证失败，显示错误消息
        return redirect(url_for("login"))  # 重定向回登录页面

    return render_template("login.html")


@app.route("/logout")
@login_required  # 用于视图保护
def logout():
    logout_user()  # 登出用户
    flash("再见。")
    return redirect(url_for("index"))  # 重定向回首页


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(app, model_class=Base)


class User(db.Model, UserMixin):
    __tablename__ = "user"  # 定义表名称
    id: Mapped[int] = mapped_column(primary_key=True)  # 主键
    name: Mapped[str] = mapped_column(String(20))  # 姓名
    username: Mapped[str] = mapped_column(String(20))  # 用户名
    password_hash: Mapped[str | None] = mapped_column(String(128))  # 密码散列值

    def set_password(self, password):  # 用来设置密码的方法，接受密码作为参数
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):  # 用于验证密码的方法，接受密码作为参数
        return check_password_hash(self.password_hash, password)


class Movie(db.Model):  # 表名将会是 movie
    __tablename__ = "movie"
    id: Mapped[int] = mapped_column(primary_key=True)  # 主键
    title: Mapped[str] = mapped_column(String(60))  # 电影标题
    year: Mapped[str] = mapped_column(String(4))  # 电影年份


@app.context_processor
def inject_user():
    user = db.session.execute(select(User)).scalar()
    return dict(user=user)  # 需要返回字典，等同于 return {'user': user}


@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(error):  # 接受异常对象作为参数
    return render_template("404.html"), 404  # 返回模板和状态码


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":  # 判断是否是 POST 请求
        if not current_user.is_authenticated:  # 如果当前用户未认证
            return redirect(url_for("index"))  # 重定向到主页
        # 获取表单数据
        title = request.form.get("title")  # 传入表单对应输入字段的 name 值
        year = request.form.get("year")
        # 验证数据
        if not title or not year or len(year) != 4 or len(title) > 60:
            flash("输入无效。")  # 显示错误提示
            return redirect(url_for("index"))  # 重定向回主页
        # 保存表单数据到数据库
        movie = Movie(title=title, year=year)  # 创建记录
        db.session.add(movie)  # 添加到数据库会话
        db.session.commit()  # 提交数据库会话
        flash("添加成功。")  # 显示成功创建的提示
        return redirect(url_for("index"))  # 重定向回主页

    movies = db.session.execute(select(Movie)).scalars().all()  # 读取所有电影记录
    return render_template("index.html", movies=movies)


@app.route("/movie/edit/<int:movie_id>", methods=["GET", "POST"])
@login_required
def edit(movie_id):
    movie = db.get_or_404(Movie, movie_id)

    if request.method == "POST":  # 处理编辑表单的提交请求
        title = request.form.get("title").strip()
        year = request.form.get("year").strip()

        if not title or not year or len(year) != 4 or len(title) > 60:
            flash("输入无效。")
            return redirect(url_for("edit", movie_id=movie_id))

        movie.title = title  # 更新标题
        movie.year = year  # 更新年份
        db.session.commit()  # 提交数据库会话
        flash("更新成功。")
        return redirect(url_for("index"))  # 重定向回主页

    return render_template("edit.html", movie=movie)  # 传入被编辑的电影记录


@app.route("/movie/delete/<int:movie_id>", methods=["POST"])  # 限定只接受 POST 请求
@login_required
def delete(movie_id):
    movie = db.get_or_404(Movie, movie_id)  # 获取电影记录
    db.session.delete(movie)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash("删除成功。")
    return redirect(url_for("index"))  # 重定向回主页


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    if request.method == "POST":
        name = request.form.get("name")

        if not name or len(name) > 20:
            flash("输入无效")
            return redirect(url_for("settings"))

        current_user.name = name  # 更新当前用户的姓名
        db.session.commit()
        flash("姓名更新成功。")
        return redirect(url_for("index"))

    return render_template("settings.html")


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
