__all__ = [
    'Resolution',
    'OpenOrderStatus',
    'UpdateOrderStatus',
    'Side',
    'Details',
    'DstCurrency',
    'ExecutionType',
    'Orderbook',
]


class Resolution:
    """
    Resolution of the order
    """

    DAY = 'D'
    HOUR = 60


class OpenOrderStatus:
    All = 'all'
    Open = 'open'
    Done = 'done'
    Close = 'close'


class UpdateOrderStatus:
    New = 'new'
    Active = 'active'
    Inactive = 'inactive'
    Cancel = 'cancel'


class Side:
    Buy = 'buy'
    Sell = 'sell'


class Details:
    Basic = 1
    Advanced = 2


class DstCurrency:
    Rial = 'rls'
    Usdt = Tether = 'usdt'


class ExecutionType:
    Market = 'market'
    Limit = 'limit'
    StopMarket = 'stop_market'
    StopLimit = 'stop_limit'


class Orderbook:
    PriceIndex = 0
    QuantityIndex = 1

    Buyers = 'asks'
    Sellers = 'bids'
