import hashlib
import json
import time

import requests
from rest_framework.exceptions import ValidationError

from app.accounts.models import VisitLog
from app.settings import ADMIN_PASSWORD


def generate_md5(input_string):
    md5_object = hashlib.md5()
    md5_object.update(input_string.encode('utf-8'))
    return md5_object.hexdigest()


def req_gateway(method, url, *args, **kwargs):
    headers = {
        "Authorization": "Bearer {}".format(ADMIN_PASSWORD),
    }
    res = requests.request(method, url, headers=headers, *args, **kwargs)
    if res.status_code != 200:
        raise ValidationError(res.text)

    return res.json()


def clean_int_list(data_list):
    if isinstance(data_list, str):
        data_list = json.loads(data_list)

    new_list = []
    for i in data_list:
        if isinstance(i, int):
            new_list.append(i)
        elif isinstance(i, str) and i.isdigit():
            new_list.append(int(i))

    return new_list


def save_visit_log(request, log_type, chatgpt_username=None):
    ip = (request.headers.get('cf-connecting-ip') or
          request.META.get('HTTP_X_FORWARDED_FOR') or
          request.META.get('REMOTE_ADDR'))

    VisitLog.save_data({
        "ip": ip,
        "log_type": log_type,
        "chatgpt_username": chatgpt_username,
        "username": request.user.username,
        "created_at": int(time.time()),
        "user_agent": request.headers.get('User-Agent'),
    })
