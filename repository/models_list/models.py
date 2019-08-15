from django.db import models
from django.utils import timezone
import datetime
import time


# Create your models here.



class Hospital(models.Model):
    hos_id = models.BigAutoField(primary_key=True, verbose_name="医院编号")
    hos_unique = models.CharField(max_length=128, verbose_name="唯一编号", unique=True, blank=True, null=True)
    hos_ctime = models.DateTimeField(default = timezone.now, verbose_name="创建时间")
    hos_name = models.CharField(max_length=64, verbose_name="医院名称", help_text="医院名称")
    hos_address = models.CharField(max_length=256, verbose_name="医院地址")
    hos_phone = models.CharField(max_length=64, verbose_name="电话")
    hos_email = models.EmailField(max_length=256, verbose_name="邮箱")
    hos_code = models.CharField(max_length=32, verbose_name="邮政编码")
    hos_contact = models.CharField(max_length=32, verbose_name="联系人")
    hos_primary = models.TextField(verbose_name="简述")
    hos_level = models.CharField(max_length=32, verbose_name="级别")
    hos_longitude = models.CharField(max_length=16, verbose_name="经度")
    hos_latitude = models.CharField(max_length=16, verbose_name="纬度")
    hcarete_choice = ((0, "否"), (1, "是"))
    hos_create_card = models.SmallIntegerField(choices=hcarete_choice, default=0, verbose_name="能否建卡")
    hos_picture = models.CharField(max_length=128, verbose_name="图片")
    hos_logo = models.CharField(max_length=128, verbose_name="标志图")

    def __str__(self):
        return "{} - {}".format(self.hos_id, self.hos_name)


class Department(models.Model):
    """
    did	bigint	8
    dtime	datetime	0
    dhid	bigint	8
    dlevel	varchar	256
    dname	varchar	64
    dopenstatus	int	1
    ddesciption	text	0
    dexpert	text	0
    dpicture	varchar	128
    dphone	varchar	64
    daddress	varchar	128
    dotherid	varchar	128
    """

    open_choices = ((0, "闭诊"), (1, "开诊"))
    dep_id = models.BigAutoField(primary_key=True, verbose_name="科室编号")
    dep_unique = models.CharField(max_length=128, verbose_name="唯一编号", unique=True, blank=True, null=True)
    dep_ctime = models.DateTimeField(default = timezone.now, verbose_name="创建时间")
    dep_hosid = models.ForeignKey(to=Hospital, null=True, blank=True, verbose_name="医院外键")
    dep_level = models.CharField(max_length=256, verbose_name="等级", null=True, blank=True)
    dep_name = models.CharField(max_length=64, null=True, blank=True, verbose_name="科室名称")
    dep_openstatus = models.SmallIntegerField(choices=open_choices, default=1, verbose_name="开诊状态")
    dep_desciption = models.TextField(verbose_name="科室简介", null=True, blank=True)
    dep_expert = models.TextField(verbose_name="科室擅长", null=True, blank=True)
    dep_picture = models.CharField(max_length=128, verbose_name="科室图片", null=True, blank=True)
    dep_phone = models.CharField(max_length=64, verbose_name="电话", null=True, blank=True)
    dep_address = models.CharField(max_length=128, verbose_name="科室位置", null=True, blank=True)
    dep_otherid = models.CharField(max_length=128, verbose_name="第三方外键", null=True, blank=True)

    def __str__(self):
        return "{} - {}".format(self.dep_id, self.dep_name)


