from sigma.order import Order
from sigma.order_side import OrderSide
from sigma.order_type import OrderType
from sigma.price_level import PriceLevel


class OrderBook:
    def __init__(self):
        self.bids = {}
        self.asks = {}
        self.orders = {}

    def add_order(self, order):
        if not isinstance(order, Order):
            raise TypeError(f"order must be Order, got {type(order)}")

        if order.order_type != OrderType.LIMIT:
            raise ValueError("OrderBook currently supports only LIMIT orders")

        if order.order_id in self.orders:
            raise ValueError(
                f"order with id {order.order_id} already exists"
            )

        levels = self.bids if order.side == OrderSide.BUY else self.asks

        if order.price not in levels:
            levels[order.price] = PriceLevel(order.price)

        levels[order.price].add_order(order)
        self.orders[order.order_id] = order

    def remove_order(self, order):
        if not isinstance(order, Order):
            raise TypeError(f"order must be Order, got {type(order)}")

        levels = self.bids if order.side == OrderSide.BUY else self.asks

        if order.price not in levels:
            raise ValueError(
                f"price level {order.price} does not exist"
            )

        level = levels[order.price]
        level.remove_order(order)

        if order.order_id in self.orders:
            del self.orders[order.order_id]

        if not level.orders:
            del levels[order.price]

    def cancel_order(self, order_id):
        if order_id not in self.orders:
            return False

        order = self.orders[order_id]
        self.remove_order(order)

        return True

    def get_best_bid_order(self):
        if self.best_bid is None:
            return None

        return self.bids[self.best_bid].first_order

    def get_best_ask_order(self):
        if self.best_ask is None:
            return None

        return self.asks[self.best_ask].first_order

    @property
    def best_bid(self):
        if not self.bids:
            return None

        return max(self.bids)

    @property
    def best_ask(self):
        if not self.asks:
            return None

        return min(self.asks)

    @property
    def spread(self):
        if self.best_bid is None or self.best_ask is None:
            return None

        return self.best_ask - self.best_bid

    def get_bids(self):
        return [
            self.bids[price]
            for price in sorted(self.bids, reverse=True)
        ]

    def get_asks(self):
        return [
            self.asks[price]
            for price in sorted(self.asks)
        ]

    def __repr__(self):
        return (
            f"OrderBook("
            f"best_bid={self.best_bid}, "
            f"best_ask={self.best_ask}, "
            f"spread={self.spread})"
        )