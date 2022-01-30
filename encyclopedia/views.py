from django.shortcuts import render
from . import util
from markdown import markdown
from django.http import HttpResponseRedirect
from django.urls import reverse

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "searching": False
    })

def entry(request, title):
    entry = util.get_entry(title)
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

def search(request):
    search = request.GET.get("q","")
    entry = util.get_entry(search)
    if entry is None:
        entry_titles = []
        for title in util.list_entries():
            if search.lower() in title.lower():
                entry_titles.append(title)
        return render(request, "encyclopedia/index.html", {
            "entries": entry_titles,
            "searching": True,
            "value": search
        })
    else:
        return HttpResponseRedirect(reverse("entry", kwargs={"title": search }))
