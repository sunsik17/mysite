from django.shortcuts import render

from .models import Question


# Create your views here.
def index(request):
    questions = Question.objects.order_by('-create_date')  # - 가 있으면 내림차순 desc, 없으면 오름차순 asc
    context = {'questions': questions}
    return render(request, 'pybo/questions.html', context)
