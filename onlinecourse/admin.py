from django.contrib import admin
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 2

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 2

class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline, QuestionInline] if 'LessonInline' in globals() else [QuestionInline]
    list_display = ('name', 'pub_date', 'total_enrollment')
    search_fields = ['name', 'description']

class LessonAdmin(admin.ModelAdmin):
    list_display = ['title']

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'course', 'grade']
    inlines = [ChoiceInline]

# Register your models here
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Submission)