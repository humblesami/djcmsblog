import sys
import traceback
from django.db import connection
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Special commands'

    def add_arguments(self, parser):
        pass
        # parser.add_argument('-hard', '--hard', help='drop database if exists and create new one')

    def execute_query(self, query):
        db_cursor = connection.cursor()
        db_cursor.execute(query)
        res = db_cursor.fetchall()
        db_cursor.close()
        return res

    def copy_post_tags(self):
        query = 'insert into post_tags (post_id,meta_id) select post_id,meta_id from meta_tags'
        self.execute_query(query)

    def handle(self, *args, **kwargs):
        try:
            self.execute_query()
            pass
        except:
            eg = traceback.format_exception(*sys.exc_info())
            error_message = ''
            cnt = 0
            for er in eg:
                cnt += 1
                if not 'lib/python' in er and not 'lib\site-packages' in er:
                    error_message += " " + er
            print('Error ' + error_message)
