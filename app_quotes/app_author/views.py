import re
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.views import View
from .models import Author
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import AuthorForm
from django.http import Http404, HttpResponseNotAllowed

# Create your views here.


def convert_link_to_fullname(name):
    parts = name.split("-")
    result = ""
    for i in range(len(parts)):
        if len(parts[i]) <= 2:
            result += parts[i] + "."
            if len(parts) > (i + 1) and len(parts[i + 1]) > 2:
                result += " "
        else:
            result += parts[i] + " "
    result = result.strip()
    print(f"result: {result}")
    return result


def get_author(request, author_name=None):
    fullname = convert_link_to_fullname(author_name)
    print(f"{author_name} -> {fullname}")
    author = get_object_or_404(Author, fullname=fullname)
    print(author.fullname)

    return render(request, "app_author/author.html", context={"author": author})


class AuthorListView(LoginRequiredMixin, ListView):
    model = Author
    template_name = "app_author/author_list.html"
    context_object_name = "authors"
    paginate_by = 30
    ordering = ["fullname"]


class AuthorCreateView(LoginRequiredMixin, CreateView):
    model = Author
    form_class = AuthorForm
    template_name = "app_author/author_form.html"
    success_url = reverse_lazy("app_author:author_list")


class AuthorUpdateView(LoginRequiredMixin, UpdateView):
    model = Author
    form_class = AuthorForm
    template_name = "app_author/author_form.html"
    success_url = reverse_lazy("app_author:author_list")


class AuthorDeleteView(LoginRequiredMixin, DeleteView):
    model = Author
    template_name = "app_author/author_confirm_delete.html"
    success_url = reverse_lazy("app_author:author_list")


class AuthorView(View):
    template_name = "app_author/author_form.html"

    def get(self, request, pk=None):
        if pk:
            print(f"pk: {pk}")
            author = get_object_or_404(Author, pk=pk)
            print(f"author fullname: {author.fullname}")
            form = AuthorForm(instance=author)
        else:
            form = AuthorForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, pk=None):
        print(f"----- Request method: {request.method}")
        if pk:
            author = get_object_or_404(Author, pk=pk)
            form = AuthorForm(request.POST, instance=author)
        else:
            form = AuthorForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(to="app_author:author_list")
        return render(request, self.template_name, {"form": form})

    def delete(self, request, pk):
        print("!!!!!!! - DELETE")
        if request.method != "DELETE":
            return HttpResponseNotAllowed(["DELETE"])
        author = get_object_or_404(Author, pk=pk)
        author.delete()
        return redirect("app_author:author_list")
