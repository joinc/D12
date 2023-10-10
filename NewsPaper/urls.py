from django.urls import path
from NewsPaper.views import (index, search_post, PostList, PostCreateView, PostDetailView, PostEditView, PostDeleteView,
                             AuthorList, CategoryList, category_subscribe, category_unsubscribe)
from NewsPaper.sign import LoginView, LogoutView, RegisterView
from NewsPaper.profile import IndexView, upgrade_me

urlpatterns = [
    path('', index, name='index', ),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', RegisterView.as_view(), name='signup'),
    path('profile/', IndexView.as_view(), name='profile'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('search/', search_post, name='post_search'),
    path('news/', PostList.as_view(), name='post_list', ),
    path('news/add/', PostCreateView.as_view(), name='post_create', ),
    path('news/<int:post_id>/', PostDetailView.as_view(), name='post_show', ),
    path('news/<int:post_id>/edit/', PostEditView.as_view(), name='post_edit'),
    path('news/<int:post_id>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('author/list/', AuthorList.as_view(), name='author_list', ),
    path('category/list/', CategoryList.as_view(), name='category_list', ),
    path('category/<int:category_id>/subscribe/', category_subscribe, name='category_subscribe', ),
    path('category/<int:category_id>/unsubscribe/', category_unsubscribe, name='category_unsubscribe', ),
]
