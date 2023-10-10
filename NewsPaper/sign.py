from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import CreateView
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .forms import LoginForm, RegisterForm

######################################################################################################################


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'sign/register.html'
    success_url = '/'

    def form_valid(self, form):
        user = form.save()
        group, created = Group.objects.get_or_create(name='common')
        user.groups.add(group)
        # user.fi
        user.save()
        html = render_to_string(
            'mail/register.html',
            {
                'user': user,
                'site_url': self.request.build_absolute_uri(reverse('index'))
            },
        )
        msg = EmailMultiAlternatives(
            subject=f'Регистрация на сайте "Газета"',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email, ],
        )
        msg.attach_alternative(html, 'text/html')

        try:
            msg.send()
        except Exception as e:
            print(e)

        return super().form_valid(form)


######################################################################################################################


class LoginView(FormView):
    model = User
    form_class = LoginForm
    template_name = 'sign/login.html'
    success_url = '/'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


######################################################################################################################


class LogoutView(LoginRequiredMixin, TemplateView):
    template_name = 'sign/logout.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


######################################################################################################################
