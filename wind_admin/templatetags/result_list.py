from django.template import Library
from types import FunctionType
register = Library()


def table_body(result_list, list_display, wind_object):
    print(list_display)
    for result in result_list:
        yield [name(wind_object, result_list) if isinstance(name, FunctionType) else getattr(result, name) for name in list_display]



def table_head():
    pass


@register.inclusion_tag("md.html")
def get_result(base_dir, result_list, list_display, wind_object):
    table_body_data = table_body(result_list, list_display, wind_object)

    return {"table_body_data": table_body_data}