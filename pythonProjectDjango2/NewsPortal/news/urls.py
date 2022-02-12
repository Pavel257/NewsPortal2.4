from django.urls import path
from .views import *

urlpatterns = [
    path('authors/', AuthorList.as_view(), name='authors'),
    path('category/', CategoryList.as_view(), name='category'),
    path('', NewsList.as_view(), name='news1'),
    path('<int:pk>/', NewsDetailView.as_view(), name='news_detail'),
    path('search/', NewsSearch.as_view(), name='news_search'),
    path('create/', AddNews.as_view(), name='news_create'),
    path('create/<int:pk>', ChangeNews.as_view(), name='news_update'),
    path('delete/<int:pk>', DeleteNews.as_view(), name='news_delete'),
    # path('<int:pk>/add_subscribe/', add_subscribe, name='add_subscribe'),
    # path('<int:pk>/del_subscribe/', del_subscribe, name='del_subscribe'),
    path('subscribed/<int:news_category_id>', subscribe_me, name='subscribed'),

]