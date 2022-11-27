from django.urls import path

from . import views

urlpatterns = [
    path('index', views.index,name=None),
    path('showList', views.showList, name='show_list'),
    path('deleteWord', views.delete_word, name='delete_word'),
    path('addingWord', views.adding_word, name='adding_word'),
    path('searchWord', views.search_word, name='search_word'),
    path('updateWord', views.update_word, name='update_word')
    # path('searchResult', views.search_result, name='search_result')

    # path('list_words/',views.list_words,name='list_words')
]
