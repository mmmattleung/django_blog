#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import git
import hashlib
from repository import models


git_address = "/Users/mingleung/Study/StudyRound2/SICP/SICP/"
copy_address = "/Users/mingleung/Study/StudyRound2/SICP/SICP/6/"

cons_dict = {
    "content":
        {
            "article_title": "",
            "article_summary": "",
            "article_read_count": 0,
            "article_comment_count": 0,
            "article_up_count": 0,
            "article_down_count": 0,
            "article_blog_id": 1,
            "article_category_id": 7,
            "article_type_id": 5,
            "article_sync_id": "",
        },
    "detail":
        {
            "articledeatail_content": "",
            "articledeatail_article": "",
        }
}

def get_git_data():
    repo = git.Repo(git_address)
    # print(repo.git.status())
    # print(repo.is_dirty())

    remote = repo.remote()
    remote.pull()
    # print(repo.git.status())
    # print(repo.is_dirty())


def process():
    file_dirs = os.listdir(copy_address)
    for file_dir in file_dirs:
        if file_dir.split(".")[1] == "md":
            # It's md file, read it
            with open(copy_address+file_dir, "r") as f:
                data = f.readlines()
                data_string = "".join(data)
                tmp = cons_dict["content"]

                title = " ".join(data[0][2:].split())
                tmp["article_title"] = title
                tmp["article_summary"] = title

                m = hashlib.md5()
                m.update(bytes(tmp["article_title"], encoding='utf8'))
                md5_key = m.hexdigest()
                tmp["article_sync_id"] = md5_key

                if not cheack_exit(md5_key):
                    # save to db
                    article_id = write_to_db(models.Article, tmp)

                    tmp_contnet = cons_dict["detail"]
                    tmp_contnet["articledeatail_content"] = data_string
                    tmp_contnet["articledeatail_article"] = article_id

                    write_to_db(models.ArticleDetail, tmp_contnet)
                else:
                    print("文章存在")


def write_to_db(model_class, data_dict):
    print(data_dict)
    print("---------")
    new_data_id = model_class.objects.create(**data_dict)
    return new_data_id


def cheack_exit(md5_key):
    return models.Article.objects.filter(article_sync_id=md5_key).first()



if __name__ == '__main__':
    process()