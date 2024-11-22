# myapp/cron.py
import logging
import time

import jwt
import requests

from app.chatgpt.models import ChatgptAccount
from app.settings import ADMIN_PASSWORD
from app.settings import CHATGPT_GATEWAY_URL

logger = logging.getLogger("cron")


def _update_token(chatgpt_username, chatgpt_token):
    url = CHATGPT_GATEWAY_URL + "/api/get-user-info"
    headers = {"Authorization": "Bearer {}".format(ADMIN_PASSWORD)}
    res = requests.post(url, headers=headers, json={"chatgpt_token": chatgpt_token})
    res_json = res.json()

    if res.status_code == 400:
        logger.info("res_json", chatgpt_username, res_json)
        if "token 失效" in res_json.get("message", ""):
            return False
        return None

    res_json["auth_status"] = True
    ChatgptAccount.save_data(res_json)
    return True


def update_access_token():
    for line in ChatgptAccount.objects.all():
        try:
            at_info = jwt.decode(line.access_token, options={"verify_signature": False})
            if int(time.time()) < at_info["exp"] - 60 * 30 and line.auth_status:
                continue
        except:
            pass


        if line.refresh_token:
            update_status = _update_token(line.chatgpt_username, line.refresh_token)
            if update_status is False:
                line.refresh_token = None
                line.save()

        elif line.session_token:
            update_status = _update_token(line.chatgpt_username, line.session_token)
            if update_status is False:
                line.session_token = None
                line.save()



def check_access_token():
    need_to_update = int(time.time() - 3600)
    for line in ChatgptAccount.objects.filter(updated_time__lte=need_to_update, auth_status=True).all():
        if line.access_token:
            if not _update_token(line.chatgpt_username, line.access_token):
                line.auth_status = False
                line.updated_time = int(time.time())
                line.save()
                logger.warning(f"access_token已经过期: {line.chatgpt_username}")
                return
            else:
                logger.warning(f"access_token 有效: {line.chatgpt_username}")



