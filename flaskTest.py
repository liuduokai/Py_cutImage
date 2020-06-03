# -*- coding: UTF-8 -*-
import numpy as np
from flask import Flask
from flask import request
import cv2
import base64
import re
import json
import chardet
from werkzeug.utils import secure_filename

app = Flask(__name__)

def cv_imread(file_path):
    cv_img = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)
    return cv_img

# hello world接口
# @app.route('/')
# def hello_world():
#     return 'Hello World!'


@app.route('/upload/', methods=['POST'])
def upload():
    if request.method == 'POST':

        # ip = request.remote_addr
        # print("request from:", ip)

        # cutWid = 100

        # 读取切割宽度及文件参数
        try:
            cutWid = int(request.args.get("width"))
            f = request.files['file']
            filepath = './upload/' + f.filename
            filepath = re.sub('\"', '', filepath)
            print(filepath)

            # filename = f.filename
            # print(chardet.detect(filename))
            # print(type(f.filename))
            # f.filename = re.sub(r'\"', '', f.filename)
            # print(f.filename)
            # print(filepath)
            try:
                f.save(filepath)
            except OSError as err:
                print("OS error: {0}".format(err))
                return "写入文件出现错误"
            try:
                img = cv_imread(filepath)
            except OSError as err:
                print("OS error: {0}".format(err))
                return "读取文件出现错误"
        except OSError as err:
            print("OS error: {0}".format(err))
            return "文件或参数发生错误"

        hei = img.shape[0]
        wid = img.shape[1]
        # print(img.shape)

        # 获取文件名及文件类型
        # print(re.search('\.', f.filename))
        filename = f.filename[0:(re.search('\.', f.filename).span()[1])-1]
        filetype = f.filename[(re.search('\.', f.filename).span()[1]):len(f.filename)]
        filetype = re.sub('\"', '', filetype)

        print(filename, filetype)
        # 求出切割的分数
        cutCount = int(wid / cutWid) + 1

        retImg = {}

        # 循环切割图片
        i = 0
        while i < cutCount:
            # print(i)

            # 最后一次不一定为整数大小
            if i == cutCount - 1:
                cropped = img[0:hei, cutWid * i:wid]
            else:
                cropped = img[0:hei, cutWid * i:cutWid * (i + 1)]

            # base64转码
            # 返回无法返回多个文件，故将图片转化为BASE64字符串后构成字典文件
            try:
                base64_str = cv2.imencode('.jpg', cropped)[1].tostring()
                # print(base64_str)
                base64_str = base64.b64encode(base64_str)
                base64_str = str(base64_str, encoding="utf-8")
            except OSError as err:
                print("OS error: {0}".format(err))
                return "格式转换出现错误"
            # print(type(base64_str))

            retImg[filename + '-' + str(i)+'.'+filetype] = base64_str

            # 写分割后的文件，服务器可选是否存储
            cv2.imwrite("./output/" + filename + '_' + str(i) + '.' + filetype, cropped)

            i += 1

        # print(retImg)
        return json.dumps(retImg, ensure_ascii=False)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port='5000')