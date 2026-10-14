from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Product


def list_products(request):
    products = list(Product.objects.values())
    return JsonResponse(products, safe=False)


@csrf_exempt
def create_product(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    try:
        data = json.loads(request.body)
        product = Product.objects.create(
            title=data.get('title', ''),
            description=data.get('description', ''),
            category=data.get('category', ''),
            price=data.get('price', 0),
            stock=data.get('stock', 0),
            image_url=data.get('image_url', ''),
        )
        return JsonResponse({'id': product.id}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)