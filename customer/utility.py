from __future__ import absolute_import, unicode_literals
from plateiq.settings import MEDIA_ROOT
import datetime

def upload_file(file_name, customer_name, customer_id, file_data):
    today_date = datetime.datetime.now().strftime('%Y%m%d')
    file_path = "{}{}/{}_{}".format(MEDIA_ROOT, customer_id, today_date, file_name)

    with open(file_path, 'wb+') as download_file:
        for chunk in file_data.chunks():
            download_file.write(chunk)

    return True, file_path
    