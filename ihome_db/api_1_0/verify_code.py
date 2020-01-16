
# 导入蓝图
from . import api

from ihome_db.utils.captcha.captcha import Captcha
from ihome_db import redis_store
from ihome_db import constant

from flask import current_app, jsonify, make_response
from ihome_db.utils.response_code import RET


# RESTful api
# GET 127.0.0.1/api/v1.0/image_code/<image_code_id>

@api.route("/image_code/<image_code_id>")    # 使用默认的转换器
def get_image_code(image_code_id):
    """
    获取图片验证码
    :param: image_code_id, 图片验证码编号
    :return: 正常情况：验证码图片   异常： 返回json
    """

    # 获取参数
    # 校验参数

    # 业务逻辑处理：
    # 生成验证码图片
    # 名字  真实文本  图片数据
    captcha = Captcha.instance()
    name, text, image_data = captcha.generate_captcha()

    print("text", text)
    print("image_code_id", image_code_id)

    # 将验证码编号和真实值保存到redis中
    # 存储： image_code_id   text  有效期
    # redis 数据类型： string hash list set zet
    # 使用hash能实现数据的存储，但不便于维护
    # image_code(key) : {image_code_id:test(file:value), image_code_id:test(file:value)....}
    # 使用string 类型进行单条存储和维护
    # image_code_%s(%image_code_id): text

    # redis_store.set("image_code_%s" %image_code_id, text)
    # redis_store.expires("image_code_%s" %image_code_id, constant.IMAGE_CODE_REDIS_EXPIRES)
    #               记录名                             有效期                          记录值
    try:
        redis_store.setex("image_code_%s" %image_code_id, constant.IMAGE_CODE_REDIS_EXPIRES, text)
    except Exception as e:
        # 记录日志
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg="save image code id failed")

    # 返回图片
    resp = make_response(image_data)
    resp.headers["Content-Type"] = "image/jpg"

    return resp
