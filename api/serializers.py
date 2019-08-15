import json
from time import timezone
from decimal import Decimal
from datetime import datetime
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from repository.models_list.models import Hospital, Department, \
    Doctor, HospitalToDoctorToDepartment, Patient, \
    HosipitalToPatient, Source, Time, Pay, PayDetail, \
    PayInfo, Order


# serializers.Serializer # 用于 Model 有联合唯一时，需要配合 create 方法，自行写逻辑
class HospitalSerializer(serializers.ModelSerializer):
    # write_only: 不使用该字段序列化（不返回）
    hos_phone = serializers.CharField(validators=[UniqueValidator(queryset=Hospital.objects.all(), message="联系电话已存在")])

    # 获取当前用户，fields需要返回ID for 取消功能。
    # user = serializers.HiddenField(serializers=serializers.CurrentUserDefault)

    # serializers.SerializerMethodField # 自定义序列化函数
    class Meta:
        model = Hospital
        fields = "__all__"

    # def create(self, validated_data):
    #     """
    #     加密字段等
    #
    #     获取 request: self.context["request"]
    #     :param validated_data:
    #     :return:
    #     """
    #     # user = super(HospitalSerializer, self).create(validated_data)
    #     # user.set_password(validated_data['password'])
    #     # user.save()
    #     return Hospital.objects.create(**validated_data)
    #
    # def validate_hos_phone(self, phone):
    #     """
    #     校验等操作
    #     :param phone:
    #     :return:
    #     """
    #     # raise serializers.ValidationError
    #     return phone
    #
    # def validate(self, attrs):
    #     """
    #     对所有字段校验
    #     :param attrs:
    #     :return:
    #     """
    #     return attrs


class DepartmentSerializer(serializers.ModelSerializer):
    """
    self.initial_data： 前端传入的参数
    """
    dep_hosid = HospitalSerializer()
    class Meta:
        model = Department
        fields = "__all__"

    def create(self, validated_data):
        return Department.objects.create(**validated_data)


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = "__all__"


class HospitalToDoctorToDepartmentSerializer(serializers.ModelSerializer):
    relate_hosid = Hospital()
    relate_depid = DepartmentSerializer()
    relate_docid = DoctorSerializer()

    class Meta:
        model = HospitalToDoctorToDepartment
        fields = "__all__"


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"


class HosipitalToPatientSerializer(serializers.ModelSerializer):
    relate_hosid = HospitalSerializer()
    relate_patid = PatientSerializer()
    class Meta:
        model = HosipitalToPatient
        fields = "__all__"


class SourceSerializer(serializers.ModelSerializer):
    sour_hosid = HospitalSerializer()
    sour_depid = DepartmentSerializer()
    sour_docid = DoctorSerializer()

    times_list = serializers.SerializerMethodField()

    class Meta:
        model = Source
        fields = "__all__"

    def get_times_list(self, obj):
        times_json = {}
        times = Time.objects.filter(time_sourceid=obj.sour_id)
        if times:
            times_json = TimeSerializer(times, many=True, context={'request': self.context['request']}).data
        return times_json


class TimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Time
        fields = "__all__"


class PaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pay
        fields = "__all__"


class PayDetailSerializer(serializers.ModelSerializer):
    paydetail_pay = serializers.SerializerMethodField()

    def get_paydetail_pay(self, obj):
        pay = Decimal(obj.paydetail_total) - Decimal(obj.paydetail_discount)
        return str(pay)

    class Meta:
        model = PayDetail
        fields = "__all__"


class PayInfoSerializer(serializers.ModelSerializer):
    payinfo_pay = serializers.SerializerMethodField()

    def get_payinfo_pay(self, obj):
        pay = Decimal(obj.payinfo_total) - Decimal(obj.payinfo_insurance_discount) - \
              Decimal(obj.payinfo_insurance_person)
        return str(pay)

    class Meta:
        model = PayInfo
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        # 重复下单（同一个患者同一个天）
        orders_obj = Order.objects.filter(order_patient__pat_id=validated_data["order_patient"].pat_id,
                                        order_sourid__sour_date=validated_data["order_timeid"].time_sourceid.sour_date
                                          ).all()
        if len(orders_obj) > 0:
            raise serializers.ValidationError("请勿重复挂号")

        # 号源不足
        time_obj = Time.objects.filter(time_id=validated_data["order_timeid"].time_id).first()
        if time_obj.time_surplus - 1 >= 0:
            time_obj.time_surplus -= 1
            time_obj.save()
        else:
            raise serializers.ValidationError("号源不足")

        # 连表查询医院等信息
        validated_data["order_number"] = Order.objects.filter(order_timeid__time_sourceid__sour_id=validated_data["order_timeid"].time_sourceid.sour_id).count()
        validated_data["order_sourid"] = Source.objects.filter(time__time_id=validated_data["order_timeid"].time_id).first()
        validated_data["order_hospital"] = validated_data["order_timeid"].time_sourceid.sour_hosid
        validated_data["order_doctor"] = validated_data["order_timeid"].time_sourceid.sour_docid
        validated_data["order_total"] = validated_data["order_timeid"].time_sourceid.sour_total

        return Order.objects.create(**validated_data)


    def update(self, instance, validated_data):
        if validated_data["order_pay"] == 3:
            # 待退款
            time_obj = Time.objects.filter(time_id=validated_data["order_timeid"].time_id).first()
            time_obj.time_surplus += 1
            time_obj.save()

        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)

        m2m_fields = []
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)

        instance.save()

        for attr, value in m2m_fields:
            field = getattr(instance, attr)
            field.set(value)

        return instance


    class Meta:
        model = Order
        fields = "__all__"