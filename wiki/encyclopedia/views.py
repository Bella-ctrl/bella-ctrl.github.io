from django.http import Http404
from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, title): 
    content = util.get_entry
    if content():
        return render(request, "encyclopedia/entry.html", {                
            "title": title, 
            "content": content
        })
    if not content(): 
        return Http404("Requested page was not found")
