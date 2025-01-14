from django.contrib import admin

# Register your models here.
from .models import Quiz
from django.urls import reverse
from django.utils.html import format_html


class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'user_link', 'category_link', 'question_count', 'created_at', 'updated_at')
    list_filter = ('category', 'user')
    search_fields = ('title', 'description', 'user__email', 'user__id')
    filter_horizontal = ('questions',)
    
    def user_link(self, obj):
        url = reverse('admin:%s_%s_change' % (obj.user._meta.app_label, obj.user._meta.model_name), args=[obj.user.id])
        return format_html(f'<a href="{url}" target="_blank">[{obj.user.id}] {obj.user.email}</a>')
    

    def category_link(self, obj):
        url = reverse('admin:%s_%s_change' % (obj.category._meta.app_label, obj.category._meta.model_name), args=[obj.category.id])
        return format_html(f'<a href="{url}" target="_blank">[{obj.category.id}] {obj.category.name}</a>')


    user_link.short_description = 'User'
    category_link.short_description = 'Category'

    def question_count(self, obj):
        return obj.questions.count()
    
    question_count.short_description = 'Number of Questions'

admin.site.register(Quiz, QuizAdmin)
