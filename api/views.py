from io import BytesIO
import time
import hashlib
from collections import defaultdict

from blog import settings
from django.db.models import Count
from django.db.models import functions
from django.utils.html import mark_safe
from django.shortcuts import render, HttpResponse, redirect

from rbac.service import initial_permission
from utils import pager, markdown_ex
from repository import models
from rbac import models as rbac_models
from markdown import markdown
from utils import random_check_code
from repository.forms import RegisterFrom, LoginForm



def index(request):
    user_info = models.UserInfo.objects.filter(userinfo_id=1).values(
        "userinfo_id",
        "userinfo_name",
        "userinfo_password",
        "userinfo_nickname",
        "userinfo_email",
        "userinfo_avatar",
        "userinfo_create_time",
        "userinfo_fans",
        "userinfo_introdution",
        "userinfo_speciality",
        "blog__blog_id"
    ).first()
    #
    articles = models.Article.objects.filter(article_blog=1).all().order_by("-article_create_time")[:5]

    categorys = models.Category.objects.filter(category_blog=1).values(
        "category_id",
        "category_title",
    ).annotate(c=Count("article__article_id"))

    tags = models.Article2Tag.objects.filter(article__article_blog=1).values(
        "tag",
        "tag__tag_title",
    ).annotate(c=Count("article__article_id"))

    times = models.Article.objects.filter(article_blog=1).extra(
        select={'c': "date_format(article_create_time,'%%Y-%%m')"}).values('c').annotate(ct=Count('article_id'))

    return render(request, 'index_test.html', {
        "categorys": categorys,
        "user_info": user_info,
        "articles": articles,
        "tags": tags,
        "times": times,
        "base_dir": settings.BASE_HOST
    })


def category(request, *args, **kwargs):
    articles = models.Article.objects.filter(**kwargs).all()
    category_info = models.Category.objects.filter(category_id=kwargs["article_category"]).first()

    return render(request, "category_test.html", {"articles": articles,
                                                  "category_info": category_info
                                                  })


def filter(request, *args, **kwargs):
    if kwargs["filter"] == "category":
        del kwargs["filter"]
        category_id = kwargs["id"]
        del kwargs["id"]


        articles = models.Article.objects.filter(article_blog=kwargs["article_blog"], article_category=category_id).all()
        category_info = models.Category.objects.filter(category_id=category_id).first()

        title_info = {
            "title": category_info.category_title,
            "description": "简介"
        }

        page_params = {"article_blog": kwargs["article_blog"], "filter": "category", "id": category_id}
        # 分页
        page_dict = pager.get_pager(request, articles, 5, "filter", **page_params)
        return render(request, "category_test.html", {
            "articles": articles,
            "base_dir": settings.BASE_HOST,
            "title_info": title_info,
            "p": page_dict["p"],
            "page_range": page_dict["page_range"],
            "reverse_url": page_dict["reverse_url"],
            "current_page": page_dict["current_page"]
          })
    if kwargs["filter"] == "tag":
        del kwargs["filter"]
        kwargs["article2tag__tag"] = kwargs["id"]
        del kwargs["id"]

        articles = models.Article.objects.filter(**kwargs).all()

        tags = models.Article2Tag.objects.filter(
            article__article_blog=kwargs["article_blog"],
            tag=kwargs["article2tag__tag"]
             ).values(
            "tag",
            "tag__tag_title")

        title_info = {
            "title": tags[0]["tag__tag_title"],
            "description": "简介"
        }
        page_params = {"article_blog": kwargs["article_blog"], "filter": "tag", "id": kwargs["article2tag__tag"]}
        page_dict = pager.get_pager(request, articles, 5, "filter", **page_params)
        return render(request, "category_test.html", {
            "articles": articles,
            "base_dir": settings.BASE_HOST,
            "title_info": title_info,
            "p": page_dict["p"],
            "page_range": page_dict["page_range"],
            "reverse_url": page_dict["reverse_url"],
            "current_page": page_dict["current_page"]
        })
    if kwargs["filter"] == "time":
        del kwargs["filter"]
        time = kwargs["id"]
        del kwargs["id"]

        articles = models.Article.objects.filter(
            article_blog=kwargs["article_blog"],
        ).extra(
            select={"t": "date_format(article_create_time,'%%Y-%%m')"},
            where=["date_format(article_create_time,'%%Y-%%m')=%s", ],
            params=[time, ]
        ).all()

        title_info = {
            "title": time,
            "description": "简介"
        }
        page_params = {"article_blog": kwargs["article_blog"], "filter": "tag", "id": time}
        page_dict = pager.get_pager(request, articles, 5, "filter", **page_params)

        return render(request, "category_test.html", {
            "articles": articles,
            "base_dir": settings.BASE_HOST,
            "title_info": title_info,
            "p": page_dict["p"],
            "page_range": page_dict["page_range"],
            "reverse_url": page_dict["reverse_url"],
            "current_page": page_dict["current_page"]
        })


