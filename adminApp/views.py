from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.models import User
from mainApp.models import Gem
from userManagementApp.forms import MyRegistrationForm, UserChangeForm
from mainApp.forms import GemsForm
from django.http import Http404, JsonResponse
from django.template import loader
from django.template.context_processors import csrf
from django.contrib.auth.decorators import user_passes_test


# доступ у админке только суперпользователю
# @user_passes_test(lambda u: u.is_superuser)
def admin_page(request):
    users = User.objects.all()
    user_form = MyRegistrationForm()

    return render(request, 'admin_page.html', {'objects': users, 'form': user_form,
                                               'object_type': 'user'})


# FIXME: Убрать. Дубликат admin_page()
def admin_gems(request):
    gems = Gem.objects.all()
    gem_form = GemsForm()

    return render(request, 'admin_page.html', {'objects': gems, 'form': gem_form,
                                               'object_type': 'gem'})


# TODO: сделать универсальной функцию. Самостоятельно!
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return HttpResponseRedirect('/admin')


def get_form(request, object_id, object_form=None):
    """
    Возвращает заполненную форму для редактирования Пользователя(User) с заданным user_id
    """
    if request.is_ajax():
        object = get_object_or_404(object_form.Meta.model, id=object_id)
        object = object_form(instance=object)
        context = {'form': object, 'id': object_id}
        context.update(csrf(request))
        html = loader.render_to_string('inc-registration_form.html', context)
        # TODO: рассказать причину плохого использования!
        data = {'errors': False, 'html': html}
        return JsonResponse(data)
    raise Http404


# # FIXME: Убрать. Дубликат get_user_form()
# def get_gem_form(request, gem_id):
#     """
#     Возвращает заполненную форму для редактирования Gem с заданным gem_id
#     """
#     if request.is_ajax():
#         gem = get_object_or_404(User, id=gem_id)
#         gem_form = GemsForm(instance=gem)
#         context = {'form': gem_form, 'id': gem_id}
#         context.update(csrf(request))
#         html = loader.render_to_string('inc-gems_form.html', context)
#         data = {'errors': False, 'html': html}
#         return JsonResponse(data)
#     raise Http404


# def create_user(request, user_id=None):
#     """
#     Создает Пользователя(User)
#     Или редактирует существующего, если указан  user_id
#     """
#     if request.is_ajax():
#         # print('user_id = ', user_id)
#         if not user_id:
#             # print('Not user_id')
#             user = MyRegistrationForm(request.POST)
#         else:
#             user = get_object_or_404(User, id=user_id)
#             user = UserChangeForm(request.POST or None, instance=user)
#         if user.is_valid():
#             user.save()
#             users = User.objects.all()
#             html = loader.render_to_string('inc-users_list.html', {'users': users}, request=request)
#             data = {'errors': False, 'html': html}
#             return JsonResponse(data)
#         else:
#             errors = user.errors.as_json()
#             return JsonResponse({'errors': errors})
#
#     raise Http404


def create_object(request, object_id=None, object_form=None):
    """
    Создает Пользователя(User)
    Или редактирует существующего, если указан  user_id
    """
    if request.is_ajax():
        # print('object_form = ', object_form)
        # print('object_id = ', object_id)
        if not object_id:
            # print('Not object_id')
            # print('files = ', request.FILES)
            object = object_form(request.POST, request.FILES)
        else:
            object = get_object_or_404(object_form.Meta.model, id=object_id)
            object = object_form(request.POST or None, instance=object)
        if object.is_valid():
            object.save()
            objects = object.Meta.model.objects.all()
            html = loader.render_to_string('inc-objects_list.html',
                                           {'objects': objects}, request=request)
            data = {'errors': False, 'html': html}
            return JsonResponse(data)
        else:
            errors = object.errors.as_json()
            return JsonResponse({'errors': errors})

    raise Http404

# Demo-views
# def send_json(request):
#     # Если данные были отправлены ajax'ом
#     if request.is_ajax():
#         # Данные хранятся также в атрибуте POST или GET, в зависимости от методы отправки данных
#         request_data = request.POST
#         # Словарик при отправке автоматически будет преобразован к json
#         send_data = {'key': 'value'}
#         return JsonResponse(send_data)
#     raise Http404


