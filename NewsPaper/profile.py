from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, reverse
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from NewsPaper.models import Author

######################################################################################################################


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Профиль позователя {self.request.user}'
        context['author'] = self.request.user.groups.filter(name='authors').exists()
        return context


######################################################################################################################


@login_required
def upgrade_me(request):
    user = request.user
    premium_group, created = Group.objects.get_or_create(name='authors')
    if created:
        premium_group.save()
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
        author, created = Author.objects.get_or_create(user=user)
        if created:
            author.save()
    return redirect(reverse('profile'))


######################################################################################################################
