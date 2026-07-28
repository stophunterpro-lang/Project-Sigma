from datetime import datetime

from sigma.order import Order
from sigma.order_book import OrderBook
from sigma.order_side import OrderSide
from sigma.order_type import OrderType
from sigma.trade import Trade
from sigma.trade_feed import TradeFeed


class MatchingEngine:
    def __init__(self):
        self.order_book = OrderBook()
        self.trade_feed = TradeFeed()
        self.next_trade_id = 1

    @property
    def trades(self):
        return self.trade_feed.get_trades()

    def process_order(self, order):
        if not isinstance(order, Order):
            raise TypeError(f"order must be Order, got {type(order)}")

        if order.side == OrderSide.BUY:
            self._process_buy_order(order)
        else:
            self._process_sell_order(order)

    def cancel_order(self, order_id):
        return self.order_book.cancel_order(order_id)

    def _process_buy_order(self, buy_order):
        while (
            buy_order.remaining_quantity > 0
            and self.order_book.best_ask is not None
            and self._buy_can_match(buy_order)
        ):
            sell_order = self.order_book.get_best_ask_order()

            trade_quantity = min(
                buy_order.remaining_quantity,
                sell_order.remaining_quantity,
            )

            buy_order.fill(trade_quantity)
            sell_order.fill(trade_quantity)

            self._create_trade(
                buy_order=buy_order,
                sell_order=sell_order,
                price=sell_order.price,
                quantity=trade_quantity,
                aggressor_side=OrderSide.BUY,
            )

            if sell_order.remaining_quantity == 0:
                self.order_book.remove_order(sell_order)

        if (
            buy_order.remaining_quantity > 0
            and buy_order.order_type == OrderType.LIMIT
        ):
            self.order_book.add_order(buy_order)

    def _process_sell_order(self, sell_order):
        while (
            sell_order.remaining_quantity > 0
            and self.order_book.best_bid is not None
            and self._sell_can_match(sell_order)
        ):
            buy_order = self.order_book.get_best_bid_order()

            trade_quantity = min(
                sell_order.remaining_quantity,
                buy_order.remaining_quantity,
            )

            sell_order.fill(trade_quantity)
            buy_order.fill(trade_quantity)

            self._create_trade(
                buy_order=buy_order,
                sell_order=sell_order,
                price=buy_order.price,
                quantity=trade_quantity,
                aggressor_side=OrderSide.SELL,
            )

            if buy_order.remaining_quantity == 0:
                self.order_book.remove_order(buy_order)

        if (
            sell_order.remaining_quantity > 0
            and sell_order.order_type == OrderType.LIMIT
        ):
            self.order_book.add_order(sell_order)

    def _buy_can_match(self, buy_order):
        if buy_order.order_type == OrderType.MARKET:
            return True

        return buy_order.price >= self.order_book.best_ask

    def _sell_can_match(self, sell_order):
        if sell_order.order_type == OrderType.MARKET:
            return True

        return sell_order.price <= self.order_book.best_bid

    def _create_trade(
        self,
        buy_order,
        sell_order,
        price,
        quantity,
        aggressor_side,
    ):
        trade = Trade(
            trade_id=self.next_trade_id,
            buy_order_id=buy_order.order_id,
            sell_order_id=sell_order.order_id,
            price=price,
            quantity=quantity,
            aggressor_side=aggressor_side,
            timestamp=datetime.now(),
        )

        self.trade_feed.add_trade(trade)
        self.next_trade_id += 1

    def get_trade_feed(self):
        return self.trade_feed