from django.core.paginator import Paginator
from django.http import HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404, redirect

from .forms import QuestionForm, AnswerForm
from .models import Question


# Create your views here.
def index(request):
    page = request.GET.get('page', '1')  # 페이지
    question_list = Question.objects.order_by('-create_date')  # - 가 있으면 내림차순 desc, 없으면 오름차순 asc
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj}
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)


def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question_id)
    else:
        return HttpResponseNotAllowed('Only \'POST\' method possible')
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)


def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()

    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)
