# coding: utf-8
import hashlib
import json
import time
import xml.etree.ElementTree as ET
from datetime import datetime

from flask import Flask, jsonify, make_response, request

from read_large_pi import m1

app = Flask(__name__)

with open("pi.json", "r") as f:
    date_digits_d = json.load(f)
# 微信后台的token
token = ""
reply = """
<xml><ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[%s]]></Content>
<FuncFlag>0</FuncFlag></xml>
"""


def reply_text(to_user, from_user, content):
    response = make_response(
        reply % (to_user, from_user, str(int(time.time())), content)
    )
    response.content_type = "application/xml"
    return response


def check_token(data):
    signature = data.get("signature", "")
    timestamp = data.get("timestamp", "")
    nonce = data.get("nonce", "")
    echostr = data.get("echostr", "")
    s = sorted([timestamp, nonce, token])
    # 字典排序
    s = "".join(s)
    if hashlib.sha1(s.encode("utf-8")).hexdigest() == signature:
        return echostr
    return "hello, this is handle view, false"


def parse_xml(xml):
    toUser = xml.find("ToUserName").text
    fromUser = xml.find("FromUserName").text
    msgType = xml.find("MsgType").text
    return toUser, fromUser, msgType


def find_date_in_pi(content):
    # output = date_digits_d[content] if content in date_digits_d.keys() else m1(content)
    output = m1(content)
    if output == -1:
        return "很抱歉，π的前25亿位中未找到你的生日{}".format(content)
    output = str(output)[::-1]
    output_lst = [output[i : i + 4] for i in range(0, len(output), 4)]
    reply_content = ",".join(x[::-1] for x in output_lst[::-1])
    return '你的生日"{}"出现在π的第{}位'.format(content, reply_content)


@app.route("/wx_api", methods=["GET", "POST"])
def wx_find_str_in_pi():
    if request.method == "GET":
        return check_token(request.args)
    elif request.method == "POST":
        xml = ET.fromstring(request.data)
        toUser, fromUser, msgType = parse_xml(xml)
        if msgType == "text":
            content = xml.find("Content").text
            try:
                date_text = datetime.strptime(content, "%Y%m%d")
            except:
                return reply_text(fromUser, toUser, "请输入有效日期，如20201212")
            return reply_text(fromUser, toUser, find_date_in_pi(content))
        elif msgType == "event":
            event = xml.find("Event").text
            if event == "subscribe":
                text_1 = "subscribe123"
                return reply_text(fromUser, toUser, text_1)
        return reply_text(fromUser, toUser, "功能开发ing")
    else:
        return "please use get or post method"


if __name__ == "__main__":
    # 端口自定义
    app.run(host="0.0.0.0", port=80)
