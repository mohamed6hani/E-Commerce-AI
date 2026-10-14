from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Order
from users.models import User


def list_orders(request):
    orders = list(Order.objects.values())
    return JsonResponse(orders, safe=False)


@csrf_exempt
def create_order(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    try:
        data = json.loads(request.body)
        user = User.objects.get(id=data['user_id'])
        order = Order.objects.create(
            user=user,
            total=data.get('total', 0),
            status=data.get('status', 'pending'),
        )
        return JsonResponse({'id': order.id}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)