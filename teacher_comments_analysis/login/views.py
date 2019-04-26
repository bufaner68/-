from django.shortcuts import render
from django.shortcuts import redirect  # 用于重定向
from login import models
from .form import StudentForm
from .form import TeacherForm
from .models import Teacher
from .models import Comment
from django.shortcuts import get_object_or_404
import datetime
import jieba
import gensim
from gensim import corpora

from gensim import similarities
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
# Create your views here.
# 四个视图都返回一个render()调用，render方法接收request作为第一个参数
# 要渲染的页面为第二个参数
# 以及需要传递给页面的数据字典作为第三个参数（可以为空）
# 表示根据请求的部分，以渲染的HTML页面为主体，使用模板语言将数据字典填入，然后返回给用户的浏览器。


def index(request):
    pass
    return render(request, 'login/index.html')


def tlogin(request):
    # 判断用户是否已登录
    if request.session.get('is_login', None):
        return redirect("/index/")
    if request.method == 'POST':
        login_form = TeacherForm(request.POST)
        # print(username, password)
        if login_form.is_valid():
            username = login_form.cleaned_data['Tusername']
            password = login_form.cleaned_data['Tpassword']
            # 用户名合法性验证
            # 密码长度验证
            # ...
        try:
            teacher = models.Teacher.objects.get(teacher_name=username)
            print("用户名为：", username)
            if teacher.teacher_password == password:
                print("密码为：", password)
                request.session['is_login'] = True
                request.session['is_tea'] = True
                request.session['user_id'] = teacher.id
                request.session['user_name'] = teacher.teacher_name
                return redirect('/index/')
            else:
                print("密码错误！")
        except:
            print("用户名不存在！")
        return render(request, 'login/tlogin.html', locals())
    login_form = TeacherForm()
    return render(request, 'login/tlogin.html', locals())


def login(request):
    # 判断用户是否已登录
    if request.session.get('is_login', None):
        return redirect("/index/")
    if request.method == 'POST':
        login_form = StudentForm(request.POST)
        # print(username, password)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            # 用户名合法性验证
            # 密码长度验证
            # ...
        try:
            student = models.Student.objects.get(student_name=username)
            # print("用户名为：", username)
            if student.student_password == password:
                # print("密码为：", password)
                request.session['is_login'] = True
                request.session['is_tea'] = False
                request.session['user_id'] = student.id
                request.session['user_name'] = student.student_name
                return redirect('/index/')
            else:
                print("密码错误！")
        except:
            print("用户名不存在！")
        return render(request, 'login/login.html', locals())
    login_form = StudentForm()
    return render(request, 'login/login.html', locals())


def about(request):
    pass
    return render(request, 'login/about.html')


def teacher(request):
    try:
        teacher = models.Teacher.objects.all()
        #print("老师列表：")
        #print(teacher)
        student = models.Student.objects.all()
        #print("学生列表：")
        #print(student)
        comment = models.Comment.objects.all()
        #print("评论列表：")
        #print(comment)
        #print(student[0].student_name, student[1].student_name)
        print(comment[0].student, comment[0].comment)
    except:
        print("无数据！")
    teacher_list = models.Teacher.objects.all()
    return render(request, 'login/teacher.html', {'data': teacher_list})


# 生成评价标签词云
def ciyun(f):
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt
    import pygal

    # f = open('data/语料库.txt', 'r', encoding="utf-8").read()
    #f = "幽默风趣 幽默 亲切 很好 很好 很好 思维清晰 思维清晰 思维清晰 思维清晰 课程简单 适合初学者 有耐心 课程不错 课程简单 适合初学者 有耐心 课程不错 课程简单 适合初学者 有耐心 课程不错"
    wordcloud = WordCloud(font_path="C:/windows/Fonts/simfang.ttf", background_color="white", width=600, height=300,
                          margin=2).generate(f)

    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
    wordcloud.to_file('static/images/ciyun.jpg')  # 保存图片


