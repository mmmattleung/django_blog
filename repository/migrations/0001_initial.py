# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-05-15 06:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('article_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('article_title', models.CharField(max_length=128, verbose_name='文章标题')),
                ('article_summary', models.CharField(max_length=255, verbose_name='文章简介')),
                ('article_read_count', models.IntegerField(default=0)),
                ('article_comment_count', models.IntegerField(default=0)),
                ('article_up_count', models.IntegerField(default=0)),
                ('article_down_count', models.IntegerField(default=0)),
                ('article_create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('article_type_id', models.IntegerField(choices=[(1, 'Python'), (2, 'Linux'), (3, 'OpenStack'), (4, 'GoLang')], default=None)),
            ],
        ),
        migrations.CreateModel(
            name='Article2Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.Article', verbose_name='文章')),
            ],
        ),
        migrations.CreateModel(
            name='ArticleDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('articledeatail_content', models.TextField(verbose_name='文章内容')),
                ('articledeatail_article', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='repository.Article', verbose_name='所属文章')),
            ],
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('blog_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('blog_title', models.CharField(max_length=64, verbose_name='个人博客标题')),
                ('blog_site', models.CharField(max_length=32, unique=True, verbose_name='个人博客前缀')),
                ('blog_theme', models.CharField(max_length=32, verbose_name='博客主题')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category_id', models.AutoField(primary_key=True, serialize=False)),
                ('category_title', models.CharField(max_length=32, verbose_name='分类标题')),
                ('category_blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.Blog', verbose_name='所属博客')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('comment_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('comment_content', models.CharField(max_length=255, verbose_name='评论内容')),
                ('comment_create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('comment_article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.Article', verbose_name='评论文章')),
                ('comment_reply', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='back', to='repository.Comment', verbose_name='回复评论')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('tag_id', models.AutoField(primary_key=True, serialize=False)),
                ('tag_title', models.CharField(max_length=32, verbose_name='标签名称')),
                ('tag_blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.Blog', verbose_name='所属博客')),
            ],
        ),
        migrations.CreateModel(
            name='UpDown',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updown_up', models.BooleanField(verbose_name='是否赞')),
                ('updown_article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.Article', verbose_name='文章')),
            ],
        ),
        migrations.CreateModel(
            name='UserFans',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('userinfo_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('userinfo_name', models.CharField(max_length=32, unique=True, verbose_name='用户名')),
                ('userinfo_password', models.CharField(max_length=64, verbose_name='密码')),
                ('userinfo_nickname', models.CharField(max_length=32, verbose_name='昵称')),
                ('userinfo_email', models.EmailField(max_length=254, unique=True, verbose_name='邮箱')),
                ('userinfo_avatar', models.ImageField(upload_to='', verbose_name='头像')),
                ('userinfo_create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('userinfo_fans', models.ManyToManyField(related_name='f', through='repository.UserFans', to='repository.UserInfo', verbose_name='粉丝们')),
            ],
        ),
        migrations.AddField(
            model_name='userfans',
            name='userfan_follower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='repository.UserInfo', verbose_name='粉丝'),
        ),
        migrations.AddField(
            model_name='userfans',
            name='userfan_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='repository.UserInfo', verbose_name='博主'),
        ),
        migrations.AddField(
            model_name='updown',
            name='updown_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.UserInfo', verbose_name='赞或踩用户'),
        ),
        migrations.AddField(
            model_name='comment',
            name='comment_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.UserInfo', verbose_name='评论者'),
        ),
        migrations.AddField(
            model_name='blog',
            name='blog_user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='repository.UserInfo'),
        ),
        migrations.AddField(
            model_name='article2tag',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.Tag', verbose_name='标签'),
        ),
        migrations.AddField(
            model_name='article',
            name='article_blog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.Blog', verbose_name='所属博客'),
        ),
        migrations.AddField(
            model_name='article',
            name='article_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='repository.Category', verbose_name='文章类型'),
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(through='repository.Article2Tag', to='repository.Tag'),
        ),
        migrations.AlterUniqueTogether(
            name='userfans',
            unique_together=set([('userfan_user', 'userfan_follower')]),
        ),
        migrations.AlterUniqueTogether(
            name='updown',
            unique_together=set([('updown_article', 'updown_user')]),
        ),
        migrations.AlterUniqueTogether(
            name='article2tag',
            unique_together=set([('article', 'tag')]),
        ),
    ]
