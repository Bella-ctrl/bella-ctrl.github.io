from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request):
    entry = ut
    return render()
#def greet(request, name):
    #return render(request, "hello/greet.html", {
        #"name": name.capitalize()
    #})