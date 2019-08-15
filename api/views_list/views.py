import random
import pandas as pd
from decimal import Decimal

from django.shortcuts import render, HttpResponse
from django_filters import rest_framework as filters

from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import mixins, generics
from rest_framework import throttling
from rest_framework.response import Response
from rest_framework import filters as rs_filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from api.permissions import IsOwnerOrReadOnly
from api.filters import HospitalFilter, DoctorFilter
from api.serializers import HospitalSerializer, \
    DepartmentSerializer, DoctorSerializer, \
    HospitalToDoctorToDepartmentSerializer, PatientSerializer, \
    HosipitalToPatientSerializer, SourceSerializer, \
    TimeSerializer, PaySerializer, PayDetailSerializer, \
    PayInfoSerializer, OrderSerializer

from repository.models_list.models import Hospital, Department, \
    Doctor, HospitalToDoctorToDepartment, Patient, HosipitalToPatient, \
    Source, Time, Pay, PayDetail, PayInfo, Order
from utils.date_utils import get_date_list

from utils.fak import Faker_t

# Create your views here.
class MyPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    # page_query_param = 'p'
    max_page_size = 10000


class HospitalList(CacheResponseMixin, viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    """
    list:
        获取医院列表
    """
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
    pagination_class = MyPagination
    filter_backends = (filters.DjangoFilterBackend, )
    throttle_classes = (throttling.AnonRateThrottle, throttling.UserRateThrottle)
    permission_classes = (IsAuthenticated, ) # IsOwnerOrReadOnly自定义权限
    # 动态设置权限
    # def get_permissions(self):
    #     if self.action == "retrieve":
    #         return [IsAuthenticated()]
    #     else:
    #         # 不设置权限
    #         return []
    #     pass

    # filter_fields = ("hos_name", "hos_phone", )
    filter_class = HospitalFilter
    # lookup_field = "hos_id" # API 网页中搜索的列名

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 自定义操作
        # obj = self.perform_create(serializer)
        # re_dict = serializer.data
        # payload = jwt_payload_handler(user)
        # re_dict["token"] = jwt_encode_handler(payload)
        # re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        # 可以在此加入某些随机字段的值
        return serializer.save()

    # ############# old #############
    # def get(self, request, format=None):
    #     hos = Hospital.objects.all()
    #     hos_serializer = HospitalSerializer(hos, many=True)
    #     return Response(hos_serializer.data)
    #
    # def post(self, request, format=None):
    #     hos_serializer = HospitalSerializer(data=request.data)
    #     if hos_serializer.is_valid():
    #         hos_serializer.save()
    #         return Response(hos_serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(hos_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def get_queryset(self):
    #     return Hospital.objects.filter(user=self.request.user) # 权限判断

    def get_object(self):
        """
        返回当前用户
        :return: 
        """
        # return self.request.user
        pass

    # def get_serializer_class(self):
    #     """
    #     根据 self.action 选择序列化类
    #     :return:
    #     """
    #     pass


class DepartmentList(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    pagination_class = MyPagination
    throttle_classes = (throttling.AnonRateThrottle, throttling.UserRateThrottle)
    # authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)  # IsOwnerOrReadOnly自定义权限
    filter_backends = (rs_filters.SearchFilter, rs_filters.OrderingFilter)
    search_fields = ('dep_name', )
    ordering_fields = ('dep_id', )


class DoctorList(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    pagination_class = MyPagination
    filter_backends = (filters.DjangoFilterBackend,)
    throttle_classes = (throttling.AnonRateThrottle, throttling.UserRateThrottle)
    # filter_fields = ("hos_name", "hos_phone", )
    filter_class = DoctorFilter
    permission_classes = (IsAuthenticated,)  # IsOwnerOrReadOnly自定义权限


class HospitalToDoctorToDepartmentList(viewsets.ModelViewSet):
    queryset = HospitalToDoctorToDepartment.objects.all()
    serializer_class = HospitalToDoctorToDepartmentSerializer
    pagination_class = MyPagination
    throttle_classes = (throttling.AnonRateThrottle, throttling.UserRateThrottle)
    # filter_backends = (filters.DjangoFilterBackend, )
    # filter_fields = ("hos_name", "hos_phone", )
    # filter_class = DoctorFilter
    permission_classes = (IsAuthenticated,)  # IsOwnerOrReadOnly自定义权限


class PatientList(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    pagination_class = MyPagination
    throttle_classes = (throttling.AnonRateThrottle, throttling.UserRateThrottle)
    permission_classes = (IsAuthenticated,)  # IsOwnerOrReadOnly自定义权限


class HosipitalToPatientList(viewsets.ModelViewSet):
    queryset = HosipitalToPatient.objects.all()
    serializer_class = HosipitalToPatientSerializer
    pagination_class = MyPagination
    throttle_classes = (throttling.AnonRateThrottle, throttling.UserRateThrottle)
    permission_classes = (IsAuthenticated,)  # IsOwnerOrReadOnly自定义权限


class SourceList(viewsets.ModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    pagination_class = MyPagination
    throttle_classes = (throttling.AnonRateThrottle, throttling.UserRateThrottle)
    permission_classes = (IsAuthenticated,)  # IsOwnerOrReadOnly自定义权限


class TimeList(viewsets.ModelViewSet):
    queryset = Time.objects.all()
    serializer_class = TimeSerializer
    pagination_class = MyPagination
    throttle_classes = (throttling.AnonRateThrottle, throttling.UserRateThrottle)
    permission_classes = (IsAuthenticated,)  # IsOwnerOrReadOnly自定义权限


class PayList(viewsets.ModelViewSet):
    queryset = Pay.objects.all()
    serializer_class = PaySerializer
    pagination_class = MyPagination
    throttle_classes = (throttling.AnonRateThrottle, throttling.UserRateThrottle)
    permission_classes = (IsAuthenticated,)  # IsOwnerOrReadOnly自定义权限

    def create(self, request, *args, **kwargs):
        data = request.data
        data._mutable = True
        data["pay_pay"] = float(data["pay_total"]) - float(data["pay_discount"])
        print(data["pay_pay"])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PayDetailList(viewsets.ModelViewSet):
    queryset = PayDetail.objects.all()
    serializer_class = PayDetailSerializer
    pagination_class = MyPagination
    throttle_classes = (throttling.AnonRateThrottle, throttling.UserRateThrottle)
    permission_classes = (IsAuthenticated,)  # IsOwnerOrReadOnly自定义权限

class PayInfoList(viewsets.ModelViewSet):
    queryset = PayInfo.objects.all()
    serializer_class = PayInfoSerializer
    pagination_class = MyPagination
    throttle_classes = (throttling.AnonRateThrottle, throttling.UserRateThrottle)
    permission_classes = (IsAuthenticated,)  # IsOwnerOrReadOnly自定义权限


class OrderList(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = MyPagination
    throttle_classes = (throttling.AnonRateThrottle, throttling.UserRateThrottle)
    permission_classes = (IsAuthenticated,)  # IsOwnerOrReadOnly自定义权限

    def perform_update(self, serializer):
        """
        当用户点击支付按钮，支付状态修改为"支付中"时，生成结算单、结算明细及支付信息
        :param serializer: 
        :return: 
        """
        serializer.save()
        if serializer.instance.order_pay == 1: # 支付中
            total = serializer.instance.order_timeid.time_sourceid.sour_total
            pay_data = {
                "pay_patient_id": serializer.instance.order_patient.pat_id,
                "pay_hospital_id": serializer.instance.order_timeid.time_sourceid.sour_hosid.hos_id,
                "pay_method": 0,
                "pay_currency": 0,
                "pay_total": total,
                "pay_discount": 0,
                "pay_pay": total,
                "pay_stauts": 1,
                "pay_insurance": 0,
            }
            pay_obj = Pay.objects.create(**pay_data)

            pay_detail_data = {
                "paydetail_payid_id": pay_obj.pay_id,
                "paydetail_type": 0,
                "paydetail_total": pay_obj.pay_total,
                "paydetail_discount": 0,
                "paydetail_pay": pay_obj.pay_total,
            }
            PayDetail.objects.create(**pay_detail_data)

            pay_info_data = {
                "payinfo_payid": pay_obj,
                "payinfo_total": pay_obj.pay_total,
                "payinfo_insurance_discount": 0,
                "payinfo_insurance_person": 0,
                "payinfo_pay": pay_obj.pay_total,
                "payinfo_type": 1,
                "payinfo_currency": 0,
                "payinfo_status": 1,
                "payinfo_method": 1,
            }
            PayInfo.objects.create(**pay_info_data)


def add_data(request):
    if request.method == "GET":
        # 写入随机医生信息
        # res = Doctor.objects.all()
        # for doc in res:
        #     fak = Faker_t()
        #     doc.doc_age = fak.get_age()
        #     doc.doc_name = fak.get_name()
        #     doc.doc_gender = 1 if fak.get_gender() == "M" else 2
        #     doc.doc_workage = random.randint(0, 30)
        #     doc.save()

        # 写入医患信息
        # res = Patient.objects.all()
        # hos = Hospital.objects.all()[0]
        # for pat in res:
        #     new_data = HosipitalToPatient()
        #     new_data.relate_hosid = hos
        #     new_data.relate_patid = pat
        #     new_data.relate_mcard = random.randint(000000, 999999)
        #     new_data.relate_hcard = random.randint(000000, 999999)
        #     new_data.relate_balance = random.randint(0, 999999)
        #     new_data.save()
        #     print("save", pat.pat_id)

        # 写入医生排班信息
        # res = HospitalToDoctorToDepartment.objects.all()
        # print(res.count())
        # hos = Hospital.objects.all()[0]
        # for doc_raltion in res:
        #     r = random.randint(0, 1)
        #     if r:
        #         """
        #         sour_hosid
        #         sour_depid
        #         sour_docid
        #         sour_date
        #         sour_total
        #         sour_surplus
        #         sour_fee
        #         sour_otherid
        #         sour_cdate
        #         sour_ctype
        #         sour_cid
        #         sour_remark
        #         """
        #         date_list = get_date_list("2019-01-01", "2019-01-31")
        #         for item in date_list:
        #             r = random.randint(0, 10)
        #             print("r==", r)
        #             if r == 0:
        #                 new_source = Source()
        #                 new_source.sour_hosid = hos
        #                 new_source.sour_depid = doc_raltion.relate_depid
        #                 new_source.sour_docid = doc_raltion.relate_docid
        #                 new_source.sour_total = random.choice([10, 20, 30])
        #                 new_source.sour_surplus = new_source.sour_total
        #                 new_source.sour_date = item
        #                 new_source.save()
        #                 print("save")

        res = Source.objects.all()
        count = Source.objects.all().count()
        print(count)
        pass_times = [
            '12:00:00',
            '12:30:00',
            '13:00:00',
            '13:30:00',
            '14:00:00',
            '17:30:00',
            '18:00:00',
            '18:30:00',
            '19:00:00',
        ]
        # i = 0
        for sour in res:
            print("sour.sour_date", sour.sour_date, sour.sour_docid)
            date_list = pd.date_range(start=str(sour.sour_date).split(" ")[0] + " 09:00:00", periods=30, freq='30min')
            """
            time_sourceid = models.ForeignKey(to=Source, verbose_name="号源编号")
            time_start = models.DateTimeField(verbose_name="开始时间")
            time_end = models.DateTimeField(verbose_name="结束时间")
            time_total = models.IntegerField(verbose_name="号源总数")
            time_surplus = models.IntegerField(verbose_name="剩余数量")
            """
            tot = sour.sour_total
            for d in date_list:

                if str(d).split(" ")[1] not in pass_times and tot > 0:
                    new_time = Time()
                    new_time.time_sourceid = sour
                    new_time.time_total = 3 if tot - 3 >= 0 else tot
                    new_time.time_surplus = 3 if tot - 3 >= 0 else tot
                    new_time.time_start = d
                    new_time.time_end = pd.date_range(start=d, periods=2, freq='30min')[1]
                    tot -= 3
                    new_time.save()
            # i += 1
            # if i == 2:
            #     break
        return HttpResponse("123")

