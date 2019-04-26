from django.conf.urls import url
from . import views

app_name = 'login'

urlpatterns = [
    # ex: /login/
    url(r'^$', views.login, name='login'),
    # ex: /login/5/
    url(r'^(?P<teacher_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /login/5/results/
    url(r'^(?P<teacher_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /login/5/add/
    url(r'^(?P<teacher_id>[0-9]+)/add/$', views.add, name='add'),

]
