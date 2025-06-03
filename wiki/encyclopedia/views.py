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