"""Gems URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from mainApp.views import *
from userManagementApp.views import *
from adminApp.views import *
from userManagementApp.forms import MyRegistrationForm, UserChangeForm
from mainApp.forms import GemsForm

# site
urlpatterns = [
    url(r'^$', listing),
]

# user management
urlpatterns += [
    url(r'^user/login/$', login),
    url(r'^user/logout/$', logout),
    url(r'^user/registration/$', registration),
]

# admin
urlpatterns += [
    # url(r'^admin/$', admin_page),
    url(r'^admin/gems/$', GemView.as_view()),
    url(r'gem/get_form/(\d*)$', GemView.get_form),
    url(r'gem/create/(\d*)$', GemView.as_view()),
    url(r'gem/delete/(\d+)$', GemView.as_view()),
]
# Данный подход нерекомендуется, и будет убран в django 1.10
# urlpatterns = patterns('mainApp.views',
#     url(r'^$', 'main'),
# )
