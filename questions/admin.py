from django.contrib import admin

# Register your models here.
from .models import Question, MCQ, MatchingPair, OrderingItem
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.contrib.admin import SimpleListFilter

class MCQInline(admin.TabularInline):
    model = MCQ
    fields = ('text', 'is_correct')

class MatchingPairInline(admin.TabularInline):
    model = MatchingPair
    fields = ('item', 'match')

class OrderingItemInline(admin.TabularInline):
    model = OrderingItem
    fields = ('text', 'order') 

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'question_type', 'difficulty', 'user', 'category', 'view_related_objects')
    list_filter = ('question_type', 'difficulty', 'category')
    search_fields = ('text', 'user__email')
    ordering = ('difficulty',)

    inlines = [MCQInline, MatchingPairInline, OrderingItemInline]
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)


    def view_related_objects(self, obj):
        if obj.question_type == Question.MULTIPLE_CHOICE:
            links = [
                f'<a href="{reverse("admin:%s_%s_change" % (choice._meta.app_label, choice._meta.model_name), args=[choice.id])}" target="_blank">'
                f'[{choice.id}] [{"Correct" if choice.is_correct else "Incorrect"}] {choice.text}</a>'
                for choice in obj.choices.all()
            ]
        elif obj.question_type == Question.TRUE_FALSE:
            links = [f'Correct Answer: {"True" if obj.tf_correct_answer else "False"}']
        elif obj.question_type == Question.MATCHING:
            links = [
                f'<a href="{reverse("admin:%s_%s_change" % (pair._meta.app_label, pair._meta.model_name), args=[pair.id])}" target="_blank">'
                f'[{pair.id}] {pair.item} -> {pair.match}</a>'
                for pair in obj.matching_pairs.all()
            ]
        elif obj.question_type == Question.ORDERING:
            links = [
                f'<a href="{reverse("admin:%s_%s_change" % (item._meta.app_label, item._meta.model_name), args=[item.id])}" target="_blank">'
                f'[{item.id}] [Order: {item.order}] {item.text}</a>'
                for item in obj.ordering_items.all()
            ]
        else:
            return "N/A"

        return mark_safe("<br>".join(links))

    view_related_objects.short_description = 'Answers/CHoices'



class MCQ_Filter(SimpleListFilter):
    title = 'MCQ Questions'
    parameter_name = 'question'

    def lookups(self, request, model_admin):
        mcq_questions = Question.objects.filter(question_type=Question.MULTIPLE_CHOICE).order_by('id')
        return [(q.id, f"ID {q.id}: {q.text}") for q in mcq_questions]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(question__id=self.value())
        return queryset

class MCQAdmin(admin.ModelAdmin):
    list_display = ('text', 'is_correct', 'question_link')
    list_filter = (MCQ_Filter,)
    search_fields = ('question__id', 'question__text', 'text')

    def question_link(self, obj):
        url = reverse('admin:%s_%s_change' % (obj.question._meta.app_label, obj.question._meta.model_name), args=[obj.question.id])
        return format_html('<a href="{}" target="_blank">ID {}: {}</a>', url, obj.question.id, obj.question.text[:30])

    question_link.short_description = 'Related Question'



class Matching_Filter(SimpleListFilter):
    title = 'Matching Questions'
    parameter_name = 'question'

    def lookups(self, request, model_admin):
        matching_questions = Question.objects.filter(question_type=Question.MATCHING).order_by('id')
        return [(q.id, f"ID {q.id}: {q.text[:25]}") for q in matching_questions]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(question__id=self.value())
        return queryset


class MatchingPairAdmin(admin.ModelAdmin):
    list_display = ('item', 'match', 'question_link')
    list_filter = (Matching_Filter,)
    search_fields = ('question__id', 'question__text', 'item', 'match')

    def question_link(self, obj):
        url = reverse('admin:%s_%s_change' % (obj.question._meta.app_label, obj.question._meta.model_name), args=[obj.question.id])
        return format_html('<a href="{}" target="_blank">ID {}: {}</a>', url, obj.question.id, obj.question.text)

    question_link.short_description = 'Related Question'


class Ordering_Filter(SimpleListFilter):
    title = 'Ordering Questions'
    parameter_name = 'question'

    def lookups(self, request, model_admin):
        ordering_questions = Question.objects.filter(question_type=Question.ORDERING).order_by('id')
        return [(q.id, f"ID {q.id}: {q.text}") for q in ordering_questions]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(question__id=self.value())
        return queryset


class OrderingItemAdmin(admin.ModelAdmin):
    list_display = ('text', 'order', 'question_link')
    list_filter = (Ordering_Filter,)
    search_fields = ('question__id', 'question__text', 'text', 'order')

    def question_link(self, obj):
        url = reverse('admin:%s_%s_change' % (obj.question._meta.app_label, obj.question._meta.model_name), args=[obj.question.id])
        return format_html('<a href="{}" target="_blank">ID {}: {}</a>', url, obj.question.id, obj.question.text)

    question_link.short_description = 'Related Question'


admin.site.register(Question, QuestionAdmin)
admin.site.register(MCQ, MCQAdmin)
admin.site.register(MatchingPair, MatchingPairAdmin)
admin.site.register(OrderingItem, OrderingItemAdmin)