class Doctor(models.Model):
    sex_choices = ((0, "女"), (1, "男"), (2, "保密"))
    doc_id = models.BigAutoField(primary_key=True)
    doc_unique = models.CharField(max_length=128, verbose_name="唯一编号", unique=True, blank=True, null=True)
    doc_ctime = models.DateTimeField(default = timezone.now, verbose_name="创建时间")
    doc_name = models.CharField(max_length=32, verbose_name="医生姓名")
    doc_gender = models.IntegerField(choices=sex_choices, default=2, verbose_name="性别")
    doc_age = models.IntegerField(blank=True, null=True, verbose_name="年龄")
    doc_level = models.CharField(max_length=32, blank=True, null=True, verbose_name="职称")
    doc_phone = models.CharField(max_length=32, blank=True, null=True, verbose_name="电话")
    doc_email = models.EmailField(max_length=128, blank=True, null=True, verbose_name='邮箱')
    doc_avatar = models.TextField(blank=True, null=True, verbose_name='头像')
    doc_specialty = models.TextField(blank=True, null=True, verbose_name='特长')
    doc_introduction = models.TextField(blank=True, null=True, verbose_name='简介')
    doc_workid = models.CharField(max_length=64, blank=True, null=True, verbose_name='工号')
    doc_workage = models.IntegerField(blank=True, null=True, verbose_name='工龄')
    doc_otherid = models.CharField(max_length=128, blank=True, null=True, verbose_name='第三方ID')

    def __str__(self):
        return "{}-{}".format(self.doc_id, self.doc_name)

class HospitalToDoctorToDepartment(models.Model):
    open_choices = ((0, "闭诊"), (1, "开诊"))

    relate_id = models.BigAutoField(primary_key=True)
    relate_ctime = models.DateTimeField(default = timezone.now, verbose_name="创建时间")
    relate_hosid = models.ForeignKey(to=Hospital)
    relate_depid = models.ForeignKey(to=Department)
    relate_docid = models.ForeignKey(to=Doctor)
    relate_like = models.IntegerField(verbose_name="点赞数量")
    relate_open_status = models.IntegerField(choices=open_choices, verbose_name="开诊状态")


class Patient(models.Model):
    gender = (("0", "女"), ("1", "男"), ("2", "保密"))
    identity = (("0", "成人"), ("1", "儿童"))
    card = (("0", "身份证"), ("1", "护照"), ("2", "港澳通行证"), ("3", "台湾通行证"), ("4", "军人证"))

    pat_id = models.BigAutoField(primary_key=True)
    pat_ctime = models.DateTimeField(default = timezone.now, verbose_name="创建时间")
    pat_name = models.CharField(max_length=32, verbose_name="患者姓名")
    pat_phone = models.CharField(max_length=32, verbose_name="手机号码")
    pat_gender = models.IntegerField(choices=gender, verbose_name="性别", default=2)
    pat_high = models.CharField(max_length=8, blank=True, null=True, verbose_name="身高")
    pat_blood = models.CharField(max_length=8, blank=True, null=True, verbose_name="血型")
    pat_weight = models.CharField(max_length=8, blank=True, null=True, verbose_name="体重")
    pat_identity = models.IntegerField(choices=identity, blank=True, null=True, verbose_name="身份")
    pat_cardtype = models.IntegerField(choices=card, blank=True, null=True, )
    pat_card = models.CharField(max_length=64, blank=True, null=True, )
    pat_age = models.CharField(max_length=8, blank=True, null=True, )
    pat_pic = models.CharField(max_length=128, blank=True, null=True, )
    pat_nation = models.CharField(max_length=8, blank=True, null=True, )
    pat_address = models.TextField(blank=True, null=True, )
    pat_guardian = models.CharField(max_length=32, blank=True, null=True, )
    pat_birthday = models.CharField(max_length=32, blank=True, null=True, )
    pat_allergy = models.CharField(max_length=16, blank=True, null=True, )
    pat_otherid = models.CharField(max_length=128, blank=True, null=True, )
    pat_scard = models.CharField(max_length=64, blank=True, null=True, )

    def __str__(self):
        return "{}-{}".format(self.pat_id, self.pat_name)


class HosipitalToPatient(models.Model):
    relate_id = models.BigAutoField(primary_key=True)
    relate_ctime = models.DateTimeField(default=datetime.datetime.now, verbose_name="创建时间")
    relate_hosid = models.ForeignKey(Hospital)
    relate_patid = models.ForeignKey(Patient)
    relate_mcard = models.CharField(max_length=16)
    relate_hcard = models.CharField(max_length=16)
    relate_balance = models.DecimalField(max_digits=18, decimal_places=2)


