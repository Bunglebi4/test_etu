from json import loads
import xmltodict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from converter.untils import json_transforming, convert_json_to_xml, get_xsd_string, validate_xml
from testsite import settings
from django.conf import settings



@csrf_exempt
def to_xml(request):
    json_data = loads(request.body)
    json_data = json_transforming(json_data)
    return convert_json_to_xml(json_data)


@csrf_exempt
def from_xml(request):
    if request.method == 'POST':
        xml_string = request.body
        xml_dict = xmltodict.parse(xml_string)
        if getattr(settings, 'VALIDATE_WITH_XSD', False):
            xsd_string = get_xsd_string("converter/validation_data/Get_Entrant_List.xsd")
            if isinstance(xsd_string, str):
                xsd_string = xsd_string.encode('utf-8')
            is_valid = validate_xml(xml_string, xsd_string)
            if not is_valid:
                return JsonResponse({'error': 'XML validation failed'})
        return JsonResponse(xml_dict, json_dumps_params={'indent': 2})
