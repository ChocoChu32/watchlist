import unittest

from watchlist import create_app
from watchlist.extensions import db
from watchlist.models import Movie, User


class WatchlistTestCase(unittest.TestCase):
    def setUp(self):
        # 使用测试配置创建程序实例
        self.app = create_app(config_name="testing")
        # 创建程序上下文
        self.context = self.app.app_context()
        # 激活上下文
        self.context.push()

        # 创建数据库和表
        db.create_all()
        # 创建测试数据，一个用户，一个电影条目
        user = User(name="Test", username="test")
        user.set_password("123")
        movie = Movie(title="Test Movie Title", year="2019")
        # 使用 add_all() 方法一次添加多个模型类实例，传入列表
        db.session.add_all([user, movie])
        db.session.commit()

        self.client = self.app.test_client()  # 创建测试客户端
        self.runner = self.app.test_cli_runner()  # 创建测试命令运行器

    def tearDown(self):
        db.session.remove()  # 清除数据库会话
        db.drop_all()  # 删除数据库表
        self.context.pop()  # 清除上下文

    # 测试程序实例是否存在
    def test_app_exist(self):
        self.assertIsNotNone(self.app)

    # 测试程序是否处于测试模式
    def test_app_is_testing(self):
        self.assertTrue(self.app.config["TESTING"])

    # 测试 404 页面
    def test_404_page(self):
        response = self.client.get("/nothing")  # 传入目标 URL
        data = response.get_data(as_text=True)
        self.assertIn("Not Found - 404", data)
        self.assertIn("返回主页", data)
        self.assertEqual(response.status_code, 404)  # 判断响应状态码

    # 测试主页
    def test_index_page(self):
        response = self.client.get("/")
        data = response.get_data(as_text=True)
        self.assertIn("Test 的观影清单", data)
        self.assertIn("Test Movie Title", data)
        self.assertEqual(response.status_code, 200)

    # 辅助方法，用于登入用户
    def login(self):
        self.client.post(
            "/login", data=dict(username="test", password="123"), follow_redirects=True
        )

    # 测试创建条目
    def test_create_item(self):
        self.login()

        # 测试创建条目操作
        response = self.client.post(
            "/", data=dict(title="New Movie", year="2019"), follow_redirects=True
        )
        data = response.get_data(as_text=True)
        self.assertIn("添加成功。", data)
        self.assertIn("New Movie", data)

        # 测试创建条目操作，但电影标题为空
        response = self.client.post(
            "/", data=dict(title="", year="2019"), follow_redirects=True
        )
        data = response.get_data(as_text=True)
        self.assertNotIn("更新成功。", data)
        self.assertIn("输入无效。", data)

        # 测试创建条目操作，但电影年份为空
        response = self.client.post(
            "/", data=dict(title="New Movie", year=""), follow_redirects=True
        )
        data = response.get_data(as_text=True)
        self.assertNotIn("更新成功。", data)
        self.assertIn("输入无效。", data)

    # 测试更新条目
    def test_update_item(self):
        self.login()

        # 测试更新页面
        response = self.client.get("/movie/edit/1")
        data = response.get_data(as_text=True)
        self.assertIn("编辑", data)
        self.assertIn("Test Movie Title", data)
        self.assertIn("2019", data)

        # 测试更新条目操作
        response = self.client.post(
            "/movie/edit/1",
            data=dict(title="New Movie Edited", year="2019"),
            follow_redirects=True,
        )
        data = response.get_data(as_text=True)
        self.assertIn("更新成功。", data)
        self.assertIn("New Movie Edited", data)

        # 测试更新条目操作，但电影标题为空
        response = self.client.post(
            "/movie/edit/1", data=dict(title="", year="2019"), follow_redirects=True
        )
        data = response.get_data(as_text=True)
        self.assertNotIn("更新成功。", data)
        self.assertIn("输入无效。", data)

        # 测试更新条目操作，但电影年份为空
        response = self.client.post(
            "/movie/edit/1",
            data=dict(title="New Movie Edited Again", year=""),
            follow_redirects=True,
        )
        data = response.get_data(as_text=True)
        self.assertNotIn("更新成功。", data)
        self.assertNotIn("New Movie Edited Again", data)
        self.assertIn("输入无效。", data)

    # 测试删除条目
    def test_delete_item(self):
        self.login()

        response = self.client.post("/movie/delete/1", follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn("删除成功。", data)
        self.assertNotIn("Test Movie Title", data)

    # 测试登录保护
    def test_login_protect(self):
        response = self.client.get("/")
        data = response.get_data(as_text=True)
        self.assertNotIn("设置", data)
        self.assertNotIn("登出", data)
        self.assertNotIn('<form method="post">', data)
        self.assertNotIn("编辑", data)
        self.assertNotIn("删除", data)

    # 测试登录
    def test_login(self):
        response = self.client.post(
            "/login", data=dict(username="test", password="123"), follow_redirects=True
        )
        data = response.get_data(as_text=True)
        self.assertIn("登陆成功。", data)
        self.assertIn("设置", data)
        self.assertIn("登出", data)
        self.assertIn('<form method="post">', data)
        self.assertIn("编辑", data)
        self.assertIn("删除", data)

        # 测试使用错误的用户名登录
        response = self.client.post(
            "/login", data=dict(username="wrong", password="123"), follow_redirects=True
        )
        data = response.get_data(as_text=True)
        self.assertNotIn("登陆成功。", data)
        self.assertIn("用户名或密码错误。", data)

        # 测试使用错误的密码登录
        response = self.client.post(
            "/login", data=dict(username="test", password="456"), follow_redirects=True
        )
        data = response.get_data(as_text=True)
        self.assertNotIn("登陆成功。", data)
        self.assertIn("用户名或密码错误。", data)

        # 测试使用空用户名登录
        response = self.client.post(
            "/login", data=dict(username="", password="123"), follow_redirects=True
        )
        data = response.get_data(as_text=True)
        self.assertNotIn("登陆成功。", data)
        self.assertIn("输入无效。", data)

        # 测试使用空密码登录
        response = self.client.post(
            "/login", data=dict(username="test", password=""), follow_redirects=True
        )
        data = response.get_data(as_text=True)
        self.assertNotIn("登陆成功。", data)
        self.assertIn("输入无效。", data)

    # 测试登出
    def test_logout(self):
        self.login()

        response = self.client.get("/logout", follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn("再见。", data)
        self.assertNotIn("设置", data)
        self.assertNotIn("登出", data)
        self.assertNotIn('<form method="post">', data)
        self.assertNotIn("编辑", data)
        self.assertNotIn("删除", data)

    # 测试设置
    def test_settings(self):
        self.login()

        # 测试设置页面
        response = self.client.get("/settings")
        data = response.get_data(as_text=True)
        self.assertIn("设置", data)
        self.assertIn("姓名", data)

        # 测试更新设置
        response = self.client.post(
            "/settings",
            data=dict(
                name="Choco Chu",
            ),
            follow_redirects=True,
        )
        data = response.get_data(as_text=True)
        self.assertIn("姓名更新成功。", data)
        self.assertIn("Choco Chu", data)

        # 测试更新设置，名称为空
        response = self.client.post(
            "/settings",
            data=dict(
                name="",
            ),
            follow_redirects=True,
        )
        data = response.get_data(as_text=True)
        self.assertNotIn("姓名更新成功。", data)
        self.assertIn("输入无效。", data)

    # 测试初始化数据库
    def test_initdb_command(self):
        result = self.runner.invoke(args=["init-db"])
        self.assertIn("Initialized database.", result.output)

    # 测试虚拟数据
    def test_forge_command(self):
        result = self.runner.invoke(args=["forge"])
        self.assertIn("Done.", result.output)
        self.assertNotEqual(Movie.query.count(), 0)

    # 测试生成管理员账户
    def test_admin_command(self):
        db.drop_all()
        db.create_all()
        # 使用 args 参数给出完整的命令参数列表
        result = self.runner.invoke(
            args=["admin", "--username", "choco", "--password", "123"]
        )
        self.assertIn("Creating user...", result.output)
        self.assertIn("Done.", result.output)
        self.assertEqual(User.query.count(), 1)
        self.assertEqual(User.query.first().username, "choco")
        self.assertTrue(User.query.first().validate_password("123"))

    # 测试更新管理员账户
    def test_admin_command_update(self):
        result = self.runner.invoke(
            args=["admin", "--username", "chu", "--password", "456"]
        )
        self.assertIn("Updating user...", result.output)
        self.assertIn("Done.", result.output)
        self.assertEqual(User.query.count(), 1)
        self.assertEqual(User.query.first().username, "chu")
        self.assertTrue(User.query.first().validate_password("456"))


if __name__ == "__main__":
    unittest.main()
