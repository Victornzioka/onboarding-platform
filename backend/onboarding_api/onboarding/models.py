from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField

FIELD_TYPES = [
    ('text', 'Text'),
    ('number', 'Number'),
    ('date', 'Date'),
    ('dropdown', 'Dropdown'),
    ('checkbox', 'Checkbox'),
    ('file', 'File Upload'),
]

class Form(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Field(models.Model):
    form = models.ForeignKey(Form, related_name='fields', on_delete=models.CASCADE)
    label = models.CharField(max_length=255)
    field_type = models.CharField(max_length=50, choices=FIELD_TYPES)
    required = models.BooleanField(default=False)
    options = models.JSONField(blank=True, null=True)  # for dropdowns
    validation = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.label} ({self.form.name})"


class Submission(models.Model):
    form = models.ForeignKey(Form, related_name='submissions', on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    client_name = models.CharField(max_length=255, blank=True, null=True)
    client_email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"Submission {self.id} for {self.form.name}"


class SubmissionField(models.Model):
    submission = models.ForeignKey(Submission, related_name='responses', on_delete=models.CASCADE)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    value = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='uploads/', blank=True, null=True)

    def __str__(self):
        return f"{self.field.label}: {self.value or 'file upload'}"
