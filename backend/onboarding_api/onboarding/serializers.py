from rest_framework import serializers
from .models import Form, Field, Submission, SubmissionField

class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = '__all__'

class FormSerializer(serializers.ModelSerializer):
    fields = FieldSerializer(many=True)

    class Meta:
        model = Form
        fields = ['id', 'name', 'description', 'fields']

class SubmissionFieldSerializer(serializers.ModelSerializer):
    # 👇 Tell DRF that 'field' is a foreign key expecting an ID (int)
    field = serializers.PrimaryKeyRelatedField(queryset=Field.objects.all())

    class Meta:
        model = SubmissionField
        fields = ["field", "value", "file"]


class SubmissionSerializer(serializers.ModelSerializer):
    responses = SubmissionFieldSerializer(many=True)

    class Meta:
        model = Submission
        fields = ["id", "form", "client_name", "client_email", "responses"]

    def create(self, validated_data):
        responses_data = validated_data.pop("responses", [])
        submission = Submission.objects.create(**validated_data)
        for r in responses_data:
            SubmissionField.objects.create(submission=submission, **r)
        return submission
