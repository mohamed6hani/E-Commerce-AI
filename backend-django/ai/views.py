from django.http import JsonResponse
from django.views.decorators.http import require_GET
from products.models import Product

import sys
from pathlib import Path

# Add project root to sys.path for importing shared modules
ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from shared.dynamic_pricing import DynamicPricing, PricingInputs  # type: ignore
except ImportError:
    DynamicPricing = None


@require_GET
def dynamic_price(request):
    try:
        product_id = int(request.GET.get('product_id'))
        demand_factor = float(request.GET.get('demand_factor', '0.5'))
        competitor_price = float(request.GET.get('competitor_price', '0'))
        product = Product.objects.get(id=product_id)
        if DynamicPricing is None:
            return JsonResponse({'error': 'AI module unavailable'}, status=500)
        dp = DynamicPricing()
        inputs = PricingInputs(
            base_price=product.price,
            demand_factor=demand_factor,
            stock_level=product.stock,
            competitor_price=competitor_price,
        )
        price = dp.adjust_price(inputs)
        return JsonResponse({'product_id': product_id, 'dynamic_price': price})
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)