from django.shortcuts import render
import markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry = util.get_entry(title)
    if entry is None:
        return render(request, "encyclopedia/entry.html", {
            "message": f" The requested entry '{title.upper()}' couldn't be found."
        })
    
    # Convert the Markdown Content to HTML
    html_content = markdown.markdown(entry)
    return render(request, "encyclopedia/entry.html", {
        "title": title.upper(),
        "content": html_content
    })

def search(request):
    entries = util.list_entries()
    query = request.GET.get("q", "").strip().lower()
    if query in entries:
        return entry(request, query)
    else:
        # Filter entries that contain the query
        matching_entries = [entry for entry in entries if query in entry.lower()]
        
        return render(request, "encyclopedia/search_results.html", {
            "query": query,
            "entries": matching_entries
        }) if matching_entries else render(request, "encyclopedia/entry.html", {
            "message": f"No entries found for '{query}'."
        })
    

