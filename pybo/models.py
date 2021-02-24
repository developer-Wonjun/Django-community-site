from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    modify_date = models.DateTimeField(null=True, blank=True) #수정 일시를 의미. null,blank = 어떤조건으로든 값을 비어둘 수 있음을 의미. 
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()

    def __str__(self):   #shell에서 id값이 제목 그대로 표기되기 위해서!!
        return self.subject

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    modify_date = models.DateTimeField(null=True, blank=True) #수정 일시를 의미. null,blank = 어떤조건으로든 값을 비어둘 수 있음을 의미. 
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()


