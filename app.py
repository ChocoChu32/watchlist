from flask import Flask, render_template

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

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", name=name, movies=movies)
