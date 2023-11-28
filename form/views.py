from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import FormTemplate
from pymongo import MongoClient
import re

# Function to validate data based on regular expressions for different types
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

# Django view for home page
def home(request):
    return HttpResponse("Welcome to the home page!")

# Django view for handling GET requests to get form data
def get_form_data(request):
    # Creating a MongoClient
    client = MongoClient('full_form-db-1')

    # Select the database and collection
    db = client['forms_database']
    collection = db['form_templates']

    if request.method == 'GET':
        # Get the form data from the request
        form_data = request.GET
        # Fetching all form templates from the collection
        all_form_templates = list(collection.find({}))
        # Validating the received form data
        received_data = {key: validate_data(value) for key, value in form_data.items()}
        # List to store matching templates
        matching_templates = []

        # Loop through each template in the collection
        for template in all_form_templates:
            # Extracting template data without '_id' and 'name'
            template_dict = dict(filter(lambda x: x[0] != '_id' and x[0] != 'name', template.items()))

            # Checking if all items in the received data are present in the template
            if all(items in received_data.items() for items in template_dict.items()):
                return JsonResponse({'matched_template_name': template['name']})
            
        # If no matching template found, return received data
        return JsonResponse(received_data)




