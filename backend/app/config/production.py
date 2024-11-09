import os
from pathlib import Path

DEBUG = False

FREE_ACCOUNT_USERNAME = "free_account"

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
CHATGPT_GATEWAY_URL = os.environ.get("CHATGPT_GATEWAY_URL")
ALLOW_REGISTER = os.environ.get("ALLOW_REGISTER", "true") == "true"

BASE_DIR = Path(__file__).resolve().parent.parent
log_file_path = os.path.join(BASE_DIR, os.pardir, 'logs/cron.log > /dev/null 2>&1')

CRONJOBS = [
    ('*/5 * * * *', 'app.cron.check_access_token', f'>> {log_file_path}'),
    ('*/5 * * * *', 'app.cron.update_access_token', f'>> {log_file_path}'),
]
