from django.template import Library
from types import FunctionType
register = Library()


def table_body(result_list, list_display, wind_object):
    for result in result_list:
        # yield \
        #     [name(wind_object, result) if isinstance(name, FunctionType)
        #         else getattr(result, name)
        #             for name in list_display
        #     ]

        if list_display == '__all__':
            yield [str(result), ]
        else:
            tmp = []
            print(list_display)
            for name in list_display:
                if isinstance(name, FunctionType):
                    tmp.append(name(wind_object, result))
                else:
                    result_attr = getattr(result, name)
                    if isinstance(result_attr, str) and len(result_attr) > 30:
                        result_attr = result_attr[:30] + '......'
                    tmp.append(result_attr)
            yield tmp


def table_head(list_display, wind_object):
    if list_display == "__all__":
        yield "对象列表"
    else:
        for item in list_display:
            if isinstance(item, FunctionType):
                yield item(wind_object, wind_object, True)
            else:
                yield wind_object.model_class._meta.get_field(item).verbose_name



@register.inclusion_tag("md.html")
def get_result(base_dir, result_list, list_display, wind_object):
    table_body_data = table_body(result_list, list_display, wind_object)
    table_head_data = table_head(list_display, wind_object)
    return {
        "table_body_data": table_body_data,
        "table_head_data": table_head_data
    }