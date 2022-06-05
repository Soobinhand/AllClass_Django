from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'board'
urlpatterns = [
                  path('', views.blankIndex, name='blankIndex'),
                  path('<int:board_id>', views.index, name='index'),
                  path('<int:board_id>/<int:question_id>/', views.detail, name='detail'),
                  path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'),
                  path('<int:board_id>/question/create/', views.question_create, name='question_create'),
                  path('<int:board_id>/question/modify/<int:question_id>/', views.question_modify,
                       name='question_modify'),
                  path('<int:board_id>/question/delete/<int:question_id>/', views.question_delete,
                       name='question_delete'),
                  path('answer/modify/<int:answer_id>/', views.answer_modify, name='answer_modify'),
                  path('answer/delete/<int:answer_id>/', views.answer_delete, name='answer_delete'),
                  path('<int:board_id>/question/vote/<int:question_id>/', views.question_vote, name='question_vote'),
                  path('answer/vote/<int:answer_id>/', views.answer_vote, name='answer_vote'),


              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
