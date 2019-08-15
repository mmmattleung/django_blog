"""test_rest_api URL Configuration

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
from api.views_list.views import HospitalList, DepartmentList, \
    DoctorList, HospitalToDoctorToDepartmentList, PatientList, \
    HosipitalToPatientList, add_data, SourceList, TimeList, \
    PayList, PayDetailList, PayInfoList, OrderList

from django.contrib import admin
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'hospitals', HospitalList)
router.register(r'departments', DepartmentList)
router.register(r'doctors', DoctorList)
router.register(r'hostodeptodoc', HospitalToDoctorToDepartmentList)
router.register(r'patients', PatientList)
router.register(r'hostopat', HosipitalToPatientList)
router.register(r'sources', SourceList)
router.register(r'times', TimeList)
router.register(r'pays', PayList)
router.register(r'paydetials', PayDetailList)
router.register(r'payinfos', PayInfoList)
router.register(r'orders', OrderList)

urlpatterns = [
    # url(r'^hospitals/', hos_list, name='hospital-list'),
    # url(r'^departments/', DepartmentList.as_view(), name='department-list'),
    url(r'^', include(router.urls)),
    url(r'^add_data/', add_data),
]
