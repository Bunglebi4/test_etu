import io
from lxml import etree
from django.http import JsonResponse
from django.http import HttpResponse
from testsite import settings
from django.conf import settings
from xmlschema import XMLSchema


def validate_xml(xml_string, xsd_string):
    xmlschema = etree.XMLSchema(etree.fromstring(xsd_string))
    xml_doc = etree.fromstring(xml_string)
    return xmlschema.validate(xml_doc)


def get_xsd_string(path):
    with open(path, 'r') as xsd_file:
        xsd_content = xsd_file.read()
    return xsd_content


def xsd_validation(xml, xsd_path):
    with open(xsd_path, encoding='utf-8') as xsd_file:
        xml_schema = XMLSchema(xsd_file)
    xml_data = io.BytesIO(xml)
    is_valid = xml_schema.is_valid(xml_data)
    return is_valid


def json_transforming(json_f):
    new_json = {
        "EntrantChoice": {
            "AddEntrant": {
                "Identification": {
                    "IdDocumentType": json_f["id"],
                    "DocName": "passport",
                    "DocSeries": json_f["passport_number"],
                    "DocNumber": json_f["passport_begda"],
                    "IssueDate": "2004-05-02",
                    "DocOrganization": json_f["passport_org_code"] if not None else '0'
                },
                "Snils": int(json_f['snils']),
                "IdGender": json_f['dict_sex_id'],
                "Birthday": json_f['birthday'],
                "Birthplace": json_f['motherland'],
                "Phone": json_f["tel_mobile"],
                "Email": json_f["email"],
                "IdOksm": json_f["user_id"],
                "FreeEducationReason": {
                    "IdFreeEducationReason": 2707
                },
                "AddressList": {
                    "Address": [
                        {
                            "IsRegistration": True,
                            "FullAddr": json_f['address_txt1'],
                            "IdRegion": 41,
                            "City": json_f['motherland']
                        },
                        {
                            "IsRegistration": False,
                            "FullAddr": "string",
                            "IdRegion": 445,
                            "City": "string"
                        },
                        {
                            "IsRegistration": 1,
                            "FullAddr": "string",
                            "IdRegion": 8065,
                            "City": "string"
                        },
                        {
                            "IsRegistration": False,
                            "FullAddr": "string",
                            "IdRegion": 4330,
                            "City": "string"
                        }
                    ]
                }
            }
        }
    }
    return new_json


def json_to_xml(data, parent):
    for key, value in data.items():
        if isinstance(value, dict):
            child = etree.SubElement(parent, key)
            json_to_xml(value, child)
        elif isinstance(value, list):
            for item in value:
                child = etree.SubElement(parent, key)
                json_to_xml(item, child)
        else:
            child = etree.SubElement(parent, key)
            if str(value) == 'True':
                child.text = str('true')
            elif str(value) == 'False':
                child.text = str('false')
            else:
                child.text = str(value)


def convert_json_to_xml(json_obj):
    root_name = list(json_obj.keys())[0]
    root = etree.Element(root_name)
    json_to_xml(json_obj[root_name], root)
    data = etree.tostring(root)
    if getattr(settings, 'VALIDATE_WITH_XSD', False):
        if xsd_validation(data, 'converter/validation_data/Add_Entrant_List.xsd'):
            return HttpResponse(data, content_type='application/xml')
        else:
            return JsonResponse({'error': 'XML validation failed'})
    else:
        return JsonResponse({'error': 'XML validation failed'})
