"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView

from api import views
from wind_admin import wind_core

from rest_framework.documentation import include_docs_urls
from rest_framework.authtoken import views as dfr_views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url(r'^$', views.index),
    url(r'^wind/', wind_core.site.urls),
    url(r'^admin/', admin.site.urls),
    url(r'^index/', views.index),
    url(r'^about/', views.about),
    url(r'^happy_birthday_to_caroline/', views.happy),
    url(r'^github/', views.github),
    url(r'^galleries.html/', views.galleries),
    # url(r'^category/(?P<article_blog>\d+)-(?P<article_category>\d+)', views.category),
    url(r'^(?P<article_blog>\d+)/(?P<filter>((category)|(tag)|(time)))/(?P<id>\w+-*\w*)', views.filter, name="filter"),
    url(r'^login/', views.login),
    url(r'^logout/', views.logout),
    url(r'^check_code/', views.check_code),
    url(r'^register/', views.register),
    url(r'^(?P<article_blog>\d+)/(?P<article_id>\d+)', views.article),
    url(r'^comment/', views.comment),
    url(r'^(?P<article_blog>\d+)/blog/', views.blog_3colums, name="blog"),
    url(r'^sync/', views.sync),
    # url(r'^(\w+)/', views.blog),



    url(r'api/', include('api.urls', namespace='api-repository')),
    url(r'docs/', include_docs_urls(title="ydyl")),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', dfr_views.obtain_auth_token), # drf 自带
    url(r'^jwt-auth/', obtain_jwt_token),
    # url(r'^sentry-debug/', trigger_error),





    url(r'^$', views.index),

]
