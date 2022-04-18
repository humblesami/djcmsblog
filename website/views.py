import json

from django.conf import settings
from django.shortcuts import render
from django.utils.text import slugify
from rest_framework.response import Response
from rest_framework.views import APIView

from .db import dict_fetch_all, read_only_db, pluck_column
from .methods import get_error_message
from .models import RomanWord, StandardLanguage, SqlReport
from django.views import View


class ShowQueryResults(APIView):
    def get(self, request):
        response_data = {'status': 'error', 'message': 'Unknown issue'}
        try:
            query = request.GET.get('query')
            data = read_only_db(query)
            response_data = {'status': 'success', 'data': data}
        except Exception as e:
            message = str(e)
            if 'Access denied for' not in message:
                message = get_error_message()
            response_data['message'] = message
        return Response(response_data)


class QueryPage(View):
    template_name = 'website/query.html'
    
    def get(self, request):
        reports = []
        context = {'rows': [], 'report_name': '', 'query': '', 'reports': reports}
        try:
            db_name = settings.DATABASES['default']['NAME']
            query = f"""
            select table_name from information_schema.tables where table_schema='{db_name}'
            and TABLE_TYPE='BASE TABLE'
            and table_name not like 'django_%' and table_name not like 'auth_%'
            """
            db_tables = pluck_column(query)
            reports = dict_fetch_all('select * from db_query')
            query = ''
            count_query = ''
            report_name = request.GET.get('report') or ''
            if report_name:
                repo = SqlReport.objects.filter(name=report_name).first()
                if repo:
                    query, count_query = make_query_from_report(repo, request.GET.get('pno'))
                else:
                    query, count_query = make_query_from_request(request)
                        
            context = {
                'db_tables': db_tables,
                'report_name': report_name,
                'report_query': query,
                'reports': reports
            }
            if query:
                report_data = read_only_db(query)
                context['data'] = report_data
            if count_query:
                count_data = read_only_db(query)
                context['row_count'] = count_data[0][0]
            return render(request, self.template_name, context)
        except Exception as e:
            message = str(e)
            if request.GET.get('full_error'):
                message = get_error_message()
            context['error'] = message
            return render(request, self.template_name, context)


def make_query_from_report(repo, pno=0):
    report_tables = repo.tables
    if not report_tables:
        return '', ''
    selects = f"select {repo.columns} from {report_tables[0]} "
    count_query = f"select count(*) from (select {report_tables[0]}.id from {report_tables[0]} "
    query = ""
    if repo.joins:
        query += repo.joins
    
    if repo.where:
        query += ' where ' + repo.where
    
    if repo.group_by:
        query += ' group by ' + repo.group_by
        
        if repo.having:
            query += ' having ' + repo.having
    
    count_query = count_query + ' ' + query
    if repo.page_size:
        page_size = repo.page_size
        query += f' limit {pno * page_size},{page_size}'
    query = selects + ' ' + query
    return query, count_query


def make_query_from_request(request):
    report_tables = request.GET.get('tables')
    if not report_tables:
        return '', ''
    selects = f"select {request.GET.get('columns')} from {report_tables[0]} "
    count_query = f"select count(*) from (select {report_tables[0]}.id from {report_tables[0]} "
    query = ""
    ar = request.GET.get('joins')
    if len(ar):
        joins = ' '.join(ar)
        query += joins
    
    ar = request.GET.get('where')
    if len(ar):
        where = ' '.join(ar)
        query += where
    
    ar = request.GET.get('group_by')
    if len(ar):
        group_by = ','.join(ar)
        query += group_by
        
        ar = request.GET.get('having')
        if len(ar):
            having = ','.join(ar)
            query += having
    
    count_query = count_query + ' ' + query
    
    page_size = request.GET.get('page_size')
    if page_size:
        pno = request.GET.get('pno') or 0
        query += f' limit {pno * page_size},{page_size}'
    query = selects + ' ' + query
    return query, count_query


class GetTableColumns(APIView):
    def get(self, request):
        query = ''
        response_data = {'status': 'error', 'query': query}
        try:
            table = request.GET.get('table')
            db_name = settings.DATABASES['default']['NAME']
            query_params = f"select column_name from information_schema.columns where table_name=%s and table_schema=%s"
            query = f"""
            select column_name from information_schema.columns where table_name='{table}' and table_schema='{db_name}'
            """
            data = pluck_column(query_params, [table, db_name])
            # data = pluck_column(query)
            response_data = {'status': 'success', 'data': data}
        except Exception as e:
            message = str(e)
            # message = get_error_message()
            response_data['message'] = message
            response_data['query'] = query
        return Response(response_data)
    

class SaveSqlReport(APIView):
    def get(self, request):
        response_data = {'status': 'error'}
        try:
            report_name = request.GET.get('report_name')
            query = request.GET.get('query')
            page_size = request.GET.get('page_size')
            columns = request.GET.get('columns')
            slug = slugify(report_name)
            obj = SqlReport.objects.filter(slug=slug).first()
            if obj:
                obj.query = query
                obj.page_size = page_size
                obj.name = report_name
                obj.save()
            else:
                SqlReport.objects.create(query=query, name=report_name, slug=slug, page_size=page_size)
            response_data = {'status': 'success', 'message': 'done'}
        except Exception as e:
            message = str(e)
            # message = get_error_message()
            response_data['message'] = message
        return Response(response_data)


class WordImprovement(APIView):

    def get(self, request, word):
        response_data = {'status': 'error', 'message': 'Unknown issue'}
        try:
            if word:
                query = "SELECT id,name,improvement from roman_word where name = %s"
                res_list = dict_fetch_all(query, [word])
                improvement = word
                if len(res_list):
                    improvement = res_list[0]['improvement']
                response_data = {'status': 'success', 'data': improvement}
            else:
                response_data = {'status': 'error', 'message': 'No words specified'}
        except:
            message = get_error_message()
            response_data['message'] = message
        return Response(response_data)

    def post(self, request):
        response_data = {'status': 'error', 'message': 'Unknown issue'}
        try:
            word = request.data.get('word')
            improvement = request.data.get('improvement')
            words = RomanWord.objects.filter(name=word)
            if words.count():
                words[0].imrovement = improvement
                words[0].save()
            else:
                lang = StandardLanguage.objects.get_or_create(name='urdu', code='ur')
                RomanWord.objects.create(name=word, lang_id=lang[0].id, improvement=improvement)
            response_data = {'status': 'success', 'data': 'done'}
        except Exception as e:
            message = str(e)
            response_data['message'] = message
        return Response(response_data)
