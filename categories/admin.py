from django.contrib import admin

# Register your models here.
from .models import Category
from django.urls import reverse
from django.utils.html import format_html

from questions.models import Question 
from quizzes.models import Quiz


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'slug', 'user_link', 'question_count', 'quiz_count', 'created_at', 'updated_at')
    list_filter = ('user',)
    search_fields = ('name', 'description', 'slug', 'user__email', 'user__id')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at', 'view_questions_link', 'view_quizzes_link')

    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description', 'user', 'created_at', 'updated_at'),
        }),
        ('Related Data', {
            'fields': ('view_questions_link', 'view_quizzes_link'),
        }),
    )

    def user_link(self, obj):
        url = reverse('admin:%s_%s_change' % (obj.user._meta.app_label, obj.user._meta.model_name), args=[obj.user.id])
        return format_html('<a href="{}" target="_blank">[{}] {}</a>', url, obj.user.id, obj.user.email)
    

    def question_count(self, obj):
        return obj.questions.count()
    

    def quiz_count(self, obj):
        return obj.quizzes.count()

    user_link.short_description = 'User'
    question_count.short_description = 'Questions'
    quiz_count.short_description = 'Quizzes'


    def view_questions_link(self, obj):
        url = reverse('admin:%s_%s_changelist' % (Question._meta.app_label, Question._meta.model_name)) + f'?category__id__exact={obj.id}'
        return format_html('<a href="{}">View Questions</a>', url)
    

    def view_quizzes_link(self, obj):
        url = reverse('admin:%s_%s_changelist' % (Quiz._meta.app_label, Quiz._meta.model_name)) + f'?category__id__exact={obj.id}'
        return format_html('<a href="{}">View Quizzes</a>', url)
    
    view_questions_link.short_description = 'Questions'
    view_quizzes_link.short_description = 'Quizzes'


admin.site.register(Category, CategoryAdmin)
