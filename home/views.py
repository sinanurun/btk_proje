from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse

from home.models import Setting


# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")
def index(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting}
    return render(request, 'index.html', context)

# def detail(request, question_id):
#     return HttpResponse("You're looking at question %s." % question_id)
# def results(request, question_id):
#     response = "You're looking at the results of question %s."
#     return HttpResponse(response % question_id)
# def vote(request, question_id):
#     return HttpResponse("You're voting on question %s." % question_id)