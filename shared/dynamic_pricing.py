"""
Dynamic pricing engine.

This module provides a basic algorithm for adjusting a product's price
based on demand, inventory and competitor pricing.  It is designed to
be illustrative rather than production-ready.
"""

from dataclasses import dataclass


@dataclass
class PricingInputs:
    base_price: float
    demand_factor: float  # 0.0 (low demand) to 1.0 (high demand)
    stock_level: int
    competitor_price: float


class DynamicPricing:
    def adjust_price(self, inputs: PricingInputs) -> float:
        """Compute a new price based on demand, stock and competitor pricing.

        - Increase price when demand is high or stock is low.
        - Decrease price when competitor prices are lower.
        """
        price = inputs.base_price
        # Adjust price proportionally to demand
        price *= 1.0 + 0.2 * inputs.demand_factor
        # If stock is low, apply a scarcity premium
        if inputs.stock_level < 5:
            price *= 1.10
        # Adjust relative to competitor
        if inputs.competitor_price > 0 and price > inputs.competitor_price:
            price = (price + inputs.competitor_price) / 2.0
        return round(price, 2)