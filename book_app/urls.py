from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('books', views.all_books),
    path('books/<int:book_id>', views.specific_book),
    path('register_user', views.register),
    path('login_user', views.login),
    path('logout', views.logout),
    path('create_book', views.create_book),
    path('favorite/<int:book_id>', views.favorite_book),
    path('delete_book/<int:book_id>', views.delete_book),
    path('edit/<int:book_id>', views.edit_book),
    path('remove_fave/<int:book_id>', views.remove_fave),
    path('user/<int:member_id>', views.specific_user)
]
