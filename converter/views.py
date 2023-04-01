import json
from lxml import etree

import xmltodict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from json import dumps, loads
from dicttoxml import dicttoxml
from django.http import HttpResponse

from testsite import settings


from django.conf import settings


def validate_xml(xml_string, xsd_string):
    xmlschema = etree.XMLSchema(etree.fromstring(xsd_string))
    xml_doc = etree.fromstring(xml_string)
    return xmlschema.validate(xml_doc)


def get_xsd_string(path):
    with open(path, 'r') as xsd_file:
        xsd_content = xsd_file.read()
    return xsd_content


@csrf_exempt
def to_xml(request):
    if request.method == 'POST':

        json_data = loads(request.body)

        data_dict = json_data if isinstance(json_data, dict) else json.loads(json_data.decode('utf-8'))

        xml_data = dicttoxml(data_dict, custom_root='EntrantChoice')
        if isinstance(xml_data, str):
            xml_data = xml_data.encode('utf-8')

        if getattr(settings, 'VALIDATE_WITH_XSD', False):
            xsd_string = get_xsd_string("converter/validation/Add_Entrant_List.xsd")
            if isinstance(xsd_string, str):
                xsd_string = xsd_string.encode('utf-8')
            is_valid = validate_xml(xml_data, xsd_string)
            if not is_valid:
                return JsonResponse({'error': 'XML validation failed'})

        return HttpResponse(xml_data, content_type='application/xml')
    else:
        return JsonResponse({'error': 'Invalid request method'})


@csrf_exempt
def from_xml(request):

    if request.method == 'POST':
        # XML передается в сериализованном виде в связи с этим ее надо декодировать в utf
        xml_string = request.body
        # переводим ее в dict
        xml_dict = xmltodict.parse(xml_string)

        if getattr(settings, 'VALIDATE_WITH_XSD', False):
            xsd_string = get_xsd_string("converter/validation/Get_Entrant_List.xsd")
            if isinstance(xsd_string, str):
                xsd_string = xsd_string.encode('utf-8')
            is_valid = validate_xml(xml_string, xsd_string)
            if not is_valid:
                return JsonResponse({'error': 'XML validation failed'})

        # indent существует строго для красоты и не несет смысла
        return JsonResponse(xml_dict, json_dumps_params={'indent': 2})