class Source(models.Model):
    sour_id = models.BigAutoField(primary_key=True)
    sour_ctime = models.DateTimeField(default=datetime.datetime.now, verbose_name="创建时间")
    sour_hosid = models.ForeignKey(to=Hospital)
    sour_depid = models.ForeignKey(to=Department)
    sour_docid = models.ForeignKey(to=Doctor)
    sour_date = models.DateTimeField(verbose_name="日期")
    sour_total = models.IntegerField(default=0, verbose_name="总号源")
    sour_surplus = models.IntegerField(default=0, verbose_name="剩余号源")
    sour_fee = models.DecimalField(max_digits=18, decimal_places=2, default=0.00, verbose_name="挂号费用")
    sour_otherid = models.CharField(max_length=128, null=True, blank=True, verbose_name="第三方编号")
    sour_cdate = models.DateTimeField(default=datetime.datetime.now, verbose_name="生成日期")
    sour_ctype = models.IntegerField(default=0, choices=((0, "导入"), (1, "策略")), verbose_name="生成方式")
    sour_cid = models.CharField(max_length=128, default="", verbose_name="生成策略编号")
    sour_remark = models.IntegerField(blank=True, null=True, choices=((0, "早"), (1, "中"), (2, "晚")), verbose_name="时段标识")


class Time(models.Model):
    time_id = models.BigAutoField(primary_key=True)
    time_ctime = models.DateTimeField(default=datetime.datetime.now, verbose_name="创建时间")
    time_sourceid = models.ForeignKey(to=Source, verbose_name="号源编号")
    time_start = models.DateTimeField(verbose_name="开始时间")
    time_end = models.DateTimeField(verbose_name="结束时间")
    time_total = models.IntegerField(verbose_name="号源总数")
    time_surplus = models.IntegerField(verbose_name="剩余数量")

    def __str__(self):
        return "time:{} source:{}".format(self.time_id, self.time_sourceid.sour_id)


class Pay(models.Model):
    """
    结算表
    """
    pay_id = models.BigAutoField(primary_key=True)
    pay_time = models.DateTimeField(default=datetime.datetime.now, verbose_name="创建时间")
    pay_patient = models.ForeignKey(to=Patient)
    pay_hospital = models.ForeignKey(to=Hospital)
    pay_method = models.IntegerField(choices=(
        (0, "现金"),
        (1, "微信"),
        (2, "支付宝"),
        (3, "银联"),
    ), verbose_name="结算方式")
    pay_currency = models.IntegerField(choices=((0, "RMB"), ), default=0, verbose_name="结算货币")
    pay_total = models.DecimalField(max_digits=18, decimal_places=2, default=0.00, verbose_name="结算金额")
    pay_discount = models.DecimalField(max_digits=18, decimal_places=2, default=0.00, verbose_name="优惠金额")
    pay_pay = models.DecimalField(max_digits=18, decimal_places=2, default=0.00, verbose_name="付款金额", null=True, blank=True)
    pay_stauts = models.IntegerField(choices=(
        (0, "待结算"),
        (1, "结算中"),
        (2, "已结算"),
    ), verbose_name="结算状态")
    pay_insurance = models.IntegerField(choices=((0, "否"), (1, "是")), verbose_name="是否医保")
    pay_remark = models.TextField(verbose_name="摘要说明")

    def __str__(self):
        return "{}-{}-{}".format(self.pay_id, self.pay_patient.pat_name, self.pay_pay)


class PayDetail(models.Model):
    """
    结算明细
    """
    paydetail_id = models.BigAutoField(primary_key=True)
    paydetail_time = models.DateTimeField(default=datetime.datetime.now, verbose_name="创建时间")
    paydetail_payid = models.ForeignKey(to=Pay)
    paydetail_type = models.IntegerField(
        choices=(
            (0, "挂号"),
            (1, "处方"),
            (2, "检查"),
            (3, "检验"),
            (4, "治疗"),
            (5, "住院押金"),
        ),
        verbose_name="结算类型")
    paydetail_total = models.DecimalField(max_digits=18, decimal_places=2, default=0.00, verbose_name="结算金额")
    paydetail_discount = models.DecimalField(max_digits=18, decimal_places=2, default=0.00, verbose_name="优惠金额")
    paydetail_pay = models.DecimalField(max_digits=18, decimal_places=2, default=0.00, verbose_name="支付金额")
    paydetail_remark = models.TextField(blank=True, null=True, verbose_name="摘要说明")


