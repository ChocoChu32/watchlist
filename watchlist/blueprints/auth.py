from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from sqlalchemy import select

from watchlist.extensions import db
from watchlist.models import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("输入无效。")
            return redirect(url_for("auth.login"))  # 重定向回登录页面

        user = db.session.execute(select(User).filter_by(username=username)).scalar()

        if user is not None and user.validate_password(password):  # 验证密码是否一致
            login_user(user)  # 登入用户
            flash("登陆成功。")
            return redirect(url_for("main.index"))  # 重定向到主页

        flash("用户名或密码错误。")  # 如果验证失败，显示错误消息
        return redirect(url_for("auth.login"))  # 重定向回登录页面

    return render_template("login.html")


@auth_bp.route("/logout")
@login_required  # 用于视图保护
def logout():
    logout_user()  # 登出用户
    flash("再见。")
    return redirect(url_for("main.index"))  # 重定向到首页
