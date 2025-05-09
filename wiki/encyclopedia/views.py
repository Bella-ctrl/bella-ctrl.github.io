from django.http import Http404
from django.shortcuts import render, redirect
from django import forms
from django.urls import reverse
from django.contrib import messages

from . import util

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100)
    content = forms.CharField(label="Content", widget=forms.Textarea)

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
    query = request.GET.get('q', '').strip().lower()  
    entries = util.list_entries()
    
    for entry in entries:
        if query == entry.lower():
            return redirect('entry', title=entry)  
    
    search_results = [
        entry for entry in entries 
        if query in entry.lower()
    ]
    
    return render(request, "encyclopedia/search_results.html", {
        "query": query,
        "results": search_results
    })

def newPage(request):
    return render(request, "encyclopedia/newPage.html")