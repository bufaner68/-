from django.shortcuts import render
from django.shortcuts import redirect # 用于重定向

#from django import forms

# Create your views here.
# 四个视图都返回一个render()调用，render方法接收request作为第一个参数.
# 要渲染的页面为第二个参数
# 以及需要传递给页面的数据字典作为第三个参数（可以为空）
# 表示根据请求的部分，以渲染的HTML页面为主体，使用模板语言将数据字典填入，然后返回给用户的浏览器。


def index(request):
    pass
    return render(request, 'index.html')



