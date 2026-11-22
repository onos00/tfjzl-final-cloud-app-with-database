from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .models import Course, Lesson, Question, Choice, Submission, Instructor, Learner

def index(request):
    course_list = Course.objects.order_by('-pub_date')[:10]
    context = {'course_list': course_list}
    return render(request, 'onlinecourse/course_list_bootstrap.html', context)

class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'onlinecourse/course_detail_bootstrap.html'

def registration_request(request):
    return render(request, 'onlinecourse/user_registration_bootstrap.html')

def login_request(request):
    return render(request, 'onlinecourse/user_login_bootstrap.html')

def logout_request(request):
    logout(request)
    return redirect('onlinecourse:index')

def enroll(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    course.total_enrollment += 1
    course.save()
    return HttpResponseRedirect(reverse('onlinecourse:course_details', args=(course.id,)))

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        learner = request.user
        submission = Submission.objects.create(learner=learner, course=course)
        
        for key in request.POST:
            if key.startswith('choice_'):
                choice_id = request.POST.get(key)
                choice = Choice.objects.get(pk=choice_id)
                submission.choices.add(choice)
                
        return HttpResponseRedirect(reverse('onlinecourse:show_exam_result', args=(course.id, submission.id)))

def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    total_score = 0
    max_score = 0
    
    for question in course.question_set.all():
        max_score += question.grade
        correct_choices = set(question.choice_set.filter(is_correct=True).values_list('id', flat=True))
        user_choices = set(submission.choices.filter(question=question).values_list('id', flat=True))
        if correct_choices and correct_choices == user_choices:
            total_score += question.grade
            
    context = {
        'course': course,
        'submission': submission,
        'grade': total_score,
        'max_score': max_score
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)