from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import select

from watchlist.extensions import db
from watchlist.models import Movie

main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":  # 判断是否是 POST 请求
        if not current_user.is_authenticated:  # 如果当前用户未认证
            return redirect(url_for("main.index"))  # 重定向回主页
        # 获取表单数据
        title = request.form.get("title")  # 传入表单对应输入字段的标题值
        year = request.form.get("year")
        # 验证数据
        if not title or not year or len(year) != 4 or len(title) > 60:
            flash("输入无效。")  # 显示错误提示
            return redirect(url_for("main.index"))  # 重定向回主页
        # 保存表单数据到数据库
        movie = Movie(title=title, year=year)  # 创建记录
        db.session.add(movie)  # 添加到数据库会话
        db.session.commit()  # 提交数据库会话
        flash("添加成功。")  # 显示成功创建的提示
        return redirect(url_for("main.index"))  # 重定向回主页

    movies = db.session.execute(select(Movie)).scalars().all()  # 读取所有电影记录
    return render_template("index.html", movies=movies)


@main_bp.route("/movie/edit/<int:movie_id>", methods=["GET", "POST"])
@login_required
def edit(movie_id):
    movie = db.get_or_404(Movie, movie_id)

    if request.method == "POST":  # 处理编辑表单的提交请求
        title = request.form.get("title").strip()
        year = request.form.get("year").strip()

        if not title or not year or len(year) != 4 or len(title) > 60:
            flash("输入无效。")
            return redirect(url_for("main.edit", movie_id=movie_id))

        movie.title = title  # 更新标题
        movie.year = year  # 更新年份
        db.session.commit()  # 提交数据库会话
        flash("更新成功。")
        return redirect(url_for("main.index"))  # 重定向到主页

    return render_template("edit.html", movie=movie)  # 传入被编辑的电影记录


@main_bp.route("/movie/delete/<int:movie_id>", methods=["POST"])  # 限定只接受 POST 请求
@login_required
def delete(movie_id):
    movie = db.get_or_404(Movie, movie_id)  # 获取电影记录
    db.session.delete(movie)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash("删除成功。")
    return redirect(url_for("main.index"))  # 重定向到主页


@main_bp.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    if request.method == "POST":
        name = request.form.get("name")

        if not name or len(name) > 20:
            flash("输入无效。")
            return redirect(url_for("main.settings"))

        current_user.name = name  # 更新当前用户的姓名
        db.session.commit()
        flash("姓名更新成功。")
        return redirect(url_for("main.index"))

    return render_template("settings.html")
