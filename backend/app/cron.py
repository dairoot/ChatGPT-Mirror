# myapp/cron.py
import logging
import time

import requests

from app.chatgpt.models import ChatgptAccount
from app.settings import ADMIN_PASSWORD
from app.settings import CHATGPT_GATEWAY_URL

logger = logging.getLogger("cron")


def _update_token(chatgpt_token):
    url = CHATGPT_GATEWAY_URL + "/api/get-user-info"
    headers = {"Authorization": "Bearer {}".format(ADMIN_PASSWORD)}
    res = requests.post(url, headers=headers, json={"chatgpt_token": chatgpt_token})
    res_json = res.json()
    if res.status_code == 400:
        print(res_json)
        return False

    ChatgptAccount.save_data(res_json)
    return True


def update_token():
    need_to_update = int(time.time() - 3600 * 6)
    # need_to_update = int(time.time() - 0)
    for line in ChatgptAccount.objects.filter(updated_time__lte=need_to_update).all():
        update_status = False

        if line.refresh_token:
            update_status = _update_token(line.refresh_token)
            if not update_status:
                line.refresh_token = None
                line.save()

        elif line.session_token:
            update_status = _update_token(line.session_token)
            if not update_status:
                line.session_token = None
                line.save()

        if update_status:
            logger.info(f"access_token 刷新成功: {line.chatgpt_username}")
            return

        if line.access_token:
            if not _update_token(line.access_token):
                line.auth_status = False
                line.updated_time = int(time.time())
                line.save()

                logger.warning(f"access_token 刷新失败，access_token已经过期: {line.chatgpt_username}")
                return

        logger.info(f"access_token 刷新失败，但 access_token 仍然有效: {line.chatgpt_username}")
