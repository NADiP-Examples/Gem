from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.models import User
from mainApp.models import Gem
from userManagementApp.forms import MyRegistrationForm, UserChangeForm
from mainApp.forms import GemsForm, CategoryForm
from django.http import Http404, JsonResponse
from django.template import loader
from django.template.context_processors import csrf
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.base import TemplateView, View


class BaseView(View):
    model = None
    model_form = None
    template_name = None
    url_prefix = ''

    def get(self, request, *args, **kwargs):
        context = kwargs
        objects = self.model.objects.all()
        context['objects'] = objects
        form = self.model_form()
        context['form'] = form
        context['url_prefix'] = self.url_prefix
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        id = args[0] if args else None
        print('files = ', request.FILES)
        if not id:
            form = self.model_form(data=request.POST or None, files=request.FILES)
        else:
            object = get_object_or_404(self.model, id=id)
            form = self.model_form(data=request.POST or None, files=request.FILES,
                                   instance=object)
        if form.is_valid():
            form.save()
            objects = self.model.objects.all()
            html = loader.render_to_string('inc-objects_list.html',
                                           {'objects': objects, 'url_prefix':self.url_prefix}, request=request)
            data = {'html': html}
            return JsonResponse(data)
        else:
            errors = form.errors.as_json()
            return JsonResponse({'errors': errors}, status=400)

    def delete(self, request, *args, **kwargs):
        print('delete')
        id = args[0]
        object = get_object_or_404(self.model, id=id)
        object.delete()
        objects = self.model.objects.all()
        html = loader.render_to_string('inc-objects_list.html',
                                       {'objects': objects, 'url_prefix': self.url_prefix}, request=request)
        data = {'html': html}
        return JsonResponse(data)

    @classmethod
    def get_form(cls, request, *args, **kwargs):
        """
        Возвращает заполненную форму для редактирования
        """
        context = kwargs
        form_context = {}
        form_context.update(csrf(request))
        if not request.is_ajax():
            raise Http404
        id = args[0] if args else None
        if id:
            object = get_object_or_404(cls.model, id=id)
            form = cls.model_form(instance=object)
            form_context['id'] = id
        else:
            form = cls.model_form()
        form_context['form'] = form
        form_context['url_prefix'] = cls.url_prefix
        form_context['category_form'] = CategoryForm()
        html = loader.render_to_string('inc-creation_form.html', form_context)
        context['html'] = html
        return JsonResponse(context)


class GemView(BaseView):
    model = Gem
    model_form = GemsForm
    template_name = 'admin_page.html'
    url_prefix = 'gem'


def category_create(request, id=None):
    if request.method != "POST":
        raise Http404
    form = CategoryForm(request.POST)
    if form.is_valid():
        print("form valid")
        form.save()
        return HttpResponseRedirect('/admin/gems/')
    print('form not valid')
