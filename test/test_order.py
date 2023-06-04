
import pytest

from src.models.user_model import Order
from src.schemas.order_schemas import OrderResponse


def test_get_order(auth_client_advance, test_order, test_items_order):
    order_id = test_order.id
    res = auth_client_advance.get(f"/order/{order_id}")
    print(res.json()["total"])
    assert res.status_code == 200
    assert len(res.json()["order_items"]) == len(test_items_order)

@pytest.mark.parametrize("total, status, items_order", [
    (0, "canceled", [12,45,78]),
    (0, "paid", [54,88,33]),
    (0, "canceled", [44,88,22]),
])
def test_create_order(auth_client, test_product, test_customer, total, status, items_order,):
    res = auth_client.post(
        "/order/", json={"total": total, "status": status, "items_order": [{"qty": i, "product_id": test_product.id} for i in items_order]})

    created_order = OrderResponse(**res.json())
    # assert res.status_code == 201
