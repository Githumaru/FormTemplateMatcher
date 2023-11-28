import pymongo


client = pymongo.MongoClient('full_form-db-1')

db = client['forms_database']

collection = db['form_templates']

collection.delete_many({})

form_templates = [
    {
        "name": "Registration Form",
        "username": "text",
        "email": "email",
    },
    {
        "name": "Contact Form",
        "full_name": "text",
        "phone": "phone",
    },
    {
        "name": "Feedback Form",
        "email": "email",
        "message": "text",
    },
    {
        "name": "Survey Form",
        "question": "text",
        "email": "email",
    },
    {
        "name": "Job Application Form",
        "email": "email",
        "resume": "text",
    },
    {
        "name": "Appointment Booking Form",
        "phone": "phone",
        "appointment_date": "date",
    },
    {
        "name": "Product Feedback Form",
        "product_name": "text",
        "feedback_message": "text",
    },
    {
        'name': 'Order Form',
        'client phone': 'phone',
        'order date': 'date',
    },
    {
        'name':'Sample Template',
        'field_name_1':'phone',
        'field_name_2':'date',
    }
]

# Добавление документов в коллекцию
result = collection.insert_many(form_templates)

# Закрытие соединения с базой данных
client.close()