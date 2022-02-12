from django.contrib.auth.models import User
from .models import BaseRegisterForm
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import View

class BaseRegisterView(CreateView):
    model = User  # модель формы, которую реализует данный дженерик;
    form_class = BaseRegisterForm  # форма, которая будет заполняться пользователем;
    success_url = '/'  # URL, на который нужно направить пользователя после успешного ввода данных в форму.


# @login_required
# def upgrade_me(request):
#     user = request.user
#     premium_group = Group.objects.get(name='premium')
#     if not request.user.groups.filter(name='premium').exists():
#         premium_group.user_set.add(user)
#     return redirect('/')

@login_required
def become_author(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')

@login_required
def not_author(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if request.user.groups.filter(name='authors').exists():
        authors_group.user_set.remove(user)
    return redirect('/')


class MyView(PermissionRequiredMixin, View):
    permission_required = ('<app>.<action>_<model>',
                           '<app>.<action>_<model>')


class AddPost(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    # // customize form view

