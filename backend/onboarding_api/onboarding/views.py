from rest_framework import generics, status
from rest_framework.response import Response
from .models import Form, Submission
from .serializers import FormSerializer, SubmissionSerializer


class FormListView(generics.ListAPIView):
    """
    GET /api/forms/
    Returns a list of all available forms with their fields.
    """
    queryset = Form.objects.prefetch_related("fields").all()
    serializer_class = FormSerializer


class SubmissionCreateView(generics.CreateAPIView):
    """
    POST /api/submit/
    Accepts multipart/form-data submissions from the frontend.
    Automatically reconstructs nested responses.
    """
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        structured_responses = []

        # --- STEP 1: Build structured responses from request.data ---
        for key, value in data.items():
            if key.startswith("responses["):
                index = int(key.split("[")[1].split("]")[0])
                field_name = key.split("][")[-1].replace("]", "")
                while len(structured_responses) <= index:
                    structured_responses.append({})

                # Convert field ID from string to integer
                if field_name == "field":
                    try:
                        value = int(value)
                    except (ValueError, TypeError):
                        pass

                structured_responses[index][field_name] = value

        # --- STEP 2: Include uploaded files ---
        for key, file in request.FILES.items():
            if key.startswith("responses["):
                index = int(key.split("[")[1].split("]")[0])
                field_name = key.split("][")[-1].replace("]", "")
                while len(structured_responses) <= index:
                    structured_responses.append({})
                structured_responses[index][field_name] = file

        # --- STEP 3: Flatten nested lists if any ---
        if len(structured_responses) == 1 and isinstance(structured_responses[0], list):
            structured_responses = structured_responses[0]

        print("=== CLEAN RESPONSES ===")
        print(structured_responses)

        # --- STEP 4: Prepare payload for serializer ---
        payload = {
            "form": data.get("form"),
            "client_name": data.get("client_name"),
            "client_email": data.get("client_email"),
            "responses": structured_responses,
        }

        # --- STEP 5: Validate and save ---
        serializer = self.get_serializer(data=payload)
        if not serializer.is_valid():
            print("=== VALIDATION ERRORS ===")
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
