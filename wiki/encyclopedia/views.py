from django.http import Http404
from django.shortcuts import render, redirect

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, title): 
    content = util.get_entry
    if content(title):
        return render(request, "encyclopedia/entry.html", {                
            "title": title, 
            "content": content
        })
    if not content(title): 
        return Http404("Requested page was not found")

def search(request):
    query = request.GET.get('q', '').strip()
    entries = util.list_entries()

    if query.lower() in [entry.lower() for entry in entries]:
        exact_match = next(entry for entry in entries if entry.lower() == query.lower())
        return redirect('entry', title=exact_match)
    
    search_results = [entry for entry in entries if query.lower() in entry.lower()]
    return render(request, "encyclopedia/search_result.html", {
        "query": query,
        "result": search_results
    })