def login(request, *args, **kwargs):
    if request.method == "GET":
        form = LoginForm(request)
        return render(request, 'login.html', {"form": form})
    else:
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = request.POST.get('userinfo_name')
            password = request.POST.get('userinfo_password')
            user = rbac_models.User.objects.filter(username=username, password=password).first()
            if user:
                initial_permission(request, user)
            return render(request, "backend_index.html")
        else:
            print(form.errors)
            return render(request, 'login.html', {"form": form})


def check_code(request, *args, **kwargs):
    img, code = random_check_code.rd_check_code()
    stream = BytesIO()
    img.save(stream, 'png')
    request.session['code'] = code
    return HttpResponse(stream.getvalue())


def register(request, *args, **kwargs):
    if request.method == "GET":
        print("GET")
        form = RegisterFrom(request)
        return render(request, 'register.html', {"obj": form})
    elif request.method == "POST":
        print("POST")
        obj = RegisterFrom(request, request.POST, request.FILES)
        if obj.is_valid():
            return HttpResponse("OK")
        else:
            print(obj.errors)
            return render(request, 'register.html', {"obj": obj})


def blog(request, blog_site):
    blog = models.Blog.objects.filter(blog_site=blog_site).first()

    if not blog:
        return redirect('/')

    categorys = models.Category.objects.all()
    user_info = models.UserInfo.objects.filter(userinfo_id=blog.blog_user.userinfo_id).values(
        "userinfo_id",
        "userinfo_name",
        "userinfo_password",
        "userinfo_nickname",
        "userinfo_email",
        "userinfo_avatar",
        "userinfo_create_time",
        "userinfo_fans",
        "userinfo_introdution",
        "userinfo_speciality",
        "blog__blog_id"
    ).first()

    articles = models.Article.objects.filter(article_blog=blog.blog_id).all()
    return render(request, 'index_test.html', {"categorys": categorys,
                                               "user_info": user_info,
                                               "articles": articles
                                               })


