"""
Inventory demand forecasting.

This module implements a simple forecasting algorithm that predicts
next week's demand based on the mean and trend of the last 30 days
of sales.
"""

from typing import Iterable
import numpy as np


class InventoryForecaster:
    def predict_demand(self, last_30_days_sales: Iterable[int]) -> int:
        """Predict demand for the next 7 days given daily sales data.

        Uses a linear trend model: demand = average + trend * 7.
        Ensures that the result is at least 1.
        """
        data = np.array(list(last_30_days_sales), dtype=float)
        if len(data) < 2:
            return max(int(np.sum(data)), 1)
        avg = data.mean()
        trend = (data[-1] - data[0]) / max(len(data) - 1, 1)
        forecast = avg + trend * 7
        return max(int(round(forecast)), 1)