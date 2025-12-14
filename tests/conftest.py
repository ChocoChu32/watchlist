import pytest

from watchlist import create_app
from watchlist.extensions import db
from watchlist.models import Movie, User


@pytest.fixture
def app():
    # 使用测试配置创建程序实例
    app = create_app(config_name="testing")
    # 创建程序上下文
    with app.app_context():
        # 创建数据库和表
        db.create_all()
        # 创建测试数据，一个用户，一个电影条目
        user = User(name="Test", username="test")
        user.set_password("123")
        movie = Movie(title="Test Movie Title", year="2019")
        # 使用 add_all() 方法一次添加多个模型类实例，传入列表
        db.session.add_all([user, movie])
        db.session.commit()

        yield app

        db.session.remove()  # 清除数据库会话
        db.drop_all()  # 删除数据库表


@pytest.fixture
def client(app):  # 创建测试客户端
    return app.test_client()


@pytest.fixture
def runner(app):  # 创建测试命令运行器
    return app.test_cli_runner()


@pytest.fixture
def login(client):  # 辅助方法，用于登入用户
    def _login(username="test", password="123"):
        client.post(
            "/login",
            data=dict(username=username, password=password),
            follow_redirects=True,
        )

    return _login
