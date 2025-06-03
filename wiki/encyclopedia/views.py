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
    # Get all entries and the search query
    all_entries = util.list_entries()
    query = request.GET.get("q", "").strip()
    
    # If no query is provided, show all entries with a message
    if not query:
        return render(request, "encyclopedia/search_results.html", {
            "query": "",
            "entries": all_entries,
            "message": "Please enter a search term or browse all entries below"
        })
    
    # Case-insensitive search
    entries_lower = [e.lower() for e in all_entries]
    query_lower = query.lower()
    
    # Exact match (with original case)
    if query_lower in entries_lower:
        original_case = all_entries[entries_lower.index(query_lower)]
        return entry(request, original_case)
    
    # Partial matches
    matching_entries = [entry for entry in all_entries 
                       if query_lower in entry.lower()]
    
    if matching_entries:
        return render(request, "encyclopedia/search_results.html", {
            "query": query,
            "entries": matching_entries
        })
    
    # No matches found
    return render(request, "encyclopedia/entry.html", {
        "message": f"No entries found for '{query}'.",
        "title": "Search Results"
    })

def edit(request, title):
    pass


