from django.http import HttpResponse, Http404
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "sp/index.html")

texts = ["something 1",
         "something 2",
         "something 3"]

def section(request, num):
    if 1 <= num <=3:
        return HttpResponse(texts[num-1])
    else:
        raise Http404("No such section")