from sigma.trade import Trade


class TradeFeed:
    def __init__(self):
        self._trades = []

    def add_trade(self, trade):
        if not isinstance(trade, Trade):
            raise TypeError(
                f"trade must be Trade, got {type(trade)}"
            )

        self._trades.append(trade)

    def get_trades(self):
        return list(self._trades)

    def __len__(self):
        return len(self._trades)

    def __iter__(self):
        return iter(self._trades)

    def __repr__(self):
        return f"TradeFeed(trades={len(self._trades)})"