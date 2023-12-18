from django.shortcuts import render, get_object_or_404, redirect

from .forms import QuestionForm
from .models import Question


# Create your views here.
def index(request):
    question_list = Question.objects.order_by('-create_date')  # - 가 있으면 내림차순 desc, 없으면 오름차순 asc
    context = {'question_list': question_list}
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)


def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.answer_set.create(content=request.POST.get('content'))
    return redirect('pybo:detail', question_id=question_id)


def question_create(request):
    form = QuestionForm()
    return render(request, 'pybo/question_form.html', {'form': form})
