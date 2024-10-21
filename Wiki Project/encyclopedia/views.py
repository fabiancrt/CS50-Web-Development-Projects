from django.shortcuts import render,redirect
from django.http import Http404
#the markdown2 that the site provided
import markdown2
from . import util
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
import random


#i resubmitted this project because i made some noticeable visual improvements to the website

#i used some comments to make it easier for you guys in at the cs50 team to understand what's going on inside my code.
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
#this is my defined entry according to the specs from the cs50 website.. Entry Page: Visiting /wiki/TITLE, where TITLE is the title of an encyclopedia entry, should render a page that displays the contents of that encyclopedia entry.
#i did my view according to this : The view should get the content of the encyclopedia entry by calling the appropriate util function.
#P.S: now that i went back to it , i updated it for the markdown
def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "The requested page was not found."
        })
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": content
    })
    
#now the view i have to build in order for the search to work:
def search(request):
    query = request.GET.get('q', '')
    if util.get_entry(query):
        return redirect('entry', query)
    else:
        results = [entry for entry in util.list_entries() if query.lower() in entry.lower()]
        return render(request, "encyclopedia/search.html", {
            "results": results,
            "query": query
        })
    
#and now next on the list , New Page: Clicking “Create New Page” in the sidebar should take the user to a page where they can create a new encyclopedia entry.
#the newpage form creation
class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea, label="Content")
#next the view:
def new_page(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        #only for the completed form
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            #making sure there are no identic titles!
            if util.get_entry(title):
                return render(request, "encyclopedia/new_page.html", {
                    "form": form,
                    "error": "Entry already exists."
                })
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry", args=[title]))
    else:
        form = NewPageForm()
    return render(request, "encyclopedia/new_page.html", {
        "form": form
    })

#now let's move on to edit page : Edit Page: On each entry page, the user should be able to click a link to be taken to a page where the user can edit that entry’s Markdown content in a textarea.
#the form created:
class EditPageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label="Content")
#the view for the edit page:
def edit_page(request, title):
    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry", args=[title]))
    else:
        content = util.get_entry(title)
        
        if content is None:
            return render(request, "encyclopedia/error.html", {
                "message": "The requested page was not found."
            })
        form = EditPageForm(initial={'content': content})

    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "form": form
    })

#random page (the easiest of them all)
def random_page(request):
    entries = util.list_entries()
    if not entries:
        return render(request, "encyclopedia/error.html", {
            "message": "No entries found."
        })
    #used imported random to choose a random entry
    random_entry = random.choice(entries)
    return HttpResponseRedirect(reverse("entry", args=[random_entry]))