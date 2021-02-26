from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    modify_date = models.DateTimeField(null=True, blank=True) #수정 일시를 의미. null,blank = 어떤조건으로든 값을 비어둘 수 있음을 의미. 
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    voter = models.ManyToManyField(User, related_name='voter_question')

    def __str__(self):   #shell에서 id값이 제목 그대로 표기되기 위해서!!
        return self.subject

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    modify_date = models.DateTimeField(null=True, blank=True) #수정 일시를 의미. null,blank = 어떤조건으로든 값을 비어둘 수 있음을 의미. 
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    voter = models.ManyToManyField(User, related_name='voter_answer')


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE) #댓글 글쓴이
    content = models.TextField()# 댓글 내용
    create_date = models.DateTimeField()#댓글 작성일시
    modify_date = models.DateTimeField(null=True, blank=True)#댓글 수정일시
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)#이 댓글이 달린 질문
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)# 이 댓글이 달린 답변


