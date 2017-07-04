from django.conf.urls import url
from . import views

app_name = 'books'
urlpatterns = [
    url(r'^create/', views.create, name='create'),
    url(r'(?P<book_id>[0-9]+)/recommend', views.recommend, name='recommend'),
    url(r'^bookinfo/(?P<book_id>[0-9]+)', views.bookinfo, name='book_info'),
    url(r'^mybooks/', views.mybooks, name='mybooks'),
    url(r'^addalreadyread/(?P<book_id>[0-9]+)', views.addAlreadyReadBook, name='addAlreadyReadBook'),
    url(r'^wanttoread/', views.want_to_read, name='want_to_read'),
    url(r'^addwanttoread/(?P<book_id>[0-9]+)', views.add_want_to_read, name='add_want_to_read'),

]