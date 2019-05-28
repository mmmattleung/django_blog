from django.shortcuts import render
from blog import settings
from django.utils.deprecation import MiddlewareMixin


class M1(MiddlewareMixin):
    def process_exception(self, request, exception):

        return render(request, "404.html", {
            "base_dir": settings.BASE_HOST
        })