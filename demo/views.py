import numpy as np
from django.http import JsonResponse
from demo.models import DIM, FIFLD_PREV, TestData
import time


def index(request):
    '''
    统计数据量
    :param request:
    :return:
    '''
    data_number = TestData.count()
    return JsonResponse({'status': 'success', 'data_number': data_number})


def insert(request):
    '''
    批量插入数据
    :param request:
    :return:
    '''
    data_number = int(request.GET.get('data_number', 20000))
    new_data = np.random.rand(data_number, DIM)
    query_list = []
    start = time.time()
    for label, n in enumerate(new_data):
        tr = {'label': time.time()}
        for i in range(1, DIM + 1):
            tr['%s%s' % (FIFLD_PREV, i)] = n[i - 1]
        query_list.append(TestData(**tr))
    end = time.time()
    print(end - start)
    TestData.bulk_create(query_list)
    return JsonResponse({'status': 'success'})


def select_by_paramid(request):
    '''
    查询某列最新100条用于画趋势图
    :param request:
    :return:
    '''
    param_id = int(request.GET.get('param_id', 1))
    fifld_name = '%s%s' % (FIFLD_PREV, param_id)
    values = ('id', 'label', fifld_name)
    data_number = TestData.count()
    start_index = data_number - 100 if data_number >= 100 else 0
    data_list = TestData.objects.values(*values).order_by('id')[start_index:]
    return JsonResponse({'status': 'success', 'data_list': [[d['id'], d['label'], d[fifld_name]] for d in data_list]})