class PayInfo(models.Model):
    """
    支付信息
    """
    payinfo_id = models.BigAutoField(primary_key=True)
    payinfo_time = models.DateTimeField(default=datetime.datetime.now, verbose_name="创建时间")
    payinfo_payid = models.ForeignKey(to=Pay)
    payinfo_total = models.DecimalField(max_digits=18, decimal_places=2, default=0.00, verbose_name="总金额")
    payinfo_insurance_discount = models.DecimalField(max_digits=18, decimal_places=2, default=0.00, verbose_name="医保统筹")
    payinfo_insurance_person = models.DecimalField(max_digits=18, decimal_places=2, default=0.00, verbose_name="医保个账")
    payinfo_pay = models.DecimalField(max_digits=18, decimal_places=2, default=0.00, verbose_name="结算金额")
    payinfo_type = models.IntegerField(choices=(
        (0, "现金"),
        (1, "微信"),
        (2, "支付宝"),
        (3, "银联"),
    ), verbose_name="结算方式")
    payinfo_currency = models.IntegerField(choices=((0, "RMB"), ), default=0, verbose_name="结算货币")
    payinfo_status = models.IntegerField(choices=(
        (0, "待结算"),
        (1, "结算中"),
        (2, "已结算"),
    ), verbose_name="结算状态")
    payinfo_method = models.IntegerField(choices=(
        (0, "柜台"),
        (1, "公众号"),
        (2, "自助机"),
    ), verbose_name="支付渠道")
    payinfo_flow_bill = models.CharField(max_length=128, blank=True, null=True,verbose_name="交易单号（流水单号）")
    payinfo_pay_time = models.DateTimeField(blank=True, null=True, verbose_name="支付时间")
    payinfo_pay_data = models.TextField(blank=True, null=True, verbose_name="支付数据")
    payinfo_refund_id = models.CharField(blank=True, null=True, max_length=128, verbose_name="退款单号")
    payinfo_refund_time = models.DateTimeField(blank=True, null=True, verbose_name="退款时间")
    payinfo_refund_data = models.TextField(blank=True, null=True, verbose_name="退款数据")
    payinfo_fail_reason = models.TextField(blank=True, null=True, verbose_name="退款原因")
    payinfo_try_times = models.IntegerField(blank=True, null=True, verbose_name="尝试次数")
    payinfo_shop_id = models.CharField(blank=True, null=True, max_length=128, verbose_name="商户号")
    payinfo_remark = models.TextField(blank=True, null=True, verbose_name="摘要说明")
    payinfo_insurance_data = models.TextField(blank=True, null=True, verbose_name="医保数据体")


class Order(models.Model):
    order_id = models.BigAutoField(primary_key=True)
    order_time = models.DateTimeField(default=datetime.datetime.now, verbose_name="创建时间")
    order_timeid = models.ForeignKey(to=Time)
    order_sourid = models.ForeignKey(to=Source, blank=True, null=True)
    order_pay_id = models.ForeignKey(to=Pay, blank=True, null=True)
    order_hospital = models.ForeignKey(to=Hospital, blank=True, null=True)
    order_doctor = models.ForeignKey(to=Doctor, blank=True, null=True)
    order_patient = models.ForeignKey(to=Patient, blank=True, null=True)
    order_paydetail = models.ForeignKey(to=PayDetail, blank=True, null=True)
    order_number = models.IntegerField(default=0, verbose_name="号源序号")
    order_selltime = models.DateTimeField(default=datetime.datetime.now, verbose_name="创建时间")
    order_cancel = models.TextField(blank=True, null=True, verbose_name="作废原因")
    order_overtime = models.DateTimeField(default=datetime.datetime.now()+datetime.timedelta(minutes=15), verbose_name="超时时间")
    order_total = models.DecimalField(max_digits=18, decimal_places=2, default=0.00)
    order_pay = models.IntegerField(choices=(
        (0, "待支付"),
        (1, "支付中"),
        (2, "已支付"),
        (3, "待退款"),
        (4, "退款中"),
        (5, "已退款"),
    ), verbose_name="支付状态")
    order_operation = models.IntegerField(choices=(
        (0, "待受理"),
        (1, "受理中"),
        (2, "已受理"),
    ), verbose_name="业务状态")
    order_sync = models.IntegerField(choices=((0, "未同步"), (1, "已同步")), verbose_name="同步状态")
    order_check = models.IntegerField(choices=((0, "未签到"), (1, "已签到")), verbose_name="是否签到")
    order_invoice = models.TextField(blank=True, null=True, verbose_name="发票号")
    order_hisdata = models.TextField(blank=True, null=True, verbose_name="HIS数据体")


