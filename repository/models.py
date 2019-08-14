from django.db import models
from mdeditor.fields import MDTextField
from django.utils.html import format_html


class UserInfo(models.Model):
    """
    用户表
    """
    userinfo_id = models.BigAutoField(primary_key=True, verbose_name="ID")
    userinfo_name = models.CharField(verbose_name='用户名', max_length=32, unique=True)
    userinfo_password = models.CharField(verbose_name='密码', max_length=64)
    userinfo_nickname = models.CharField(verbose_name='昵称', max_length=32)
    userinfo_email = models.EmailField(verbose_name='邮箱', unique=True)
    userinfo_avatar = models.ImageField(verbose_name='头像', upload_to="static/avatar")
    userinfo_avatar_full = models.ImageField(verbose_name='头像', blank=True, null=True, upload_to="static/avatar")

    userinfo_create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    # userinfo_fans = models.ForeignKey(to='UserFans', to_field='userfan_user')
    userinfo_fans = models.ManyToManyField(verbose_name='粉丝们',
                                  null=True,
                                  blank=True,
                                  to='UserInfo',
                                  through='UserFans',
                                  related_name='f',
                                  through_fields=('userfan_user', 'userfan_follower'))
    userinfo_introdution = models.TextField(verbose_name="简介")
    userinfo_speciality = models.CharField(max_length=64, verbose_name="特长")
    userinfo_skills = models.CharField(max_length=256, verbose_name="技能", blank=True, null=True)
    userinfo_education_and_experience = models.TextField(verbose_name="教育和经验", blank=True, null=True)
    userinfo_portfolo = models.TextField(verbose_name="作品", blank=True, null=True)

    def __str__(self):
        return "%s - %s" % (self.userinfo_id, self.userinfo_name)

    def text_username(self):
        return self.userinfo_name

    def value_username(self):
        return self.userinfo_name


class Blog(models.Model):
    """
    博客信息
    """
    blog_id = models.BigAutoField(primary_key=True)
    blog_title = models.CharField(verbose_name='个人博客标题', max_length=64)
    blog_site = models.CharField(verbose_name='个人博客前缀', max_length=32, unique=True)
    blog_theme = models.CharField(verbose_name='博客主题', max_length=32)
    blog_user = models.OneToOneField(to='UserInfo', to_field='userinfo_id')

    def __str__(self):
        return "%s - %s" % (self.blog_title, self.blog_site)


class UserFans(models.Model):
    """
    互粉关系表
    """
    userfan_user = models.ForeignKey(verbose_name='博主', to='UserInfo', to_field='userinfo_id', related_name='users')
    userfan_follower = models.ForeignKey(verbose_name='粉丝', to='UserInfo', to_field='userinfo_id', related_name='followers')

    class Meta:
        unique_together = [
            ('userfan_user', 'userfan_follower'),
        ]


class Category(models.Model):
    """
    博主个人文章分类表
    """
    category_id = models.AutoField(primary_key=True)
    category_title = models.CharField(verbose_name='分类标题', max_length=32)

    category_blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='blog_id')

    def __str__(self):
        return "%s - %s" % (self.category_id, self.category_title)


class ArticleDetail(models.Model):
    """
    文章详细表
    """
    articledeatail_content = MDTextField(blank=True, null=True, verbose_name='文章内容')

    articledeatail_article = models.OneToOneField(verbose_name='所属文章', to='Article', to_field='article_id')




class UpDown(models.Model):
    """
    文章顶或踩
    """
    updown_article = models.ForeignKey(verbose_name='文章', to='Article', to_field='article_id')
    updown_user = models.ForeignKey(verbose_name='赞或踩用户', to='UserInfo', to_field='userinfo_id')
    updown_up = models.BooleanField(verbose_name='是否赞')

    class Meta:
        unique_together = [
            ('updown_article', 'updown_user'),
        ]


class Comment(models.Model):
    """
    评论表
    """
    comment_id = models.BigAutoField(primary_key=True)
    comment_content = models.CharField(verbose_name='评论内容', max_length=255)
    comment_create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    comment_reply = models.ForeignKey(verbose_name='回复评论', to='self', related_name='back', null=True)
    comment_article = models.ForeignKey(verbose_name='评论文章', to='Article', to_field='article_id')
    comment_user = models.ForeignKey(verbose_name='评论者', to='UserInfo', to_field='userinfo_id')


class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    tag_title = models.CharField(verbose_name='标签名称', max_length=32)
    tag_blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='blog_id')

    def __str__(self):
        return "%s - %s" % (self.tag_id, self.tag_title)


class Article(models.Model):
    article_id = models.BigAutoField(primary_key=True)
    article_title = models.CharField(verbose_name='文章标题', max_length=128)
    article_summary = models.CharField(verbose_name='文章简介', max_length=255)
    article_read_count = models.IntegerField(default=0)
    article_comment_count = models.IntegerField(default=0)
    article_up_count = models.IntegerField(default=0)
    article_down_count = models.IntegerField(default=0)
    article_picture = models.ImageField(verbose_name="配图", upload_to="static/article_pic", blank=True, null=True)
    article_create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    article_blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='blog_id')
    article_category = models.ForeignKey(verbose_name='文章类型', to='Category', to_field='category_id', null=True)

    type_choices = [
        (1, "Python"),
        (2, "Data Structure And Algorithm"),
        (3, "Marx's philosophy"),
        (4, "Buddhism"),
        (5, "SICP"),
        (6, "Others"),
    ]

    article_type_id = models.IntegerField(choices=type_choices, default=None)

    tags = models.ManyToManyField(
        to="Tag",
        through='Article2Tag',
        through_fields=('article', 'tag'),
    )

    article_sync_id = models.CharField(max_length=128, verbose_name="同步编号", blank=True, null=True, unique=True)

    def __str__(self):
        return "%s - %s" % (self.article_id, self.article_title)


class Article2Tag(models.Model):
    article = models.ForeignKey(verbose_name='文章', to="Article", to_field='article_id')
    tag = models.ForeignKey(verbose_name='标签', to="Tag", to_field='tag_id')

    class Meta:
        unique_together = [
            ('article', 'tag'),
        ]

