from django.urls import path
from .views import (Note_detail, books_view, conversion, 
                    delete_homework, dictionary_view, 
                    home_view, 
                    homework_view, 
                    notes_view, 
                    Note_delete_view, profile_view, todo_delete, todo_update, 
                    todo_view, 
                    update_homework, wiki_views, 
                    youtube_view
)

urlpatterns = [
    path('', home_view, name="home"),

    #notes_urls
    path('notes/', notes_view, name = "notes"),
    path('notes/<int:id>/', Note_delete_view, name = "notes_delete"),
    path('detail/<int:id>/', Note_detail, name = "notes_detail"),

    #homework_urls
    path('homework', homework_view, name = 'homework'),
    path('homework/<int:id>', update_homework, name = 'update_homework'),
    path('delete_homework/<int:id>/', delete_homework, name = 'delete_homework'),

    #youtube_urls
    path('youtube', youtube_view, name = "youtube" ),

    #todo_app urls
    path('todo', todo_view, name="todo"),
    path('todo/<int:id>/', todo_update, name = "update_todo"),
    path('todo_delete/<int:id>/', todo_delete, name = "delete_todo"),

    #books_app urls
    path('books', books_view, name = "books"),

    #dictinary_urls
    path('dictionary', dictionary_view, name="dict_view"),

    #wiki_urls
    path('wiki', wiki_views, name="wiki"),

    #conversion_urls
    path('convert', conversion, name = "conv_view"),

    path('profile', profile_view, name="profile_view"),
]


