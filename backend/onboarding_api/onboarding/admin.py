from django.contrib import admin
from .models import Form, Field, Submission, SubmissionField

class FieldInline(admin.TabularInline):
    model = Field
    extra = 1

@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    inlines = [FieldInline]

admin.site.register(Submission)
admin.site.register(SubmissionField)
