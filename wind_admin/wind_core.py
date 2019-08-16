#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.core.files.uploadedfile import InMemoryUploadedFile
import copy
from utils import pager
from django.db.models import QuerySet
from django.urls import reverse
from django.conf.urls import url, include
from django.http.request import QueryDict
from django.forms.models import model_to_dict
from django.shortcuts import render, HttpResponse, redirect

from repository.forms import LoginForm
from rbac import models as rbac_models
from blog import settings
from rbac.service import initial_permission
from utils.filter_code import FilterList, FilterOption


class BaseWind:

    list_display = "__all__"

    action_list = []

    filter_list = []

    add_or_edit_model_form = None

    def __init__(self, model_class, site_object):
        self.model_class = model_class
        self.site_object = site_object
        self.app_label = model_class._meta.app_label
        self.model_name = model_class._meta.model_name

    def get_add_or_edit_model_form(self):
        if self.add_or_edit_model_form:
            return self.add_or_edit_model_form
        else:
            from django.forms import ModelForm

            def create_dynamic_model_form(model_class):
                '''动态生成modelform'''
                class Meta:
                    model = model_class
                    fields = "__all__"

                def __new__(cls, *args, **kwargs):
                    for field_name in cls.base_fields:

                        filed_obj = cls.base_fields[field_name]
                        # 添加属性
                        filed_obj.widget.attrs.update({'class': 'form-control'})

                    return ModelForm.__new__(cls)

                dynamic_form = type("DynamicModelForm", (ModelForm,), {'Meta': Meta, '__new__': __new__})

                return dynamic_form

            return create_dynamic_model_form(self.model_class)

    @property
    def urls(self):
        return self.get_urls()

    def changelist_view(self, request):
        # 保留 GET 参数
        self.request = request
        param_dict = QueryDict(mutable=True)
        condition = {}
        if request.GET:
            param_dict['_changelistfilter'] = request.GET.urlencode()
            r = copy.deepcopy(request.GET)
            r._mutable = True
            if r.get("page"):
                r.pop("page")
            condition = r
        # add 按钮 URL
        base_add_url = reverse("{2}:{0}_{1}_add".format(self.app_label, self.model_name, self.site_object.name_space))
        add_url = "{0}?{1}".format(base_add_url, param_dict.urlencode())

        # action
        action_list = []
        for item in self.action_list:
            tpl = {'name': item.__name__, 'text': item.text}
            action_list.append(tpl)
        if request.method == 'POST':
            # 1. 获取action
            func_name_str = request.POST.get('action')
            ret = getattr(self, func_name_str)(request)
            action_page_url = reverse(
                "{2}:{0}_{1}_changelist".format(self.app_label, self.model_name, self.site_object.name_space))
            if ret:
                action_page_url = "{0}?{1}".format(action_page_url, request.GET.urlencode())
            return redirect(action_page_url)

        # filter
        from utils.filter_code import FilterList
        filter_list = []
        for option in self.filter_list:
            if option.is_func:
                data_list = option.field_or_func(self, option, request)
            else:
                from django.db.models import ForeignKey, ManyToManyField
                field = self.model_class._meta.get_field(option.field_or_func)
                if isinstance(field, ForeignKey):
                    data_list = FilterList(option, field.rel.model.objects.all(), request)
                elif isinstance(field, ManyToManyField):
                    data_list = FilterList(option, field.rel.model.objects.all(), request)
                else:
                    data_list = FilterList(option, field.model.objects.all(), request)

            filter_list.append(data_list)

        # page

        fields = [item.name for item in self.model_class._meta._get_fields()]
        q = {}
        for k in condition:
            if k not in fields:
                continue
            q[k + '__in'] = condition.getlist(k)
        result_list = self.model_class.objects.filter(**q)
        # print(">" * 10, result_list)
        if q:
            # If has "q", request.GET dict must be removed the key of "page"
            rg = request.GET
            rg._mutable = True
            if rg.get("page"):
                del rg["page"]

        if result_list:
            ps, object_list = pager.get_pager(self, request, result_list, 5)
        else:
            ps = None
            object_list = []

        context = {
            'base_dir': settings.BASE_HOST,
            'result_list': object_list,
            'list_display': self.list_display,
            "wind_object": self,
            "add_url": add_url,
            "ps": ps,
            'action_list': action_list,
            "filter_list": filter_list,
        }
        return render(request, "changelist.html", context)

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

    def add_view(self, request):
        self.request = request
        if request.method == "GET":
            # form = self.get_add_or_edit_model_form(request)
            form = self.get_add_or_edit_model_form()()
            model_form_obj = form
        else:
            # form = self.get_add_or_edit_model_form(request, data=request.POST, files=request.FILES)
            form = self.get_add_or_edit_model_form()(data=request.POST, files=request.FILES)
            model_form_obj = form

            # print(request.POST.get('userfan_user'))
            # print(request.POST.get('userfan_follower'))
            # print("-" * 10)
            # print(model_form_obj.fields["userfan_user"].choices)
            # print(model_form_obj.fields["userfan_follower"].choices)
            if model_form_obj.is_valid():
                obj = model_form_obj.save(commit=False)
                obj.save()
                from django.db.models.fields.related_descriptors import ManyToManyDescriptor
                for key, value in form.cleaned_data.items():
                    if isinstance(getattr(self.model_class, key), ManyToManyDescriptor):
                        print(key, value)
                        if key == "tags":
                            data_dict = {
                                "article": obj,
                                "tag": None,
                            }
                        m2m_model = getattr(self.model_class, key).through
                        for item in value:
                            data_dict["tag"] = item
                            m2m_model.objects.create(**data_dict)

                # model_form_obj.save()
                # obj = model_form_obj.save(commit=False)
                # obj.save()
                #
                # from django.db.models.fields.related_descriptors import ManyToManyDescriptor
                # for key, value in form.cleaned_data.items():
                #     if isinstance(getattr(self.model_class, key), ManyToManyDescriptor):
                #         print(key, value)
                #         m2m_model = getattr(self.model_class, key).through
                #         for item in value:
                #             m2m_model.objects.filter(userfan_user=obj).all().delete()
                #             fans = m2m_model(userfan_user=obj, userfan_follower=item)
                #             fans.save()


                # process many to many field
                # for item in model_form_obj:
                #     print(type(item), item, item.field, type(item.field))
                #     # <class 'django.forms.fields.ChoiceField'>
                # many_to_many_dict = {}
                # for key, value in model_form_obj.cleaned_data.items():
                #     if isinstance(value, list):
                #         many_to_many_dict[key] = value
                #
                # for key in many_to_many_dict.keys():
                #     model_form_obj.cleaned_data.pop(key)
                #
                # for key, value in many_to_many_dict.items():
                #     eval("print(self.model_class." + key + ".through)")
                #
                # obj = self.model_class.objects.create(**model_form_obj.cleaned_data)
                # print(many_to_many_dict)
                # for key, value in many_to_many_dict.items():
                #     for i in value:
                #         eval("self.model_class."+key+".through.objects.create(userfan_user=obj, userfan_follower=self.model_class.objects.filter(pk=i).first())")

                popup_id = request.GET.get('popup')
                if popup_id:
                    context = {
                        'popup_dict': {
                            'popup_id': popup_id,
                            'text': str(obj),
                            'pk': obj.pk
                        }
                    }
                    return render(request, 'popup_response.html', context)

                base_list_url = reverse("{2}:{0}_{1}_changelist".format(self.app_label, self.model_name, self.site_object.name_space))
                list_url = "{0}?{1}".format(base_list_url, request.GET.get('_changelistfilter') )
                return redirect(list_url)

        context = {
            "form": {'m': model_form_obj, 'mc': self.model_class}
        }
        return render(request, "add.html", context)

    def change_view(self, request, pk):
        self.request = request
        obj = self.model_class.objects.filter(pk=pk).first()
        dict_of_obj = model_to_dict(obj)
        if not obj:
            return HttpResponse("No ID")

        # Need to iterate the queryset and change to list when the column type is many to many
        for key, value in dict_of_obj.items():
            if isinstance(value, QuerySet):
                change_to_list = []
                for i in value:
                    change_to_list.append(i.pk)
                dict_of_obj[key] = change_to_list

        if request.method == "GET":
            form = self.get_add_or_edit_model_form()(instance=obj)
            # form = self.get_add_or_edit_model_form(request, initial=dict_of_obj)
        elif request.method == "POST":
            # form = self.get_add_or_edit_model_form(request, data=request.POST, files=request.FILES, initial=dict_of_obj)
            form = self.get_add_or_edit_model_form()(data=request.POST, files=request.FILES, instance=obj)
            if form.is_valid():
                # for key, value in form.cleaned_data.items():
                #     if isinstance(value, InMemoryUploadedFile) or isinstance(value, TemporaryUploadedFile):
                #         file_dir = settings.AVATAR_DIRS[key]
                #         # save image
                #         file_obj = request.FILES.get(key)
                #         chunks = file_obj.chunks()
                #         with open(file_dir+"/"+str(value), "wb") as f:
                #             for item in chunks:
                #                 f.write(item)
                #
                #         form.cleaned_data[key] = file_dir+"/"+str(value)
                #
                # many_to_many_dict = {}
                # for key, value in form.cleaned_data.items():
                #     if isinstance(value, list):
                #         many_to_many_dict[key] = value
                #
                # for key in many_to_many_dict.keys():
                #     form.cleaned_data.pop(key)
                #
                # for key, value in many_to_many_dict.items():
                #     eval("print(self.model_class." + key + ".through)")
                #
                # self.model_class.objects.filter(pk=pk).update(**form.cleaned_data)
                #
                # # process many to many field
                # for key, value in many_to_many_dict.items():
                #     eval("self.model_class." + key + ".through.objects.filter(userfan_user=pk).delete()")
                #     for i in value:
                #         eval("self.model_class."+key+".through.objects.create(userfan_user=obj, userfan_follower=self.model_class.objects.filter(pk=i).first())")
                obj = form.save(commit=False)
                obj.save()

                from django.db.models.fields.related_descriptors import ManyToManyDescriptor
                for key, value in form.cleaned_data.items():
                    if isinstance(getattr(self.model_class, key), ManyToManyDescriptor):
                        m2m_model = getattr(self.model_class, key).through
                        for item in value:
                            m2m_model.objects.filter(userfan_user=obj).all().delete()
                            fans = m2m_model(userfan_user=obj, userfan_follower=item)
                            fans.save()

                base_list_url = reverse(
                    "{2}:{0}_{1}_changelist".format(self.app_label, self.model_name, self.site_object.name_space))
                list_url = "{0}?{1}".format(base_list_url, request.GET.get('_changelistfilter'))
                print(list_url)
                return redirect(list_url)

        context = {
            'form': form
        }
        return render(request, 'edit.html', context)

    def delete_view(self, request, pk):
        self.request = request
        obj = self.model_class.objects.filter(id=pk).delete()
        param_dict = QueryDict(mutable=True)
        base_add_url = reverse("{}:{}_{}_changelist".format(self.site_object.name_space, self.app_label, self.model_name))
        if not obj:
            return redirect(base_add_url)
        else:
            if request.GET:
                param_dict['_changelistfilter'] = request.GET.urlencode()
            change_list = "{}?{}".format(base_add_url, param_dict.urlencode())
            return redirect(change_list)


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
                print("bbbbb")
                return render(request, "backend_layout_1.html")
            else:
                print(form.errors)
                return render(request, 'login.html', {"form": form})

    def logout(self, request, *args, **kwargs):
        pass


site = WindSite()
