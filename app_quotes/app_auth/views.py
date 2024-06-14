from django.http import HttpResponseNotAllowed
from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin

from django.urls import reverse_lazy
from .forms import RegisterForm


class RegisetrView(View):
    template_name = "app_auth/register.html"
    form_class = RegisterForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to="home")
        else:
            return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={"form": self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            messages.success(request, f"Registration user: {username} successfully")
            return redirect(to="app_auth:signin")
        return render(request, self.template_name, {"form": form})


class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        print("dispatch")
        if request.method != "POST":
            request.method = "POST"
            return super().dispatch(request, *args, **kwargs)

            # return HttpResponseNotAllowed(["POST"])
        return super().dispatch(request, *args, **kwargs)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = "app_auth/password_reset.html"
    email_template_name = "app_auth/password_reset_email.html"
    html_email_template_name = "app_auth/password_reset_email.html"
    success_url = reverse_lazy('app_auth:password_reset_done')
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
    subject_template_name = 'app_auth/password_reset_subject.txt'
