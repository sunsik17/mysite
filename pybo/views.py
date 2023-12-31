from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .forms import QuestionForm, AnswerForm
from .models import Question


# Create your views here.
def index(request):
    page = request.GET.get('page', '1')  # 페이지
    question_list = Question.objects.order_by('-create_date')  # - 가 있으면 내림차순 desc, 없으면 오름차순 asc
    paginator = Paginator(question_list, 10)  # page당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj}
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)


@login_required(login_url='common:login')
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.author = request.user
            answer.save()
            return redirect('pybo:detail', question_id=question_id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)


@login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()

    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_modify(reqeust, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if reqeust.user != question.author:
        messages.error(reqeust, '수정 권한이 없습니다.')
        return redirect('pybo:detail', question_id=question.id)

    if reqeust.method == 'POST':
        form = QuestionForm(reqeust.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)

    context = {'form': form}
    return render(reqeust, 'pybo/question_form.html', context)
