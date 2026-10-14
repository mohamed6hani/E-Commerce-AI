from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import User


@csrf_exempt
def register(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    try:
        data = json.loads(request.body)
        if User.objects.filter(email=data['email']).exists():
            return JsonResponse({'error': 'Email already registered'}, status=400)
        user = User.objects.create(
            name=data.get('name', ''),
            email=data['email'],
            password=data['password'],
        )
        return JsonResponse({'id': user.id}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
def login(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    try:
        data = json.loads(request.body)
        user = User.objects.filter(email=data['email'], password=data['password']).first()
        if not user:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
        return JsonResponse({'message': 'Login successful', 'id': user.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)