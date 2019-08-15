from django_filters import rest_framework as filters
from repository.models_list.models import Hospital, Doctor


class HospitalFilter(filters.FilterSet):
    """
    自定义规则
    定义后在 fields 加入
    """

    class Meta:
        model = Hospital
        fields = "__all__"

class DoctorFilter(filters.FilterSet):
    """
    自定义规则
    定义后在 fields 加入
    """
    work_min = filters.NumberFilter(field_name="doc_workage", lookup_expr='lte')
    work_max = filters.NumberFilter(field_name="doc_workage", lookup_expr='gte')

    class Meta:
        model = Doctor
        fields = ["work_min", "work_max"]