from sigma.order import Order


class PriceLevel:
    def __init__(self, price):
        if price <= 0:
            raise ValueError("price must be greater than 0")

        self.price = price
        self.orders = []

    def add_order(self, order):
        if not isinstance(order, Order):
            raise TypeError(f"order must be Order, got {type(order)}")

        if order.price != self.price:
            raise ValueError(
                f"order price {order.price} does not match level price {self.price}"
            )

        self.orders.append(order)

    @property
    def first_order(self):
        if not self.orders:
            return None

        return self.orders[0]

    def remove_order(self, order):
        if order not in self.orders:
            raise ValueError(
                f"order {order.order_id} does not exist at price level {self.price}"
            )

        self.orders.remove(order)

    def remove_filled_orders(self):
        self.orders = [
            order
            for order in self.orders
            if order.remaining_quantity > 0
        ]

    @property
    def total_quantity(self):
        return sum(order.remaining_quantity for order in self.orders)

    def __repr__(self):
        return (
            f"PriceLevel("
            f"price={self.price}, "
            f"orders={len(self.orders)}, "
            f"quantity={self.total_quantity})"
        )