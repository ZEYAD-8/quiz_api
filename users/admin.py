from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserCustom
from django.urls import reverse
from django.utils.html import format_html
from questions.models import Question
from quizzes.models import Quiz
from categories.models import Category

class UserCustomAdmin(UserAdmin):
    model = UserCustom
    list_display = (
        'id', 'email', 'is_creator', 'is_active', 'is_staff', 
        'question_count', 'quiz_count', 'category_count', 
        'view_questions_link', 'view_quizzes_link', 'view_categories_link'
    )
    list_filter = ('is_creator',)
    search_fields = ('email', 'id')
    ordering = ('id', 'email')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('username', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_creator', 'is_admin')}),
        ('Metrics', {
            'fields': (
                'question_count_display', 
                'view_questions_link_display', 
                'quiz_count_display', 
                'view_quizzes_link_display', 
                'category_count_display',
                'view_categories_link_display'
            )
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_creator', 'is_admin', 'is_active')}
        ),
    )

    readonly_fields = (
        'question_count_display', 'quiz_count_display', 'category_count_display', 
        'view_questions_link_display', 'view_quizzes_link_display', 'view_categories_link_display'
    )

    def question_count(self, obj):
        return obj.questions.count()

    def quiz_count(self, obj):
        return obj.quizzes.count()

    def category_count(self, obj):
        return obj.categories.count()

    question_count.short_description = 'Questions'
    quiz_count.short_description = 'Quizzes'
    category_count.short_description = 'Categories'


    def view_questions_link(self, obj):

        url = reverse('admin:%s_%s_changelist' % (Question._meta.app_label, Question._meta.model_name)) + f'?user__id__exact={obj.id}'
        return format_html('<a href="{}">View Questions</a>', url)


    def view_quizzes_link(self, obj):
        url = reverse('admin:%s_%s_changelist' % (Quiz._meta.app_label, Quiz._meta.model_name)) + f'?user__id__exact={obj.id}'
        return format_html('<a href="{}">View Quizzes</a>', url)


    def view_categories_link(self, obj):
        url = reverse('admin:%s_%s_changelist' % (Category._meta.app_label, Category._meta.model_name)) + f'?user__id__exact={obj.id}'
        return format_html('<a href="{}">View Categories</a>', url)


    view_questions_link.short_description = 'Questions Link'
    view_quizzes_link.short_description = 'Quizzes Link'
    view_categories_link.short_description = 'Categories Link'

    def question_count_display(self, obj):
        return f"{obj.questions.count()}"

    def quiz_count_display(self, obj):
        return f"{obj.quizzes.count()}"

    def category_count_display(self, obj):
        return f"{obj.categories.count()}"

    question_count_display.short_description = 'Questions created'
    quiz_count_display.short_description = 'Quizzes created'
    category_count_display.short_description = 'Categories created'


    # to be able to view the links in the detail view of the user (in addition to the list view)
    def view_questions_link_display(self, obj):
        return self.view_questions_link(obj)

    def view_quizzes_link_display(self, obj):
        return self.view_quizzes_link(obj)

    def view_categories_link_display(self, obj):
        return self.view_categories_link(obj)

    view_questions_link_display.short_description = 'Link'
    view_quizzes_link_display.short_description = 'Link'
    view_categories_link_display.short_description = 'Link'

admin.site.register(UserCustom, UserCustomAdmin)
