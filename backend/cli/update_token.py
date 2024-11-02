import os
import sys

import django

cur_path = os.path.abspath(__file__)
parent = os.path.dirname
sys.path.append(parent(parent(cur_path)))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

if __name__ == "__main__":
    from app.cron import check_access_token, update_access_token
    check_access_token()
    update_access_token()


