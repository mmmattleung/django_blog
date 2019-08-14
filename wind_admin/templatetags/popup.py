#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.template import Library
from django.forms import ModelChoiceField
from django.urls import reverse
from wind_admin.wind_core import site


register = Library()

@register.inclusion_tag('popup.html')
def add_list(form):
    # from django.forms.boundfield import BoundField
    # from django.db.models.fields.related_descriptors import ManyToManyDescriptor, ForwardManyToOneDescriptor
    # for item in form["m"]:
    #     pop_dict = {'item': None, 'is_pop': False, 'pop_url': None}
    #     print(type(item.field), item.field)
    #     if type(item.field) == MultipleChoiceField:
    #         # eval("print(form['mc']." + item.name + ".through._meta.app_label)")
    #         # eval("print(form['mc']." + item.name + ".through._meta.model_name)")
    #
    #         pop_dict['item'] = item
    #         pop_dict['is_pop'] = True
    #
    #         base_url = reverse("{}:{}_{}_add".format(
    #             site.name_space,
    #             eval("form['mc']." + item.name + ".through._meta.app_label"),
    #             eval("form['mc']." + item.name + ".through._meta.model_name")
    #             )
    #         )
    #         pop_dict['pop_url'] = base_url
    #
    #     elif type(item.field) == ChoiceField:
    #
    #         # eval("print(form['mc']." + item.name + ".get_queryset().model._meta.app_label)"),
    #         pop_dict['item'] = item
    #         pop_dict['is_pop'] = True
    #
    #         base_url = reverse("{}:{}_{}_add".format(
    #             site.name_space,
    #             eval("form['mc']." + item.name + ".get_queryset().model._meta.app_label"),
    #             eval("form['mc']." + item.name + ".get_queryset().model._meta.model_name")
    #         )
    #         )
    #         pop_dict['pop_url'] = base_url
    #     else:
    #         pop_dict['item'] = item
    #     form_list.append(pop_dict)
    form_list = []
    for item in form["m"]:
        row = {'is_popup': False, 'item': None, 'popup_url': None}
        if isinstance(item.field, ModelChoiceField) and item.field.queryset.model in site._register:
            target_app_label = item.field.queryset.model._meta.app_label
            target_model_name = item.field.queryset.model._meta.model_name
            url_name = "{0}:{1}_{2}_add".format(site.name_space, target_app_label, target_model_name)
            target_url = "{0}?popup={1}".format(reverse(url_name), item.auto_id)

            row['is_popup'] = True
            row['item'] = item
            row['popup_url'] = target_url
        else:
            row['item'] = item
        form_list.append(row)
    print("form_list", form_list)
    return {'form': form_list, "f": form["m"]}