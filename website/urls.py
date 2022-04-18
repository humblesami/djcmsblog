from django.apps import apps
from django.http import JsonResponse
from urllib.parse import unquote
from django.urls import path

from .views import WordImprovement, ShowQueryResults, QueryPage, SaveSqlReport, GetTableColumns


def next_prev_id(request):
    data = request.GET
    row_id = data.get('row_id')
    app = data.get('app')
    model = data.get('model')

    model = apps.get_model(app, model)
    nex = model.objects.filter(id__gt=row_id).order_by('id').first()
    prev = model.objects.filter(id__lt=row_id).order_by('id').last()
    res = {}
    if prev:
        res['prev'] = prev.id
    else:
        if model.objects.all().count():
            qs = model.objects.all().order_by("-id")
            res['prev'] = qs[0].id
    if nex:
        res['next'] = nex.id
    else:
        if model.objects.all().count():
            qs = model.objects.all().order_by("id")
            res['next'] = qs[0].id
    return JsonResponse(res)


def decode_unicode_url(request, url_string):
    if url_string.endswith('%258'):
        url_string = url_string.substring(0, len(url_string) - 4)
    if url_string.endswith('%DB%8'):
        url_string = url_string[:len(url_string) - 5]
    res = unquote(url_string)
    res = "".join([ch for ch in res if ord(ch) <= 9999])
    res = {'status': 'success', 'data': res}
    return JsonResponse(res)


urlpatterns = [
    path('get-next-prev-id/', next_prev_id),
    path('save-sql-report/', SaveSqlReport.as_view()),
    path('query-page/', QueryPage.as_view()),
    path('get_columns/', GetTableColumns.as_view()),
    # path('query-page/', TemplateView.as_view(template_name='website/query.html')),
    path('exec_query/', ShowQueryResults.as_view()),
    path('get_improvement/<word>/', WordImprovement.as_view()),
    path('save_improvement/', WordImprovement.as_view()),
]
