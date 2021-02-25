from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Question, Answer, Comment
from django.utils import timezone
from .forms import QuestionForm, AnswerForm, CommentForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

def index(request):

    """
    pybo 목록 출력
    """

    #입력 인자
    page = request.GET.get('page', '1') #페이지

    #조회
    question_list = Question.objects.order_by('-create_date')

    #페이징 처리
    paginator = Paginator(question_list, 10) #페이지 당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj}
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    """
    pybo 내용 출력
    """

    question = get_object_or_404(Question, pk=question_id)
    context = {'question':question}
    return render(request, 'pybo/question_detail.html', context)

@login_required(login_url='common:login') #로그인 상태인지 검사한후 비로그인 상태면 로그인창으로 이동
def answer_create(request, question_id):
    """
    pybo 답변 등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context= {'question':question,  'form':form}
    return render(request, 'pybo/question_detail.html', context)

@login_required(login_url='common:login') #로그인 상태인지 검사한후 비로그인 상태면 로그인창으로 이동
def question_create(request):
    """
    pybo 질문 등록
    """
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context= {'form': form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login') #로그인 상태인지 검사한후 비로그인 상태면 로그인창으로 이동
def question_modify(request, question_id):
    """
    pybo질문 수정
    """
    question = get_object_or_404(Question, pk=question_id)

    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('pybo:detail', question_id = question.id)

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context= {'form':form}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login') #로그인 상태인지 검사한후 비로그인 상태면 로그인창으로 이동
def question_delete(request, question_id):
    """
    pybo 질문 삭제
    """
    question= get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다.')
        return redirect('pybo:detail', question_id = question.id)
    question.delete()
    return redirect('pybo:index')

@login_required(login_url='common:login') #로그인 상태인지 검사한후 비로그인 상태면 로그인창으로 이동
def answer_modify(request, answer_id):
    """
    pybo 답변 수정
    """
    answer = get_object_or_404(Answer, pk=answer_id)

    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('pybo:detail', question_id = question.id)

    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('pybo:detail', question_id=answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    context= {'answer':answer, 'form':form}
    return render(request, 'pybo/answer_form.html', context)


@login_required(login_url='common:login') #로그인 상태인지 검사한후 비로그인 상태면 로그인창으로 이동
def answer_delete(request, answer_id):
    """
    pybo 답변 삭제
    """
    answer= get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다.')
    
    else:
        answer.delete()
    return redirect('pybo:detail', question_id = answer.question.id)


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
            return redirect('pybo:detail', question_id=question.id)
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
            return redirect('pybo:detail', question_id=comment.question.id)
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
            return redirect('pybo:detail', question_id=comment.answer.question.id)
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
            return redirect('pybo:detail', question_id=comment.answer.question.id)
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