def article(request, *args, **kwargs):
    article = models.Article.objects.filter(**kwargs).values(
        "article_id",
        "article_title",
        "article_summary",
        "article_read_count",
        "article_comment_count",
        "article_up_count",
        "article_down_count",
        "article_picture",
        "article_create_time",
        "article_blog_id",
        "article_blog__blog_user__userinfo_nickname",
        "article_category__category_title",
        "article_category_id",
        "article_type_id",
        "articledetail__articledeatail_content",
    )

    articles = models.Article.objects.filter(article_blog=kwargs["article_blog"]).all()
    pre = None
    after = None

    for i in range(0, len(articles)):
        if articles[i].article_id == int(kwargs["article_id"]):
            if i != 0:
                pre = articles[i-1]
            else:
                pre = None
            if i < len(articles)-1:
                after = articles[i+1]
            else:
                after = None

    pre_and_after = {
        "pre": pre,
        "after": after
    }

    tags = models.Article2Tag.objects.filter(article=kwargs["article_id"]).all()

    configs = {}
    myext = markdown_ex.CodeExtension(configs=configs)
    content = mark_safe(markdown(article[0]["articledetail__articledeatail_content"], extensions=[myext]))
    # content = mark_safe(markdown(article[0]["articledetail__articledeatail_content"]))

    comments = models.Comment.objects.filter(comment_article=kwargs["article_id"]).values(
        "comment_id",
        "comment_content",
        "comment_create_time",
        "comment_reply",
        "comment_reply__comment_user__userinfo_nickname",
        "comment_article",
        "comment_user__userinfo_nickname",
        "comment_user__userinfo_avatar",
    )
    comments_dict = {}
    for c in comments:
        comments_dict[c["comment_id"]] = {"data": c}
        comments_dict[c["comment_id"]].setdefault("child", [])

    result = []

    def make_list(data_list):
        for key, value in data_list.items():
            if value["data"]["comment_reply"]:
                data_list[value["data"]["comment_reply"]]["child"].append(value)
            else:
                result.append(value)
        return result

    a = make_list(comments_dict)
    # print(a)
    tpl = """
        <div class="eskimo_comments">
                            <div class="eskimo_comment">
                                <div class="eskimo_comment_inner">
                                    <div class="eskimo_comment_left">
                                        <img alt='' src='{avatar}' />
                                    </div>
                                    <div class="eskimo_comment_right">
                                        <div class="eskimo_comment_right_inner ">
                                            <cite class="eskimo_fn">
                                                <a href='author.html'>{author}</a>
                                                {reply_to}
                                            </cite>
                                            <div class="eskimo_comment_links">
                                                <i class="fa fa-clock-o"></i>{time}- <a href="#">Reply</a>
                                            </div>
                                            <div class="eskimo_comment_text">
                                                <p>{content}</p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
        """
    tpl_reply_to = "<a href='author.html' style='display:inline-block;margin-left: 10px'>to: {origin}</a>"
    def make_tree(result):
        comment_str = '<div class="eskimo_comment_wrapper">'
        for i in result:
            if i["data"]["comment_reply__comment_user__userinfo_nickname"]:
                tmp_reply_to = tpl_reply_to.format(origin=i["data"]["comment_reply__comment_user__userinfo_nickname"])
                tmp = tpl.format(reply_to=tmp_reply_to,
                                 content=i["data"]["comment_content"],
                                 author=i["data"]["comment_user__userinfo_nickname"],
                                 time=i["data"]["comment_create_time"],
                                 avatar=settings.BASE_HOST+"/"+i["data"]["comment_user__userinfo_avatar"])
            else:
                tmp = tpl.format(reply_to="", content=i["data"]["comment_content"],
                                 author=i["data"]["comment_user__userinfo_nickname"],
                                 time=i["data"]["comment_create_time"],
                                 avatar=settings.BASE_HOST+"/"+i["data"]["comment_user__userinfo_avatar"]
                                 )
            comment_str += tmp
            if i["child"]:
                child_str = make_tree(i["child"])
                comment_str += child_str
        return comment_str

    comment_str = make_tree(a)

    return render(request, "article.html", {
        "article": article[0],
        "content": content,
        "tags": tags,
        "comment_str": comment_str,
        "pre_and_after": pre_and_after
    })


def comment(request, *args, **kwargs):
    comments = models.Comment.objects.filter(comment_article=1).values(
        "comment_id",
        "comment_content",
        "comment_create_time",
        "comment_reply",

        "comment_article",
        "comment_user__userinfo_nickname",
    )
    comments_dict = {}
    for c in comments:
        comments_dict[c["comment_id"]] = {"data": c}
        comments_dict[c["comment_id"]].setdefault("child", [])

    result = []
    def make_list(data_list):
        for key, value in data_list.items():
            if value["data"]["comment_reply"]:
                data_list[value["data"]["comment_reply"]]["child"].append(value)
            else:
                result.append(value)
        return result

    a = make_list(comments_dict)
    print(a)
    tpl = """
    <div class="eskimo_comments">
                        <div class="eskimo_comment">
                            <div class="eskimo_comment_inner">
                                <div class="eskimo_comment_left">
                                    <img alt='' src='http://0.gravatar.com/avatar/0b19666d0fc7a149e6f8f2319a04ef63?s=60&#038;d=mm&#038;r=g' />
                                </div>
                                <div class="eskimo_comment_right">
                                    <div class="eskimo_comment_right_inner ">
                                        <cite class="eskimo_fn">
                                            <a href='author.html'>{author}</a>
                                        </cite>
                                        <div class="eskimo_comment_links">
                                            <i class="fa fa-clock-o"></i>{time}- <a href="#">Reply</a>
                                        </div>
                                        <div class="eskimo_comment_text">
                                            <p>{content}</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
    """
    def make_tree(result):
        comment_str = '<div class="eskimo_comment_wrapper">'
        for i in result:
            tmp = tpl.format(content=i["data"]["comment_content"], author=i["data"]["comment_user__userinfo_nickname"], time=i["data"]["comment_create_time"])
            comment_str += tmp
            if i["child"]:
                child_str = make_tree(i["child"])
                comment_str += child_str
        return comment_str
    print(make_tree(a))

    return HttpResponse(123)


