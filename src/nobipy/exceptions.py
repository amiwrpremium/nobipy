from typing import Union


class NobitexExceptions(Exception):
    def __init__(self, func_name: str, message: Union[str, Exception], args: dict = None):
        self.func_name = func_name
        self.message = str(message)
        self._args = args
        super().__init__(self.message)

    def __str__(self):
        return f'"{self.func_name}" -> {self.message} | {str(self._args)}'


class RequestsExceptions(NobitexExceptions):
    def __init__(self, func_name: str, message: Union[str, Exception], args: dict = None):
        self.func_name = func_name
        self.message = message
        self._args = args
        super().__init__(func_name, message, args)

    def __str__(self):
        return f'{self.func_name} -> {self.message} | {str(self._args)}'


class StatusCodeExceptions(NobitexExceptions):
    def __init__(self, func_name: str, status_code: int, message: Union[str, Exception], args: dict = None):
        self.func_name = func_name
        self.status_code = status_code
        self.message = message
        self._args = args
        super().__init__(func_name, message, args)

    def __str__(self):
        return f'{self.func_name} | {self.status_code} -> {self.message} | {str(self._args)}'


class JsonDecodingExceptions(NobitexExceptions):
    def __init__(self, func_name: str, message: Union[str, Exception], args: dict = None):
        self.func_name = func_name
        self.message = message
        self._args = args
        super().__init__(func_name, message, args)

    def __str__(self):
        return f'{self.func_name} -> {self.message} | {str(self._args)}'


class InvalidResponseExceptions(NobitexExceptions):
    def __init__(self, func_name: str, message: Union[str, Exception], args: dict = None):
        self.func_name = func_name
        self.message = message
        self._args = args
        super().__init__(func_name, message, args)

    def __str__(self):
        return f'{self.func_name} -> {self.message} | {str(self._args)}'


class InvalidTokenExceptions(NobitexExceptions):
    def __init__(self, func_name: str, message: Union[str, Exception], args: dict = None):
        self.func_name = func_name
        self.message = message
        self._args = args
        super().__init__(func_name, message, args)

    def __str__(self):
        return f'{self.func_name} -> {self.message} | {str(self._args)}'


class InvalidInputExceptions(NobitexExceptions):
    def __init__(self, func_name: str, message: Union[str, Exception], args: dict = None):
        self.func_name = func_name
        self.message = message
        self._args = args
        super().__init__(func_name, message, args)

    def __str__(self):
        return f'{self.func_name} -> {self.message} | {str(self._args)}'


class CreateOrderException(NobitexExceptions):
    def __init__(self, func_name: str, message: Union[str, Exception], args: dict = None):
        self.func_name = func_name
        self.message = message
        self._args = args
        super().__init__(func_name, message, args)


class InvalidOrderPrice(CreateOrderException):
    def __init__(self, message: Union[str, Exception], args: dict = None):
        self.message = message
        self._args = args
        super().__init__('create_order', message, args)


class BadPrice(CreateOrderException):
    def __init__(self, message: Union[str, Exception], args: dict = None):
        self.message = message
        self._args = args
        super().__init__('create_order', message, args)


class InvalidExecutionType(CreateOrderException):
    def __init__(self, message: Union[str, Exception], args: dict = None):
        self.message = message
        self._args = args
        super().__init__('create_order', message, args)


class InvalidOrderType(CreateOrderException):
    def __init__(self, message: Union[str, Exception], args: dict = None):
        self.message = message
        self._args = args
        super().__init__('create_order', message, args)


class OverValueOrder(CreateOrderException):
    def __init__(self, message: Union[str, Exception], args: dict = None):
        self.message = message
        self._args = args
        super().__init__('create_order', message, args)


class SmallOrder(CreateOrderException):
    def __init__(self, message: Union[str, Exception], args: dict = None):
        self.message = message
        self._args = args
        super().__init__('create_order', message, args)


class DuplicateOrder(CreateOrderException):
    def __init__(self, message: Union[str, Exception], args: dict = None):
        self.message = message
        self._args = args
        super().__init__('create_order', message, args)


class InvalidMarketPair(CreateOrderException):
    def __init__(self, message: Union[str, Exception], args: dict = None):
        self.message = message
        self._args = args
        super().__init__('create_order', message, args)


class MarketClosed(CreateOrderException):
    def __init__(self, message: Union[str, Exception], args: dict = None):
        self.message = message
        self._args = args
        super().__init__('create_order', message, args)


class TradingUnavailable(CreateOrderException):
    def __init__(self, message: Union[str, Exception], args: dict = None):
        self.message = message
        self._args = args
        super().__init__('create_order', message, args)


class FeatureUnavailable(CreateOrderException):
    def __init__(self, message: Union[str, Exception], args: dict = None):
        self.message = message
        self._args = args
        super().__init__('create_order', message, args)
