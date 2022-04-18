import json

from MySQLdb import connect
from django.conf import settings
from django.core import serializers
from django.db import connection
from django.utils.timesince import timesince


def execute_update(query):
    cr = connection.cursor()
    res = cr.execute(query)
    return res


def stringify_fields(dict_object):
    if dict_object.get('updated_at'):
        dict_object['updated_at'] = str(dict_object['updated_at'])
    if dict_object.get('created_at'):
        dict_object['created_at'] = str(dict_object['created_at'])
    if dict_object.get('updated_by'):
        dict_object['updated_by'] = str(dict_object['updated_by'])
    if dict_object.get('created_by'):
        dict_object['created_by'] = str(dict_object['created_by'])


def execute_read(query):
    cr = connection.cursor()
    cr.execute(query)
    col_names = [desc[0] for desc in cr.cursor.description]
    rows = cr.fetchall()
    res_list = []
    for row in rows:
        row_dict = {}
        i = 0
        for col in col_names:
            row_dict[col] = row[i]
            i += 1
        res_list.append(row_dict)
    return res_list


def pluck_column(query, params=None):
    cr = connection.cursor()
    if params:
        cr.execute(query, params)
    else:
        cr.execute(query)
    rows = cr.fetchall()
    column_values = [str(row[0]) for row in rows]
    return column_values


def get_json_list(qs, columns=None):
    dict_list = []
    qs_values = []
    if columns:
        qs_values = qs.values(*columns)
    else:
        qs_values = qs.values()
    dict_list = list(qs_values)
    return dict_list


def convert_time(arr, col, covert_type=None):
    for item in arr:
        item[col] = timesince(item[col])


def get_json_str(qs, columns=None):
    dict_list = []
    if not columns:
        serializers.serialize("json", qs)
    else:
        dict_list = serializers.serialize("json", qs, fields=columns)
    return dict_list


def get_serialized_json(qs, columns=None):
    dict_str = get_json_str(qs, columns)
    dict_list = json.loads(dict_str)
    rows = []
    for row in dict_list:
        rec = row['fields']
        rec['id'] = row['pk']
        rows.append(rec)
    return rows


def add_in_args(arr):
    ss = []
    [ss.append('%s') for s in arr]
    return ",".join(ss)


def dict_fetch_all(query, params=None):
    res = dict_fetch_all_head_body(query, params)
    return res['body']


def dict_fetch_all_head_body(query, params=None):
    if not query:
        return []
    cr = connection.cursor()
    if params:
        if len(params):
            cr.execute(query, params)
        else:
            cr.execute(query)
    else:
        cr.execute(query)
    desc = cr.description
    head = []
    res = {'head': head}
    all_rows = cr.fetchall()
    if desc:
        res['head'] = [item[0] for item in desc]
        res['body'] = [dict(zip([col[0] for col in desc], row)) for row in all_rows]
    else:
        res['body'] = []
    return res


def read_only_db(query, params=None):
    database_info = {}
    site_path = str(settings.BASE_DIR)
    config_path = site_path + '/config.json'
    with open(config_path, 'r') as site_config:
        config_info = json.load(site_config)
        active_conn = config_info.get('active_conns')
        database_info = active_conn.get('mysql_readonly')
    conn = connect(host="localhost", user=database_info['USER'], database=database_info['NAME'],
                   passwd=database_info['PASSWORD'], charset='utf8')
    conn.autocommit = False
    cr = conn.cursor()
    if params:
        if len(params):
            cr.execute(query, params)
        else:
            cr.execute(query)
    else:
        cr.execute(query)
    desc = cr.description
    head = []
    res = {'columns': head}
    all_rows = cr.fetchall()
    if desc:
        res['columns'] = [item[0] for item in desc]
        res['rows'] = [cell for cell in [row for row in all_rows]]
    else:
        res['rows'] = []
    return res
    