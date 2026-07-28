from datetime import datetime

from sigma.matching_engine import MatchingEngine
from sigma.order import Order
from sigma.order_side import OrderSide
from sigma.order_type import OrderType


engine = MatchingEngine()

sell_order = Order(
    order_id=1,
    user_id=101,
    side=OrderSide.SELL,
    order_type=OrderType.LIMIT,
    price=100,
    quantity=5,
    timestamp=datetime.now(),
)

buy_order = Order(
    order_id=2,
    user_id=102,
    side=OrderSide.BUY,
    order_type=OrderType.MARKET,
    price=None,
    quantity=3,
    timestamp=datetime.now(),
)

engine.process_order(sell_order)
engine.process_order(buy_order)

print("TradeFeed:")
trade_feed = engine.get_trade_feed()

print(trade_feed)

for trade in trade_feed:
    print(trade)

print("\nКількість угод:")
print(len(engine.trade_feed))

print("\nУгоди через TradeFeed:")
for trade in engine.trade_feed:
    print(trade)

print("\nУгоди через стару властивість engine.trades:")
for trade in engine.trades:
    print(trade)