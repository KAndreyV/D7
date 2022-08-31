from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'

#     send_mail(
#         subject="Поздравляем, вы зарегистрировались на нашем сайте!",
#         # имя клиента и дата записи будут в теме для удобства
#         message="Добро пожаловать в наше сообщество",  # сообщение с кратким описанием проблемы
#         from_email='Qdim2002@yandex.ru',  # здесь указываете почту, с которой будете отправлять (об этом попозже)
#         recipient_list=[]  # здесь список получателей. Например, секретарь, сам врач и т. д.
#     )


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')