class Prescription(models.Model):
    prescription_id = models.BigAutoField(primary_key=True)
    prescription_time = models.DateTimeField(default=datetime.datetime.now, verbose_name="创建时间")
    prescription_pay_id = models.ForeignKey(to=Pay)
    prescription_pay_detail_id = models.ForeignKey(to=PayDetail)
    prescription_patient = models.ForeignKey(to=Patient)
    prescription_hospital = models.ForeignKey(to=Hospital)
    prescription_dep_check = models.ForeignKey(to=Department, related_name="dep_check")
    prescription_dep_do = models.ForeignKey(to=Department, related_name="dep_do")
    prescription_doc = models.ForeignKey(to=Doctor)
    prescription_title = models.CharField(max_length=64, verbose_name="单据名称")
    prescription_total = models.DecimalField(max_digits=18, decimal_places=2, default=0.00, verbose_name="结算金额")
    prescription_pay_time = models.DateTimeField(default=datetime.datetime.now, verbose_name="创建时间")
    prescription_status = models.IntegerField(choices=(
        (0, "待结算"),
        (1, "结算中"),
        (2, "已结算"),
    ), verbose_name="业务状态")
    prescription_drug_status = models.IntegerField(choices=(
        (0, "否"),
        (1, "是"),
    ), verbose_name="取药状态", default=0)
    prescription_pay_status = models.IntegerField(choices=(
        (0, "待支付"),
        (1, "支付中"),
        (2, "已支付"),
    ), verbose_name="支付状态")
    prescription_sync = models.IntegerField(choices=(
        (0, "未同步"),
        (1, "已同步"),
    ), default=0, verbose_name="同步状态")
    prescription_invoice_number = models.CharField(max_length=128, verbose_name="发票号")
    prescription_sync_number = models.CharField(max_length=128, verbose_name="同步号")
    prescription_his_data = models.TextField(verbose_name="his数据体")
    prescription_push_status = models.IntegerField(choices=(
        (0, "未推送"),
        (1, "已推送"),
    ), default=0, verbose_name="推送状态")
    prescription_insurance = models.IntegerField(choices=(
        (0, "否"),
        (1, "是")
    ), verbose_name="是否医保", default=0)
    prescription_insurance_discount = models.DecimalField(max_digits=18, decimal_places=2, default=0.00, verbose_name="社保统筹")
    prescription_insurance_person = models.DecimalField(max_digits=18, decimal_places=2, default=0.00, verbose_name="社保个账")
    prescription_pay = models.DecimalField(max_digits=18, decimal_places=2, default=0.00, verbose_name="个人支付")
    prescription_his_insurance_data = models.TextField(verbose_name="his医保结算数据体")
    prescription_drug_remark = models.CharField(max_length=128, verbose_name="取药指引")


class PrescriptionDetail(models.Model):
    """
    处方明细
    """
    prescriptiondetail_id = models.BigAutoField(primary_key=True)
    prescriptiondetail_time = models.DateTimeField(default=datetime.datetime.now, verbose_name="创建时间")
    prescriptiondetail_p_id = models.ForeignKey(to=Prescription)
    prescriptiondetail_hos = models.ForeignKey(to=Hospital)
    prescriptiondetail_title = models.CharField(max_length=128, verbose_name="商品名称")
    prescriptiondetail_type_name = models.CharField(max_length=128, verbose_name="商品名称")
    prescriptiondetail_explain = models.TextField(verbose_name="规格说明")
    prescriptiondetail_unit_price = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="单价")
    prescriptiondetail_unit = models.CharField(max_length=64, verbose_name="单价")
    prescriptiondetail_numbers = models.IntegerField(verbose_name="数量")
    prescriptiondetail_total = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="合计金额")
    prescriptiondetail_sync_id = models.CharField(max_length=128, verbose_name="同步单据号")