from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import FormTemplate
from pymongo import MongoClient
import re




def validate_data(data):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    phone_regex = r'^[\s+]7\s\d{3}\s\d{3}\s\d{2}\s\d{2}$'
    date_regex = r'^(?:(?:0[1-9]|1\d|2[0-8])\.(?:0[1-9]|1[0-2])\.\d{4}|(?:29|30|31)\.(?:0[13578]|1[02])\.\d{4}|29\.02\.(?:(?:19|20)(?:[02468][048]|[13579][26])|(?:[2468][048]|[13579][26])00))$|^\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|1\d|2[0-8])$|^(?:19|20)\d{2}-(?:0[1-9]|1[0-2])-29$'
    if re.match(email_regex, data):
        return 'email'
    elif re.match(phone_regex, data):
        return 'phone'
    elif re.match(date_regex, data):
        return 'date'
    else:
        return 'text'

    
def home(request):
    return HttpResponse("Welcome to the home page!")


def get_form_data(request):
    client = MongoClient('full_form-db-1')

    # Select the database and collection
    db = client['forms_database']
    collection = db['form_templates']
    if request.method == 'GET':

        # Получаем данные из POST запроса
        form_data = request.GET


        # Получаем все шаблоны форм из базы данных
        all_form_templates = list(collection.find({}))



        # Преобразуем данные из POST запроса в словарь
        received_data = {key: validate_data(value) for key, value in form_data.items()}


        # Список для хранения соответствующих шаблонов форм
        matching_templates = []

        # Проходим по всем шаблонам форм и проверяем совпадения полей
        for template in all_form_templates:

            template_dict = dict(filter(lambda x: x[0] != '_id' and x[0] != 'name', template.items()))

            # Проверяем соответствие полей шаблона формы и полученных данных
            if all(items in received_data.items() for items in template_dict.items()):
                return JsonResponse({'matched_template_name': template['name']})
            
        return JsonResponse(received_data)




