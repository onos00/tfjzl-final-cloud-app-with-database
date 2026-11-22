from django.db import models
from django.conf import settings
from django.utils.timezone import now


class Course(models.Model):
    name = models.CharField(max_length=100, default='online course')
    description = models.CharField(max_length=500)
    pub_date = models.DateField(null=True)
    total_enrollment = models.IntegerField(default=0)
    image = models.ImageField(upload_to='course_images/', blank=True, null=True)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    title = models.CharField(max_length=200, default="title")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.TextField()
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Instructor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_time = models.BooleanField(default=True)
    total_students = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class Learner(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    occupation = models.CharField(
        max_length=20,
        choices=[
            ('student', 'Student'),
            ('developer', 'Developer'),
            ('data_scientist', 'Data Scientist'),
            ('dba', 'Database Administrator')
        ],
        default='student'
    )
    social_link = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return self.user.username


class Enrollment(models.Model):
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(default=now)
    mode = models.CharField(
        max_length=20,
        choices=[('audit', 'Audit'), ('honor', 'Honor'), ('B2B', 'B2B')],
        default='audit'
    )


class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    grade = models.IntegerField(default=50)

    def __str__(self):
        return self.question_text

    def calculate_max_score(self):
        return self.grade


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)

    def __str__(self):
        return f"Submission {self.id}"