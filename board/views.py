from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Question, Answer, Board, Board2
from .forms import QuestionForm, AnswerForm
from django.http import HttpResponseNotAllowed
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Question


def blankIndex(request):
    return redirect('board:index', board_id=1)


def index(request, board_id):
    board = Board.objects.all()

    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')
    question_list = Question.objects.order_by('-create_date').filter(board=board_id)
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(answer__content__icontains=kw) |  # 답변 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'board': board, 'board_id': board_id}
    return render(request, 'board/question_list.html', context)


def detail(request, question_id, board_id):
    question = Question.objects.get(id=question_id, board_id=board_id)
    context = {'question': question, 'board_id': board_id}
    return render(request, 'board/question_detail.html', context)


@login_required(login_url='common:login')
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('board:detail', question_id=question.id, board_id=question.board_id)
    else:
        return HttpResponseNotAllowed('Only POST is possible.')
    context = {'question': question, 'form': form, 'board_id': question.board_id}
    return render(request, 'board/question_detail.html', context)


@login_required(login_url='common:login')
def question_create(request, board_id):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            if request.FILES:
                question.photo = request.FILES["photo"]
            question.author = request.user
            question.create_date = timezone.now()
            question.board_id = board_id
            question.save()
            return redirect('board:index', board_id=board_id)
    else:
        form = QuestionForm()
    context = {'form': form, 'board_id': board_id}
    return render(request, 'board/question_form.html', context)


@login_required(login_url='common:login')
def question_modify(request, question_id, board_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('board:detail', question_id=question.id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()  # 수정일시 저장
            question.board_id = board_id
            question.save()
            return redirect('board:detail', question_id=question.id, board_id=board_id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form, 'board_id': board_id}
    return render(request, 'board/question_form.html', context)


@login_required(login_url='common:login')
def question_delete(request, question_id, board_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('board:detail', question_id=question.id, board_id=board_id)
    question.delete()
    return redirect('board:index', board_id=board_id)


@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('board:detail', question_id=answer.question.id)
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('board:detail', question_id=answer.question.id, board_id=answer.question.board_id)
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form, 'board_id': answer.question.board_id}
    return render(request, 'board/answer_form.html', context)


@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        answer.delete()
    return redirect('board:detail', question_id=answer.question.id, board_id=answer.question.board_id)


@login_required(login_url='common:login')
def question_vote(request, question_id, board_id):
    question = get_object_or_404(Question, pk=question_id, board_id=board_id)
    if request.user == question.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        question.voter.add(request.user)
    return redirect('board:detail', question_id=question.id, board_id=board_id)


@login_required(login_url='common:login')
def answer_vote(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user == answer.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        answer.voter.add(request.user)
    return redirect('board:detail', question_id=answer.question.id, board_id=answer.question.board_id)
