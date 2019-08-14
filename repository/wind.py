from django import forms
from django.utils.safestring import mark_safe
from repository.models import ArticleDetail
from repository.forms import UserInfoForm, UserFansForm
from wind_admin import wind_core
from repository import models
from django.urls import reverse
from utils.filter_code import FilterList, FilterOption


class UserInfoWind(wind_core.BaseWind):
    def func(self, obj=None, is_header=False):
        if is_header:
            return "操作"
        else:
            name = "{0}:{1}_{2}_change".format(self.site_object.name_space, self.model_class._meta.app_label, self.model_class._meta.model_name)
            url = reverse(name, args=(obj.pk,))
            return mark_safe("<a href='{0}'>编辑</a>".format(url))

    def checkbox(self, obj=None, is_header=False):
        if is_header:
            return "选项"
        else:
            tag = "<input type='checkbox' name='pk' value='{0}' />".format(obj.pk)
            return mark_safe(tag)

    def userinfo_avatar_data(self, obj=None, is_header=False):
        if is_header:
            return "头像预览"
        else:
            url = "http://127.0.0.1:8000/{0}"
            img_url = url.format(obj.userinfo_avatar)
            tag = "<img src='{0}' width='100px' />".format(img_url)
            return mark_safe(tag)

    # get_add_or_edit_model_form = UserInfoForm
    list_display = [
        checkbox,
        "userinfo_id",
        "userinfo_name",
        "userinfo_password",
        "userinfo_nickname",
        "userinfo_email",
        userinfo_avatar_data,
        "userinfo_avatar",
        "userinfo_avatar_full",
        "userinfo_create_time",
        # "userinfo_fans",
        "userinfo_introdution",
        "userinfo_speciality",
        "userinfo_skills",
        "userinfo_education_and_experience",
        "userinfo_portfolo",
        "userinfo_fans",
        func,
    ]

    def initial(self, request):
        pk_list = request.POST.getlist('pk')
        # print(pk_list)
        models.UserInfo.objects.filter(pk__in=pk_list).update(userinfo_nickname='initial_test')
        return True
    initial.text = "初始化"

    def multi_delete(self, request):
        pass
    multi_delete.text = "批量删除"

    action_list = [initial, multi_delete]

    filter_list = [
        FilterOption('userinfo_name', False, text_func_name="text_username", val_func_name="value_username"),
        # FilterOption(email, False, text_func_name="text_email", val_func_name="value_email"),
        # FilterOption('userinfo_fans', True),
        # FilterOption('mmm', False),
    ]

wind_core.site.register(models.UserInfo, UserInfoWind)


class UserFansWind(wind_core.BaseWind):
    # get_add_or_edit_model_form = UserFansForm

    list_display = [
        "userfan_user",
        "userfan_follower"
    ]

wind_core.site.register(models.UserFans, UserFansWind)


class ArticleWind(wind_core.BaseWind):
    def func(self, obj=None, is_header=False):
        if is_header:
            return "操作"
        else:
            name = "{0}:{1}_{2}_change".format(self.site_object.name_space, self.model_class._meta.app_label, self.model_class._meta.model_name)
            url = reverse(name, args=(obj.pk,))
            return mark_safe("<a href='{0}'>编辑</a>".format(url))

    def checkbox(self, obj=None, is_header=False):
        if is_header:
            return "选项"
        else:
            tag = "<input type='checkbox' name='pk' value='{0}' />".format(obj.pk)
            return mark_safe(tag)


    list_display = [
        checkbox,
        "article_id",
        "article_title",
        "article_summary",
        "article_read_count",
        "article_comment_count",
        "article_up_count",
        "article_down_count",
        "article_picture",
        "article_create_time",
        "article_blog",
        "article_category",
        "article_type_id",
        "tags",
        "article_sync_id",
        func,
    ]

wind_core.site.register(models.Article, ArticleWind)


class ArticleDetialWind(wind_core.BaseWind):
    def func(self, obj=None, is_header=False):
        if is_header:
            return "操作"
        else:
            name = "{0}:{1}_{2}_change".format(self.site_object.name_space, self.model_class._meta.app_label,
                                               self.model_class._meta.model_name)
            url = reverse(name, args=(obj.pk,))
            return mark_safe("<a href='{0}'>编辑</a>".format(url))

    def checkbox(self, obj=None, is_header=False):
        if is_header:
            return "选项"
        else:
            tag = "<input type='checkbox' name='pk' value='{0}' />".format(obj.pk)
            return mark_safe(tag)

    class myMForm(forms.ModelForm):
        class Meta:
            model = ArticleDetail
            fields = '__all__'

    add_or_edit_model_form = myMForm
    list_display = [
        checkbox,
        "articledeatail_article",
        "articledeatail_content",
        func,
    ]

wind_core.site.register(models.ArticleDetail, ArticleDetialWind)


class CategoryWind(wind_core.BaseWind):
    list_display = [
        "category_id",
        "category_title",
        "category_blog"
    ]

wind_core.site.register(models.Category, CategoryWind)


class TagWind(wind_core.BaseWind):
    list_display = [
        "tag_id",
        "tag_title",
        "tag_blog"
    ]

wind_core.site.register(models.Tag, TagWind)