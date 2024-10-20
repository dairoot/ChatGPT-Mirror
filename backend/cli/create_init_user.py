import os
import sys

import django

cur_path = os.path.abspath(__file__)
parent = os.path.dirname
sys.path.append(parent(parent(cur_path)))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

if __name__ == "__main__":
    from app.accounts.models import User
    from app.settings import FREE_ACCOUNT_USERNAME, ADMIN_USERNAME, ADMIN_PASSWORD

    if not ADMIN_USERNAME:
        raise Exception("未设置 超级管理员账密")


    defaults = {"remark": "超级管理员", "isolated_session": False}
    user, created = User.objects.get_or_create(username=ADMIN_USERNAME, defaults=defaults)
    user.set_password(ADMIN_PASSWORD)
    user.is_staff = True
    user.is_active = True
    user.is_superuser = True

    user.save()
    print("Superuser created.")

    defaults = {
        "remark": "用于免费体验",
        "is_active": False,
        "isolated_session": True,
        "model_limit": [
            {"every_minute": 1, "limit_count": 3, "model_name": "gpt-4"},
            {"every_minute": 1, "limit_count": 3, "model_name": "gpt-4o"},
            {"every_minute": 1, "limit_count": 3, "model_name": "gpt-4o-mini"},
            {"every_minute": 1, "limit_count": 1, "model_name": "o1-mini"},
            {"every_minute": 1, "limit_count": 1, "model_name": "o1-preview", }
        ]
    }
    user, created = User.objects.get_or_create(username=FREE_ACCOUNT_USERNAME, defaults=defaults)
    user.is_superuser = False
    user.save()
    print("Freeuser created.")
