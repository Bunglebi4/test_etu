import json
import xmltodict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from json import dumps, loads
from dicttoxml import dicttoxml

@csrf_exempt
def to_xml(request):
    if request.method == 'POST':
        # Получаем JSON из запроса
        json_data = loads(request.body)
        # Конвертируем JSON в словарь
        data_dict = json_data if isinstance(json_data, dict) else json.loads(json_data.decode('utf-8'))
        # Конвертируем словарь в XML и возвращаем его как ответ на запрос
        xml_data = dicttoxml(data_dict, custom_root='root')
        from django.http import HttpResponse
        return HttpResponse(xml_data, content_type='application/xml')
    else:
        return JsonResponse({'error': 'Invalid request method'})


@csrf_exempt
def from_xml(request):

    if request.method == 'POST':
        # XML передается в сериализованном виде в связи с этим ее надо декодировать в /тв
        xml_string = request.body.decode('utf-8')
        # переводим ее в dict
        xml_dict = xmltodict.parse(xml_string)
        # indent существует строго для красоты и не несет смысла
        return JsonResponse(xml_dict, json_dumps_params={'indent': 2})