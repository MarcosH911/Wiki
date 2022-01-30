from django.shortcuts import render
from . import util
from markdown import markdown
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={"class": "form-control col-md-8 col-lg-8"}))
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={"class": "form-control col-md-8 col-lg-8"}))
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "searching": False
    })


def entry(request, title):
    entry = util.get_entry(title)
    if entry is None:
        return render(request, "encyclopedia/entryNotFound.html", {
            "title": title
    })
    else:
        entry = markdown(entry)
        print(entry)
        return render(request, "encyclopedia/entry.html", {
            "title": title.capitalize(), "entry": entry
    })


def newEntry(request):
    if request.method == "POST":
        pass

    else:
        return render(request, "encyclopedia/newEntry.html", {
            "form": NewEntryForm,
            "existing": False
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
