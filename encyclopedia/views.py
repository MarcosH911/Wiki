from django.shortcuts import render
from . import util
from markdown import markdown


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry = util.get_entry(title)
    print(entry)
    if entry is None:
        return render(request, "encyclopedia/EntryNotFound.html", {
            "title": title
    })
    else:
        entry = markdown(entry)
        print(entry)
        return render(request, "encyclopedia/entry.html", {
            "title": title.capitalize(), "entry": entry
    })