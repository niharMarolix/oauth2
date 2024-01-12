from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from oauth2_provider.decorators import protected_resource
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest, JsonResponse
from oauth2_provider.models import AccessToken, RefreshToken, get_application_model
from django.utils import timezone
from .utils import token_generator


import json

@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
    email, username, password = data.get("email"), data.get("username"), data.get("password")

    if email is None or username is None or password is None:
        return JsonResponse({"status": "failed", "message": "incompolete input(s)"})
    
    userObjSaving = User.objects.create_user(username=username, email=email, password=password)

    return JsonResponse({
        "status":"Success",
        "message":"User registered successfully"
    })

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            expiration_time = timezone.now() + timezone.timedelta(minutes=5)

            Application = get_application_model()
            application = Application.objects.get(name='oauthApp2')
            refresh_token_value = token_generator.make_token(user)
            refresh_token = RefreshToken.objects.create(
                user=user,
                application=application,
                access_token=access_token,
                token=refresh_token_value
            )

            access_token_value = token_generator.make_token(user)
            access_token = AccessToken.objects.create(
                user=user,
                application=application,
                scope='read write',
                expires=expiration_time,
                token=access_token_value
            )

            

            return JsonResponse({
                'message': 'Login successful',
                'access_token': access_token.token,
                'refresh_token': refresh_token.token  # Make sure to check if this is now being generated
            })

        return JsonResponse({'message': 'Invalid credentials'}, status=401)

    return HttpResponseBadRequest('Invalid request method')