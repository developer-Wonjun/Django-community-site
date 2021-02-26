from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.http import HttpResponse
from ..models import Question, Answer, Comment
from django.utils import timezone
from ..forms import QuestionForm, AnswerForm, CommentForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required(login_url='common:login') #로그인 상태인지 검사한후 비로그인 상태면 로그인창으로 이동
def comment_create_question(request, question_id):
    """
    pybo 질문에 댓글 달기.
    """
    question = get_object_or_404(Question, pk=question_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.question=question
            comment.save()
            return redirect('{}#comment_{}'.format(resolve_url('pybo:detail', question_id=comment.question.id), comment.id))
    else:
        form = CommentForm
    context= {'form':form}
    return render(request, 'pybo/comment_form.html', context)

@login_required(login_url='common:login') #로그인 상태인지 검사한후 비로그인 상태면 로그인창으로 이동
def comment_modify_question(request, comment_id):
    """
    pybo질문 댓글 수정
    """
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.user != comment.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('pybo:detail', question_id = comment.question.id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('{}#comment_{}'.format(resolve_url('pybo:detail', question_id=comment.question.id), comment.id))
    else:
        form = CommentForm(instance=comment)
    context= {'form':form}
    return render(request, 'pybo/comment_form.html', context)

@login_required(login_url='common:login') #로그인 상태인지 검사한후 비로그인 상태면 로그인창으로 이동
def comment_delete_question(request, comment_id):
    """
    pybo 질문 댓글 삭제
    """
    comment= get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다.')
        return redirect('pybo:detail', question_id = comment.question.id)
    else:
        comment.delete()
    return redirect('pybo:detail', question_id=comment.question_id)

@login_required(login_url='common:login') #로그인 상태인지 검사한후 비로그인 상태면 로그인창으로 이동
def comment_create_answer(request, answer_id):
    """
    pybo 답변에 댓글 달기.
    """
    answer = get_object_or_404(Answer, pk=answer_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.answer=answer
            comment.save()
            return redirect('{}#comment_{}'.format(resolve_url('pybo:detail', question_id=comment.answer.question.id), comment.id))
    else:
        form = CommentForm
    context= {'form':form}
    return render(request, 'pybo/comment_form.html', context)

@login_required(login_url='common:login') #로그인 상태인지 검사한후 비로그인 상태면 로그인창으로 이동
def comment_modify_answer(request, comment_id):
    """
    pybo답변 댓글 수정
    """
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.user != comment.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('pybo:detail', question_id = comment.answer.question.id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('{}#comment_{}'.format(resolve_url('pybo:detail', question_id=comment.answer.question.id), comment.id))
    else:
        form = CommentForm(instance=comment)
    context= {'form':form}
    return render(request, 'pybo/comment_form.html', context)

@login_required(login_url='common:login') #로그인 상태인지 검사한후 비로그인 상태면 로그인창으로 이동
def comment_delete_answer(request, comment_id):
    """
    pybo 답변 댓글 삭제
    """
    comment= get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다.')
        return redirect('pybo:detail', question_id = comment.answer.question.id)
    else:
        comment.delete()
    return redirect('pybo:detail', question_id=comment.answer.question_id)