from django.conf.urls import url
from .views import MoviesView, CommentsView, welcome

urlpatterns = [
    url('movies', MoviesView.as_view(), name="MoviesView"),
    url('comments', CommentsView.as_view(), name="CommentsView"),
    url('', welcome, name="welcome")
]
