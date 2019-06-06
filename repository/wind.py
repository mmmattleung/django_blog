from wind_admin import wind_core
from repository import models


class UserInfoWind(wind_core.BaseWind):
    list_display = [
        "userinfo_id",
        "userinfo_name",
        "userinfo_password",
        "userinfo_nickname",
        "userinfo_email",
        "userinfo_avatar",
        "userinfo_avatar_full",
        "userinfo_create_time",
        "userinfo_fans",
        "userinfo_introdution",
        "userinfo_speciality",
        "userinfo_skills",
        "userinfo_education_and_experience",
        "userinfo_portfolo",
    ]

wind_core.site.register(models.UserInfo, UserInfoWind)

