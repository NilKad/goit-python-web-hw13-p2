import re
from django.urls import reverse_lazy
from django.shortcuts import render, HttpResponse, redirect
from django.core.paginator import Paginator
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse
from .models import Quote
from .forms import QuoteForm


def convert_fullname_to_link(name):
    result = re.sub(r"\.\s|\s|\.", "-", name)
    # print(f"result: '{result}'")
    return result


# TODO: это можно будет удалить
def index(request):
    quotes = Quote.objects.order_by("id").all()
    page_number = request.GET.get("page")
    per_page = request.GET.get("per_page")
    print(f"GET {request.path}")
    print(f"GET {request.path_info}")
    if not per_page:
        per_page = 10
    is_edit = False
    if request.path == "/quotes/":
        is_edit = True
        per_page = 30
    paginator = Paginator(quotes, per_page)

    # Создание ссылки для старницы автора из fullname
    for quote in quotes:
        quote.tags = quote.tags.split(",")
        fullname_uri = convert_fullname_to_link(quote.author.fullname)
        quote.author_detail_url = f"author/{fullname_uri}"

    page_obj = paginator.get_page(page_number)

    if is_edit:
        return render(request, "app_quotes/quotes_list.html", {"page_obj": page_obj})
    else:
        return render(request, "app_quotes/index.html", {"page_obj": page_obj})


class QuoteListView(ListView):
    model = Quote
    context_object_name = "quotes"
    ordering = ["id"]

    def get_queryset(self):
        queryset = super().get_queryset()
        author_id = self.request.GET.get("author_id")
        tag = self.request.GET.get("tag")
        if author_id:
            queryset = queryset.filter(author_id=author_id)
        if tag:
            queryset = queryset.filter(tags__icontains=tag)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for quote in context["quotes"]:
            quote.tag_list = quote.tags.split(",")
            fullname_uri = convert_fullname_to_link(quote.author.fullname)
            quote.author_detail_url = f"author/{fullname_uri}"

        return context

    def get_template_names(self):
        if self.request.user.is_authenticated and self.request.path == reverse(
            "quote_list"
        ):
            return "app_quotes/quotes_list.html"
        else:
            return "app_quotes/index.html"

    def get_paginate_by(self, queryset):
        if self.request.path == reverse("quote_list"):
            return 30
        else:
            return 10


class QuoteCreateView(LoginRequiredMixin, CreateView):
    model = Quote
    form_class = QuoteForm
    template_name = "app_quotes/quote_form.html"
    success_url = reverse_lazy("quote_list")


class QuoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Quote
    form_class = QuoteForm
    template_name = "app_quotes/quote_form.html"
    success_url = reverse_lazy("quote_list")


class QuoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Quote
    template_name = "app_quotes/quote_confirm_delete.html"
    success_url = reverse_lazy("quote_list")


def custom_404_view(request, exception):
    return render(
        request, "app_quotes/404.html", status=404, context={"exception": exception}
    )
