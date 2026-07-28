from sigma.order_side import OrderSide


class Trade:
    def __init__(
        self,
        trade_id,
        buy_order_id,
        sell_order_id,
        price,
        quantity,
        aggressor_side,
        timestamp,
    ):
        if price <= 0:
            raise ValueError("price must be greater than 0")

        if quantity <= 0:
            raise ValueError("quantity must be greater than 0")

        if not isinstance(aggressor_side, OrderSide):
            raise TypeError(
                f"aggressor_side must be OrderSide, got {type(aggressor_side)}"
            )

        self.trade_id = trade_id
        self.buy_order_id = buy_order_id
        self.sell_order_id = sell_order_id
        self.price = price
        self.quantity = quantity
        self.aggressor_side = aggressor_side
        self.timestamp = timestamp

    def __repr__(self):
        return (
            f"Trade("
            f"id={self.trade_id}, "
            f"price={self.price}, "
            f"quantity={self.quantity}, "
            f"aggressor={self.aggressor_side.name})"
        )