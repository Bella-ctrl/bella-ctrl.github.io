from django.contrib import messages
from django.http import Http404
from django import forms
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
import markdown2
import random

from . import util

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100)
    content = forms.CharField(label="Content", widget=forms.Textarea)

class EditPageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, title): 
    content = util.get_entry(title)
    if content is None:
        return Http404("Requested page was not found")
    
    html_content = markdown2.markdown(content)

    return render(request, "encyclopedia/entry.html", {                
        "title": title, 
        "content": html_content
    })

def search(request):
    query = request.GET.get('q', '').strip().lower()  
    entries = util.list_entries()
    
    for entry in entries:
        if query == entry.lower():
            return redirect('wiki', title=entry)  
    
    search_results = [
        entry for entry in entries 
        if query in entry.lower()
    ]
    
    return render(request, "encyclopedia/search_results.html", {
        "query": query,
        "results": search_results
    })

def new_page(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']

            existing_entries = util.list_entries()
            if any(title.lower() == entry.lower() for entry in existing_entries):
                messages.error(request, F"An entry with the title '{title}' already exists.")
            else:
                util.save_entry(title, content)
                return redirect(reverse('entry', kwargs={"title": title}))
    else:
        form = NewPageForm()
    
    return render(request, "encyclopedia/new_page.html", {
        "form": form
    })

def edit_page(request, title):
    content = util.get_entry(title)
    if content is None:
        raise Http404("Entry not found")

    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            new_content = form.cleaned_data["content"]
            util.save_entry(title, new_content)
            return redirect("entry", title=title)
    else:
        form = EditPageForm(initial={"content": content})
    
    return render(request, "encyclopedia/edit_page.html", {
        "form": form,
        "title": title
    })

def random_page(request):
    entries = util.list_entries()
    if not entries:
        raise Http404("No entries exist yet")
    random_entry = random.choice(entries)
    return redirect("entry", title=random_entry)