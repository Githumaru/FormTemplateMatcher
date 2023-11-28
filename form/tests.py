from django.test import TestCase, Client
from .models import FormTemplate
from pymongo import MongoClient

class GetFormDataViewTest(TestCase):

    def setUp(self):
        # Create a sample FormTemplate for testing
        FormTemplate.objects.create(
            name='Sample Template',
            field_name_1='phone',
            field_name_2='date',
        )

        self.client = Client()

    def test_matching_template(self):
        # Insert sample data into the MongoDB collection
        c = MongoClient('full_form-db-1')
        db = c['forms_database']
        collection = db['form_templates']
        collection.insert_one({
            'name': 'Sample Template',
            'field_name_1': 'phone',
            'field_name_2': 'date',
        })
        # Make a GET request with matching data
        response = self.client.get('/get_form/', {'field1': 'test@email.com', 'field_name_1': '+7 123 456 78 90', 'field_name_2': '2023-11-23'})

        # Remove the sample data from the collection
        collection.remove({'name': 'Sample Template'})
        # Check if the response contains the expected template name
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['matched_template_name'], 'Sample Template')

    def test_no_matching_template(self):
        # Insert sample data into the MongoDB collection
        c = MongoClient('full_form-db-1')
        db = c['forms_database']
        collection = db['form_templates']
        collection.insert_one({
            'name': 'Sample Template',
            'field_name_1': 'phone',
            'field_name_2': 'date',
        })

        # Make a GET request with data that doesn't match any template
        response = self.client.get('/get_form/', {'field1': 'text', 'field2': '123', 'field3': '2023-11-23'})

        # Remove the sample data from the collection
        collection.remove({'name': 'Sample Template'})

        # Check if the response contains the received data as JSON
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'field1': 'text', 'field2': 'text', 'field3': 'date'})

    def test_dynamic_type_inference(self):
        # Insert sample data into the MongoDB collection
        c = MongoClient('full_form-db-1')
        db = c['forms_database']
        collection = db['form_templates']
        collection.insert_one({
            'name': 'Sample Template',
            'field_name_1': 'phone',
            'field_name_2': 'date',
        })

        # Make a GET request with data that requires dynamic type inference
        response = self.client.get('/get_form/', {'field1': 'test@email.com'})

        # Remove the sample data from the collection
        collection.remove({'name': 'Sample Template'})

        # Check if the response contains the inferred types as JSON
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'field1': 'email'})

    def test_empty_data(self):
        # Insert sample data into the MongoDB collection
        c = MongoClient('full_form-db-1')
        db = c['forms_database']
        collection = db['form_templates']
        collection.insert_one({
            'name': 'Sample Template',
            'field_name_1': 'phone',
            'field_name_2': 'date',
        })

        # Make a GET request with no data
        response = self.client.get('/get_form/')

        # Remove the sample data from the collection
        collection.remove({'name': 'Sample Template'})
        
        # Check if the response contains an empty dictionary
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {})
