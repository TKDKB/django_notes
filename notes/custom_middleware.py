from django.utils.deprecation import MiddlewareMixin
from pathlib import Path
import os
import datetime
from django.conf import settings
from django_last_hope import settings

# PATH_FOR_LOGS = "usersActivity.log"


class LogsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # if os.path.exists('usersActivity.log'):
        #     with open('usersActivity.log', 'r') as f:
        #         for i, _ in enumerate(f):
        #             pass
        #         lines_amount = i
        #         if lines_amount == 101:
        #             f.truncate(0)
        with open(settings.PATH_FOR_LOGS, 'a') as f:
            f.write(f"{datetime.datetime.now()} | {request.user.username} | {request.get_full_path()}\n")

