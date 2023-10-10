from django import forms
from django_filters import FilterSet
from NewsPaper.models import Post


# class PostFilter(FilterSet):
#     class Meta:
#         model = Post
#         fields = {
#             'title': ['icontains'],
#             'text': ['icontains'],
#             'author': ['exact'],
#             'create_date': ['exact', 'range']
#         }


class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'author': ['exact'],
            'create_date': ['gt'],
            'title': ['icontains'],
            'type_post': ['exact']
        }
