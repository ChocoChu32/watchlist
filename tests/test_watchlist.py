from watchlist.extensions import db
from watchlist.models import Movie, User


# 测试程序实例是否存在
def test_app_exist(app):
    assert app is not None


# 测试程序是否处于测试模式
def test_app_is_testing(app):
    assert app.config["TESTING"] is True


# 测试 404 页面
def test_404_page(client):
    response = client.get("/nothing")  # 传入目标 URL
    data = response.get_data(as_text=True)
    assert "Not Found - 404" in data
    assert "返回主页" in data
    assert response.status_code == 404  # 判断响应状态码


# 测试主页
def test_index_page(client):
    response = client.get("/")
    data = response.get_data(as_text=True)
    assert "Test 的观影清单" in data
    assert "Test Movie Title" in data
    assert response.status_code == 200


# 测试创建条目
def test_create_item(client, login):
    login()

    # 测试创建条目操作
    response = client.post(
        "/", data=dict(title="New Movie", year="2019"), follow_redirects=True
    )
    data = response.get_data(as_text=True)
    assert "添加成功。" in data
    assert "New Movie" in data

    # 测试创建条目操作，但电影标题为空
    response = client.post("/", data=dict(title="", year="2019"), follow_redirects=True)
    data = response.get_data(as_text=True)
    assert "更新成功。" not in data
    assert "输入无效。" in data

    # 测试创建条目操作，但电影年份为空
    response = client.post(
        "/", data=dict(title="New Movie", year=""), follow_redirects=True
    )
    data = response.get_data(as_text=True)
    assert "更新成功。" not in data
    assert "输入无效。" in data


# 测试更新条目
def test_update_item(client, login):
    login()

    # 测试更新页面
    response = client.get("/movie/edit/1")
    data = response.get_data(as_text=True)
    assert "编辑" in data
    assert "Test Movie Title" in data
    assert "2019" in data

    # 测试更新条目操作
    response = client.post(
        "/movie/edit/1",
        data=dict(title="New Movie Edited", year="2019"),
        follow_redirects=True,
    )
    data = response.get_data(as_text=True)
    assert "更新成功。" in data
    assert "New Movie Edited" in data

    # 测试更新条目操作，但电影标题为空
    response = client.post(
        "/movie/edit/1", data=dict(title="", year="2019"), follow_redirects=True
    )
    data = response.get_data(as_text=True)
    assert "更新成功。" not in data
    assert "输入无效。" in data

    # 测试更新条目操作，但电影年份为空
    response = client.post(
        "/movie/edit/1",
        data=dict(title="New Movie Edited Again", year=""),
        follow_redirects=True,
    )
    data = response.get_data(as_text=True)
    assert "更新成功。" not in data
    assert "New Movie Edited Again" not in data
    assert "输入无效。" in data


# 测试删除条目
def test_delete_item(client, login):
    login()

    response = client.post("/movie/delete/1", follow_redirects=True)
    data = response.get_data(as_text=True)
    assert "删除成功。" in data
    assert "Test Movie Title" not in data


# 测试登录保护
def test_login_protect(client):
    response = client.get("/")
    data = response.get_data(as_text=True)
    assert "设置" not in data
    assert "登出" not in data
    assert '<form method="post">' not in data
    assert "编辑" not in data
    assert "删除" not in data


# 测试登录
def test_login(client):
    response = client.post(
        "/login", data=dict(username="test", password="123"), follow_redirects=True
    )
    data = response.get_data(as_text=True)
    assert "登陆成功。" in data
    assert "设置" in data
    assert "登出" in data
    assert '<form method="post">' in data
    assert "编辑" in data
    assert "删除" in data

    # 测试使用错误的用户名登录
    response = client.post(
        "/login", data=dict(username="wrong", password="123"), follow_redirects=True
    )
    data = response.get_data(as_text=True)
    assert "登陆成功。" not in data
    assert "用户名或密码错误。" in data

    # 测试使用错误的密码登录
    response = client.post(
        "/login", data=dict(username="test", password="456"), follow_redirects=True
    )
    data = response.get_data(as_text=True)
    assert "登陆成功。" not in data
    assert "用户名或密码错误。" in data

    # 测试使用空用户名登录
    response = client.post(
        "/login", data=dict(username="", password="123"), follow_redirects=True
    )
    data = response.get_data(as_text=True)
    assert "登陆成功。" not in data
    assert "输入无效。" in data

    # 测试使用空密码登录
    response = client.post(
        "/login", data=dict(username="test", password=""), follow_redirects=True
    )
    data = response.get_data(as_text=True)
    assert "登陆成功。" not in data
    assert "输入无效。" in data


# 测试登出
def test_logout(client, login):
    login()

    response = client.get("/logout", follow_redirects=True)
    data = response.get_data(as_text=True)
    assert "再见。" in data
    assert "设置" not in data
    assert "登出" not in data
    assert '<form method="post">' not in data
    assert "编辑" not in data
    assert "删除" not in data


# 测试设置
def test_settings(client, login):
    login()

    # 测试设置页面
    response = client.get("/settings")
    data = response.get_data(as_text=True)
    assert "设置" in data
    assert "姓名" in data

    # 测试更新设置
    response = client.post(
        "/settings",
        data=dict(
            name="Choco Chu",
        ),
        follow_redirects=True,
    )
    data = response.get_data(as_text=True)
    assert "姓名更新成功。" in data
    assert "Choco Chu" in data

    # 测试更新设置，名称为空
    response = client.post(
        "/settings",
        data=dict(
            name="",
        ),
        follow_redirects=True,
    )
    data = response.get_data(as_text=True)
    assert "姓名更新成功。" not in data
    assert "输入无效。" in data


# 测试初始化数据库
def test_initdb_command(runner):
    result = runner.invoke(args=["init-db"])
    assert "Initialized database." in result.output


# 测试虚拟数据
def test_forge_command(runner):
    db.session.remove()
    result = runner.invoke(args=["forge"])
    assert "Done." in result.output
    assert Movie.query.count() != 0


# 测试生成管理员账户
def test_admin_command(runner):
    db.session.remove()
    db.drop_all()
    db.create_all()
    # 使用 args 参数给出完整的命令参数列表
    result = runner.invoke(args=["admin", "--username", "choco", "--password", "123"])
    assert "Creating user..." in result.output
    assert "Done." in result.output
    assert User.query.count() == 1
    assert User.query.first().username == "choco"
    assert User.query.first().validate_password("123")


# 测试更新管理员账户
def test_admin_command_update(runner):
    result = runner.invoke(args=["admin", "--username", "chu", "--password", "456"])
    assert "Updating user..." in result.output
    assert "Done." in result.output
    assert User.query.count() == 1
    assert User.query.first().username == "chu"
    assert User.query.first().validate_password("456")