# 将原始评价与前期生成的评价标签做相似度计算，对每一条原始评价生成评论标签
def newdata(l1, a):
    from gensim import models
    all_doc_list = []
    for doc in l1:
        doc_list = [word for word in jieba.cut(doc)]
        all_doc_list.append(doc_list)

    #print("分词结果：", all_doc_list)
    doc_test_list = [word for word in jieba.cut(a)]

    # 制作语料库
    dictionary = corpora.Dictionary(all_doc_list)  # 制作词袋
    # 词袋的理解
    # 词袋就是将很多很多的词,进行排列形成一个 词(key) 与一个 标志位(value) 的字典
    # 例如: {'什么': 0, '你': 1, '名字': 2, '是': 3, '的': 4, '了': 5, '今年': 6, '几岁': 7, '多': 8, '有': 9, '胸多大': 10, '高': 11}
    # 至于它是做什么用的,带着问题往下看

    #print("token2id", dictionary.token2id)
    #print("dictionary", dictionary, type(dictionary))

    corpus = [dictionary.doc2bow(doc) for doc in all_doc_list]
    # 语料库:
    # 这里是将all_doc_list 中的每一个列表中的词语 与 dictionary 中的Key进行匹配
    # 得到一个匹配后的结果,例如['你', '今年', '几岁', '了']
    # 就可以得到 [(1, 1), (5, 1), (6, 1), (7, 1)]
    # 1代表的的是 你 1代表出现一次, 5代表的是 了  1代表出现了一次, 以此类推 6 = 今年 , 7 = 几岁
    #print("corpus", corpus, type(corpus))

    # 将需要寻找相似度的分词列表 做成 语料库 doc_test_vec
    doc_test_vec = dictionary.doc2bow(doc_test_list)
    #print("doc_test_vec", doc_test_vec, type(doc_test_vec))

    # 将corpus语料库(初识语料库) 使用Lsi模型进行训练
    lsi = models.LsiModel(corpus)
    # 这里的只是需要学习Lsi模型来了解的,这里不做阐述
    #print("lsi", lsi, type(lsi))
    # 语料库corpus的训练结果
    #print("lsi[corpus]", lsi[corpus])
    # 获得语料库doc_test_vec 在 语料库corpus的训练结果 中的 向量表示
    #print("lsi[doc_test_vec]", lsi[doc_test_vec])

    # 文本相似度
    # 稀疏矩阵相似度 将 主 语料库corpus的训练结果 作为初始值
    index = similarities.SparseMatrixSimilarity(lsi[corpus], num_features=len(dictionary.keys()))
    #print("index", index, type(index))

    # 将 语料库doc_test_vec 在 语料库corpus的训练结果 中的 向量表示 与 语料库corpus的 向量表示 做矩阵相似度计算
    sim = index[lsi[doc_test_vec]]
    #print("sim", sim, type(sim))

    # 对下标和相似度结果进行一个排序,拿出相似度最高的结果
    # cc = sorted(enumerate(sim), key=lambda item: item[1],reverse=True)
    cc = sorted(enumerate(sim), key=lambda item: -item[1])
    #print(cc)
    text = l1[cc[0][0]]
    #print(a, text)
    return text

def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    request.session.flush()
    return redirect("/index/")


def detail(request, teacher_id):
    teacher_list = get_object_or_404(Teacher, pk=teacher_id)
    return render(request, 'login/detail.html', {'teacher': teacher_list})


def add(request, teacher_id):

    if request.method == 'POST':
        newcomment = request.POST.get('comment')
        models.Comment.objects.create(
        # 向数据库中插入数据
        comment=newcomment,
        teacher_id=teacher_id,
        student_id=request.session['user_id'],
        created_time=datetime.date.today()
    )
    #newcomment = request.POST['comment']
    #comment = Comment(comment=newcomment, teacher_id=teacher_id, student_id=request.session['user_id'],created_time=datetime.date.today())
    #comment.save()
    # 成功处理数据后，自动跳转到结果页面，防止用户连续多次提交。
    #HttpResponseRedirect(reverse('login:results', args=(teacher.id,)))

    # 读取
    items = open("data/myphrase.txt", "r", encoding="utf-8").read()
    list = items.split()
    #print(list)
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    #print("教师评价查询：", teacher.comment_set.all())

    # 生成评价标签
    label_list = []
    for comment in teacher.comment_set.all():
        label = newdata(list, comment.comment)
        #print("生成的标签为：", label)
        label_list.append(label)
    f = " ".join(label_list)
    # 生成词云
    ciyun(f)

    return render(request, 'login/results.html', {'teacher': teacher})


def results(request, teacher_id):
    # 读取
    items = open("data/myphrase.txt", "r", encoding="utf-8").read()
    list = items.split()
    # print(list)
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    # print("教师评价查询：", teacher.comment_set.all())

    # 生成评价标签
    label_list = []
    for comment in teacher.comment_set.all():
        label = newdata(list, comment.comment)
        print("生成的标签为：", label)
        label_list.append(label)
    f = " ".join(label_list)
    # 生成词云
    ciyun(f)
    return render(request, "login/results.html", {'teacher': teacher})



