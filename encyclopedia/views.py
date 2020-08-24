import random
import markdown2

from django import forms
from . import util
from django.shortcuts import render, redirect


class NewPageForm(forms.Form):
    page_title = forms.CharField(label = "New Page") 
    page_content = forms.CharField(widget= forms.Textarea, label=" Content")

class EditPageForm(forms.Form):
    page_content = forms.CharField(widget= forms.Textarea, label=" Content")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_check(request, entry):
    content = util.get_entry(entry)
    if entry in util.list_entries():
        return render(request, "encyclopedia/wiki_entry.html", {
                "entry": entry, "content": markdown2.markdown(content)
            })

    else:
        return render(request, "encyclopedia/error_message.html", {
                "entry": entry
            }) 

def random_page(request):
    entries = util.list_entries()
    no_entries = len(entries)
    rand_entry = random.randrange(no_entries)
    return redirect(entry_check, entries[rand_entry])

def new_page(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["page_title"] not in util.list_entries():
                title = form.cleaned_data["page_title"]
                content = form.cleaned_data["page_content"]
                util.save_entry(title, content)
                return entry_check(request, title)

            else:
                return render(request, "encyclopedia/New_page.html", {
                "form": form
            })

    else: 
        return render(request, "encyclopedia/New_page.html", {
        "form": NewPageForm()
            })

def edit_page(request, entry):
    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["page_content"]
            util.save_entry(entry, content)
            return redirect('entry_check', entry)
        else:
            return render(request, "encyclopedia/edit_page.html", {
                "form": form,
                "title": entry
            })

    else:
        content = util.get_entry(entry)
        return render(request, "encyclopedia/edit_page.html", {
            "form": EditPageForm(initial={'page_content': content}),
            "title": entry
        })

def search_pages(request):
    if request.method == 'GET':
        search_query = request.GET.get('search', None)
        entries = util.list_entries()
        if search_query in entries:
            return redirect('entry_check', search_query)
        
        else:
            matches = []
            for i in entries:
                if search_query in i:
                    matches.append(i)
            return render(request, "encyclopedia/search_results.html", {
            "search_input": search_query,
            "matches": matches
        })
        
        '''else:
            return render(request, "encyclopedia/error_message.html", {
                "entry": search_query
            }) '''
    