import copy
from django.urls import reverse
from django.core.paginator import Paginator,Page,PageNotAnInteger,EmptyPage


def get_pager(self, request, articles, pages):
    def _get_request_param(request):
        page_param_dict = copy.deepcopy(request.GET)
        page_param_dict._mutable = True
        if request.GET.get("page"):
            current_page = int(request.GET.get("page"))
        else:
            current_page = 1
            page_param_dict["page"] = 1
        return current_page, page_param_dict

    current_page, page_param_dict = _get_request_param(request)

    def _get_page_object(articles, pages):
        p = Paginator(articles, pages)
        ps = p.page(current_page)
        return p, ps

    p, ps = _get_page_object(articles, pages)

    def _get_url(self):
        return reverse(
        "{2}:{0}_{1}_changelist".format(self.app_label, self.model_name, self.site_object.name_space))

    base_page_url = _get_url(self)
    object_list = articles[ps.start_index() - 1:ps.end_index()]

    def _set_next_pre_url(ps):
        if ps.has_previous():
            page_param_dict["page"] = current_page - 1
            previous_url = "%s?%s" % (base_page_url, page_param_dict.urlencode())
            ps.previous_url = previous_url
        if ps.has_next():
            page_param_dict["page"] = current_page + 1
            next_url = "%s?%s" % (base_page_url, page_param_dict.urlencode())
            ps.next_url = next_url

    _set_next_pre_url(ps)

    def _count_pages(p, current_page):
        if current_page - pages <= 0:
            begin = 1
            if p.num_pages <= pages:
                end = p.num_pages + 1
            else:
                end = pages * 2 + 1
        elif current_page + pages > p.num_pages:
            begin= p.num_pages - (pages * 2 + 1)
            end = p.num_pages
        else:
            begin= current_page - pages
            end = current_page + pages + 1
        return range(begin, end)

    diy_range = _count_pages(p, current_page)
    print(diy_range)

    def _set_html_tags(ps, diy_range):
        range_str = ""
        for item in diy_range:
            tmp = "<a href='{0}' class='{1}' >{2}</a>"
            if item == current_page:
                item_class = "btn btn-white active"
            else:
                item_class = "btn btn-white"
            page_param_dict["page"] = item
            tmp = tmp.format(
                "%s?%s" % (base_page_url, page_param_dict.urlencode()),
                item_class,
                item
            )
            range_str += tmp
        ps.diy_range = range_str

    _set_html_tags(ps, diy_range)

    return ps, object_list