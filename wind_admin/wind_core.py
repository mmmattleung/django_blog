#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.shortcuts import render, HttpResponse
from repository.forms import LoginForm
from rbac import models as rbac_models
from blog import settings
from rbac.service import initial_permission


class BaseWind:

    list_display = "__all__"

    def __init__(self, model_class, site_object):
        self.model_class = model_class
        self.site_object = site_object
        self.app_label = model_class._meta.app_label
        self.model_name = model_class._meta.model_name

    @property
    def urls(self):
        return self.get_urls()

    def get_urls(self):
        info = self.app_label, self.model_name
        urlpatterns = [
            url(r'^$', self.changelist_view, name='%s_%s_changelist' % info),
            url(r'^add/$', self.add_view, name='%s_%s_add' % info),
            url(r'^(\d+)/change/$', self.change_view, name='%s_%s_change' % info),
            url(r'^(\d+)/delete/$', self.delete_view, name='%s_%s_delete' % info),
        ]
        # urlpatterns += self.another_urls
        return urlpatterns

    def changelist_view(self, request):
        self.request = request
        result_list = self.model_class.objects.all()
        context = {
            'base_dir': settings.BASE_HOST,
            'result_list': result_list,
            'list_display': self.list_display,
            "wind_object": self
        }
        return render(request, "changelist.html", context)

    def add_view(self, request):
        return HttpResponse("add")

    def change_view(self, request, pk):
        return HttpResponse("change")

    def delete_view(self, request, pk):
        return HttpResponse("delete")


class WindSite:
    def __init__(self):
        self._register = {}
        self.name_space = "wind"
        self.app_name = "wind"

    @property
    def urls(self):
        return self.get_urls(), self.app_name, self.name_space

    def get_urls(self):
        urlpatterns = [
            url(r'^login$', self.login, name='login'),
            url(r'^logout', self.logout, name='login'),
        ]

        for model_class, base_object in self._register.items():
            self.base_obj = base_object
            self.model_name = model_class._meta.model_name
            self.app_label = model_class._meta.app_label
            urlpatterns.append(url(r'%s/%s/' % (self.app_label, self.model_name), include(base_object.urls)))
        return urlpatterns

    def register(self, model_class, base_class=BaseWind):
        self._register[model_class] = base_class(model_class, self)

    def login(self, request, *args, **kwargs):
        if request.method == "GET":
            form = LoginForm(request)
            return render(request, 'login.html', {"form": form})
        else:
            form = LoginForm(request, request.POST)
            if form.is_valid():
                username = request.POST.get('userinfo_name')
                password = request.POST.get('userinfo_password')
                user = rbac_models.User.objects.filter(username=username, password=password).first()
                if user:
                    initial_permission(request, user)
                return render(request, "backend_index.html")
            else:
                print(form.errors)
                return render(request, 'login.html', {"form": form})

    def logout(self, request, *args, **kwargs):
        pass


site = WindSite()