def blog_3colums(request, *args, **kwargs):
    articles = models.Article.objects.filter(article_blog=1).all()

    page_dict = pager.get_pager(request, articles, 9, "blog", **{"article_blog": 1})


    return render(request, "blog-3.html",
      {
          "base_dir": settings.BASE_HOST,
          "p": page_dict["p"],
          "page_range": page_dict["page_range"],
          "reverse_url": page_dict["reverse_url"],
          "current_page": page_dict["current_page"]
      }
    )


def about(request, *args, **kwargs):
    user_info = models.UserInfo.objects.filter(userinfo_id=1).first()

    skills = [
        {
            "name": "Python",
            "level": "100%",
            "style": "bg-primary",
        },
        {
            "name": "Django、Tornado、Flask",
            "level": "100%",
            "style": "bg-primary",
        },
        {
            "name": "MySql",
            "level": "80%",
            "style": "bg-info",
        },
        {
            "name": "Network Programming",
            "level": "80%",
            "style": "bg-info",
        },
        {
            "name": "HTML、CSS、JQuery",
            "level": "70%",
            "style": "bg-success",
        },
        {
            "name": "Linux",
            "level": "70%",
            "style": "bg-success",
        },
        {
            "name": "Machine Learning(Start-up)",
            "level": "60%",
            "style": "bg-warning",
        }
    ]

    experience = [
        {
            "id":1,
            "time_line": "2010 - 2013",
            "content": ["广东交通职业技术学院", "xxxxxxxxxxx"]
        },
        {
            "id": 2,
            "time_line": "2013 - 2017",
            "content": ["弱电系统工程师", "xxxxxxxxxxxx"]
        },
        {
            "id": 3,
            "time_line": "2017 - 2019",
            "content": ["Python 开发者", "xxxxxxxxxxxx"]
        },
        {
            "id": 4,
            "time_line": "2019 - Present",
            "content": ["华南理工大学（自考）", "xxxxxxxxxxxx"]
        }
    ]
    experience = reversed(experience)

    return render(request, "about_test.html", {
        "base_dir": settings.BASE_HOST,
        "user_info": user_info,
        "skills": skills,
        "experience": experience
    })


def galleries(request, *args, **kwargs):
    return render(request, "gallery_test.html", {
        "base_dir": settings.BASE_HOST
    })

from django.views.decorators.csrf import csrf_exempt,csrf_protect
import hmac
import subprocess
@csrf_exempt
def github(request, *args, **kwargs):
    signature = request.META.get('HTTP_X_HUB_SIGNATURE')
    print(request.META)
    print(request.body)

    sha, signature = signature.split('=')
    today = time.strftime("%Y-%m-%d", time.localtime(time.time()))


    hashhex = hmac.new(settings.SHA1_STR.encode("utf-8"), request.body, digestmod='sha1').hexdigest()
    print(hashhex)
    if hmac.compare_digest(hashhex, signature):
        a = "git --git-dir=/home/django_blog/.git  --work-tree=/home/django_blog pull"
        multi_task = subprocess.Popen(
	        a, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(multi_task.stdout.read())
        print(multi_task.stderr.read())
    else:
        print("NO")
    return HttpResponse(123)


def sync(request, *args, **kwargs):
    from utils import sync_github
    sync_github.get_git_data()

    sync_github.process()
    return HttpResponse("ok")