import random
from markdown2 import Markdown
from django.shortcuts import render
from django.http import HttpResponse
from django import forms 

from . import util

class SearchForm(forms.Form):
	search = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))

class CreateForm(forms.Form):
	create = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Title'}))
	
class TextForm(forms.Form):	
	textarea = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': 'Markdown content'}))
	

mark = Markdown()

global gb_test

gb_test = False

def index(request):
	gb_test = False
	if request.method == "POST":
		form = SearchForm(request.POST)
		if form.is_valid():
			substr = []
			check_substr = True
			gb_test = True
			pr_test = False
			search = form.cleaned_data["search"]
			for entry in util.list_entries():
				if search.lower() == entry.lower():
					pr_test = True
					search = entry
					gb_title = entry
			if not pr_test:
				for entry in util.list_entries():
					if search.lower() in entry.lower():
						substr.append(entry)
			if pr_test:
				return render(request, "encyclopedia/entries.html", {
					"titles": mark.convert(util.get_entry(search)),
					"form": SearchForm(),
					"substr": substr,
					"check_substr": check_substr,
					"pr_test": pr_test,
					"title": search
					})
			else:
				if len(substr)==0: 
					return render(request, "encyclopedia/error_404.html", {
						"form": SearchForm(),
						"pr_test": pr_test
						})
				return render(request, "encyclopedia/index.html", {
					"form": SearchForm(),
					"entries": substr,
					"pr_test": pr_test
					})

	else:
	    return render(request, "encyclopedia/index.html", {
	        "entries": util.list_entries(),
	        "form": SearchForm(),
	        "test": False
	    })


def create(request):
	if request.method == "POST":
		form = CreateForm(request.POST)
		frm = TextForm(request.POST)
		if form.is_valid() and frm.is_valid():
			exist = False
			create = form.cleaned_data["create"]
			textarea = frm.cleaned_data["textarea"]
			for entry in util.list_entries():
				if entry.lower()==create: exist = True
			if exist:
				return render(request, "encyclopedia/error.html", {
					"form": SearchForm()
					})
			util.save_entry(create, textarea)
			return render(request, "encyclopedia/entries.html", {
				"create": CreateForm(),
				"form": SearchForm(),
				"area": TextForm(),
				"exist": exist,
				"title": create,
				"titles": mark.convert(textarea)
				})
	else:
		return render(request, "encyclopedia/create.html", {
				"create": CreateForm(),
				"form": SearchForm(),
				"area": TextForm()
			})


def wiki(request, title):
	test = True
	for entry in util.list_entries():
		if entry.lower() == title.lower():
			title = entry
			gb_title = entry
			test = False
	if test:
		return render(request, "encyclopedia/error_404.html", {
			"form": SearchForm()
			})

	return render(request, "encyclopedia/entries.html", {
			"form": SearchForm(),
			"titles": mark.convert(util.get_entry(title)),
			"title": title,
			"test": util.get_entry(title)==None,
			"gb_test": gb_test
		})

def edit(request, title):
	if request.method == "GET":
		entry = util.get_entry(title)
		return render(request, "encyclopedia/edit.html", {
			"form": SearchForm(),
			"area": TextForm(initial={'textarea': entry}),
			"title": title,
			"search": CreateForm(initial={'create': title})
			})
	else:
		form = TextForm(request.POST)
		if form.is_valid():
			entry = form.cleaned_data["textarea"]
			util.save_entry(title, entry)
			return render(request, "encyclopedia/entries.html", {
				"form": SearchForm(),
				"titles": mark.convert(entry),
				"title": title
				})

def randomPage(request):
	num = len(util.list_entries())
	rnd = random.randint(0, num-1)
	title = util.list_entries()[rnd]
	entry = util.get_entry(title)
	return render(request, "encyclopedia/newentry.html", {
		"form": SearchForm(),
		"titles": mark.convert(entry),
		"title": title
		})




