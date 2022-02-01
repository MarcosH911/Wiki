from . import util
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from markdown2 import Markdown
from random import randint


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
    markdown = Markdown()
    entry = util.get_entry(title)
    if entry is None:
        return render(request, "encyclopedia/entryNotFound.html", {
            "title": title
    })
    else:
        entry = markdown.convert(entry)
        print(entry)
        return render(request, "encyclopedia/entry.html", {
            "title": title.capitalize(), "entry": entry
    })


def newEntry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if not util.get_entry(title) or form.cleaned_data["edit"]:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("entry", kwargs={"title": title}))
            else:
                return render(request, "encyclopedia/newEntry.html", {
                    "form": form,
                    "existing": True,
                    "title": title
                })

    else:
        return render(request, "encyclopedia/newEntry.html", {
            "form": NewEntryForm,
            "existing": False
        })


def editEntry(request, title):
    entry = util.get_entry(title)
    if not entry:
        return render(request, "encyclopedia/newEntry.html", {"title": title})
    else:
        form = NewEntryForm()
        form.fields["title"].initial = title
        form.fields["title"].widget = forms.HiddenInput()
        form.fields["content"].initial = entry
        form.fields["edit"].initial = True
        return render(request, "encyclopedia/newEntry.html", {
            "title": title,
            "form": form,
            "edit": True
        })

def searchEntry(request):
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


def randomEntry(request):
    entries = util.list_entries()
    n = randint(0, len(entries) - 1)
    return HttpResponseRedirect(reverse("entry", kwargs={"title": entries[n]}))