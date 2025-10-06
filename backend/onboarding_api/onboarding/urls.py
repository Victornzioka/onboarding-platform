from django.urls import path
from .views import FormListView, SubmissionCreateView

urlpatterns = [
    path('forms/', FormListView.as_view(), name='form-list'),
    path('submit/', SubmissionCreateView.as_view(), name='form-submit'),
]
