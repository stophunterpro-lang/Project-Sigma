from sigma.order_side import OrderSide
from sigma.order_status import OrderStatus
from sigma.order_type import OrderType


class Order:
    def __init__(
        self,
        order_id,
        user_id,
        side,
        order_type,
        price,
        quantity,
        timestamp,
    ):
        if not isinstance(side, OrderSide):
            raise TypeError(
                f"side must be OrderSide, got {type(side)}"
            )

        if not isinstance(order_type, OrderType):
            raise TypeError(
                f"order_type must be OrderType, got {type(order_type)}"
            )

        if quantity <= 0:
            raise ValueError(
                "quantity must be greater than zero"
            )

        if order_type == OrderType.LIMIT:
            if price is None or price <= 0:
                raise ValueError(
                    "LIMIT order price must be greater than zero"
                )

        if order_type == OrderType.MARKET:
            if price is not None:
                raise ValueError(
                    "MARKET order price must be None"
                )

        self.order_id = order_id
        self.user_id = user_id
        self.side = side
        self.order_type = order_type
        self.price = price

        self.original_quantity = quantity
        self.remaining_quantity = quantity

        self.timestamp = timestamp
        self.status = OrderStatus.NEW

    def fill(self, quantity):
        if quantity <= 0:
            raise ValueError(
                "fill quantity must be greater than zero"
            )

        if quantity > self.remaining_quantity:
            raise ValueError(
                "fill quantity exceeds remaining quantity"
            )

        self.remaining_quantity -= quantity

        if self.remaining_quantity == 0:
            self.status = OrderStatus.FILLED
        else:
            self.status = OrderStatus.PARTIALLY_FILLED

    def __repr__(self):
        return (
            f"Order("
            f"id={self.order_id}, "
            f"side={self.side.name}, "
            f"type={self.order_type.name}, "
            f"price={self.price}, "
            f"remaining={self.remaining_quantity}, "
            f"status={self.status.name})"
        )