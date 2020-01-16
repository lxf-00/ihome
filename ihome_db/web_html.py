# 定义提供静态文件的蓝图

from flask import Blueprint, current_app, make_response
from flask_wtf import csrf


html = Blueprint("web", __name__)



# 构建蓝图路径
@html.route("/<re(r'.*'):html_file_name>")
def get_html(html_file_name):
    """提供html文件"""

    # 如果html_file_name 为空表示访问的是主页
    if not html_file_name:
        html_file_name = "index.html"

    # 如果html_file_name 不是favicon.ico
    if html_file_name != "favicon.ico":
        html_file_name = "html/" + html_file_name

    # 生成一个csrf_token 的值
    csrf_token = csrf.generate_csrf()

    # flask 提供的返回静态文件的方法
    resp = make_response(current_app.send_static_file(html_file_name))

    # 设置cookie值
    resp.set_cookie("csrf_token", csrf_token)

    # 返回
    return resp
