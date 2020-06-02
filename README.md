# Py_cutImage
将上传的图片按指定参数切割成不同宽度的小图片
## 文件说明
* client.py server.py：前期考虑使用socket编程实现网路调用，文件为socket编程demo后弃用，未完成
* main.py：裁切功能实现
* test.py: 测试一些功时使用
## 相关
* opencv:实现了图片裁剪功能
* flask:搭建了请求接口，可以通过post请求调用
## 调用说明
* 使用post请求服务请求需要两个参数
* width：需要切割的宽度
* file：上传的图片
  
## 返回说明
* 返回json格式数据
* 根据裁切后的文件数量使用文件名+_+编号.+扩展名的方式命名
* json 键为切割后图片名
* json 值为图片BASE64化后的字符串，可以使用BASE64转化为图片
 