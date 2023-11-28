from django.db import models

class FormTemplate(models.Model):
    name = models.CharField(max_length=100)
    # Поля для типов данных: email, телефон, дата, текст
    FIELD_TYPES = [
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('date', 'Date'),
        ('text', 'Text')
    ]
    field_name_1 = models.CharField(max_length=100, choices=FIELD_TYPES)
    field_name_2 = models.CharField(max_length=100, choices=FIELD_TYPES)
    # Добавьте другие поля, если необходимо

