#
from django.urls import reverse
from django.core.paginator import Paginator,Page,PageNotAnInteger,EmptyPage


def get_pager(request, articles, pages, reverse_name, **kwargs):
    if request.GET.get("page"):
        current_page = int(request.GET.get("page"))
    else:
        current_page = 1
    p = Paginator(articles, pages)
    ps = p.page(current_page)

    # print(current_page, pages, p.num_pages)
    if current_page - pages <= 0:
        begin = 1
        if p.num_pages <= pages:
            end = p.num_pages + 1
        elif pages * 2 <= p.num_pages:
            print("123")
            end = pages * 2 + 1
        else:
            end = p.num_pages + 1
    elif current_page + pages < p.num_pages:
        begin = p.num_pages - (pages * 2 + 1)
        end = p.num_pages
    elif pages * 2 <= p.num_pages:
        begin = current_page - pages
        end = current_page + pages + 1
    else:
        begin = current_page - pages
        end = pages + 1

    diy_range = range(begin, end)
    reverse_url = reverse(reverse_name, kwargs=kwargs)
    return {
        "page_range": diy_range,
        "reverse_url": reverse_url,
        "p": ps,
        "current_page": current_page,
    }