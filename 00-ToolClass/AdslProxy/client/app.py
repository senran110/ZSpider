"""
@file:app.py
@time:2019/9/18-15:01
"""
from flask import Flask, jsonify, request, g

from redisDB import RedisClient

app = Flask(__name__)


def get_conn():
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()

    return g.redis


@app.route("/", methods=["GET"])
def index():
    """
    获取拨号ip并放入数据库
    :return:
    """
    return "welcome!!!"


#
# @app.route("/proxyip", methods=["POST"])
# def add():
#     """
#     获取拨号ip并放入数据库
#     :return:
#     """
#     # data = request.get_json()
#     # for k, v in data.items():
#     #     pass
#     return jsonify(code=0, msg="success")
#
#
# #
# @app.route("/proxyip", methods=['DELETE'])
# def remove():
#     """
#     移除拨号ip
#     :return:
#     """
#     return jsonify(code=0, msg="success")


#
@app.route("/proxyip", methods=["GET"])
def get():
    """
    从redis获取ip
    :return:
    """
    conn = get_conn()
    return conn.random()


@app.errorhandler(500)
def internal_error(error):
    return "", 500


if __name__ == '__main__':
    app.run(host="0.0.0.0")
