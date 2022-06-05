from django.contrib import admin
from .models import Question, Board, Board2


class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']


class BoardAdmin(admin.ModelAdmin):
    search_fields = ['board_id']


class Board2Admin(admin.ModelAdmin):
    search_fields = ['board2_id']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Board, BoardAdmin)
admin.site.register(Board2, Board2Admin)
