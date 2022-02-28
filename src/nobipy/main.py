import typing as t

import requests
from simplejson import JSONDecodeError

from .exceptions import *
from .const import *


__all__ = [
    'Nobitex',
    'get_token',
]


def get_token(username: str, password: str) -> t.Dict:
    """
    Get a token from the Nobitex API.

    :param username: Nobitex account username
    :type username: str

    :param password: Nobitex account password
    :type password: str

    :raises: NobitexAPIException

    :return: Token
    :rtype: dict
    """

    __locals = locals()

    json_data = {
        'username': 'name@example.com',
        'password': 'secret-password-1234',
        'captcha': 'api',
    }

    try:
        r = requests.post('https://api.nobitex.ir/auth/login/', json=json_data, timeout=5)
    except Exception as e:
        raise RequestsExceptions('get_token', e, __locals)

    status_code = r.status_code

    if 200 <= status_code < 300:
        try:
            resp = r.json()
        except JSONDecodeError as e:
            raise JsonDecodingExceptions('get_token', r.text, __locals)

        return resp.get('result').get('token')

    else:
        raise StatusCodeExceptions('get_token', status_code, r.text, __locals)


class Nobitex:
    def __init__(self, token: str = None, timeout: int = 5) -> None:
        """
        Initialize a Nobitex API object.

        :param token: Token (Can be obtained from get_token()) (optional)
        :type token: str

        :param timeout: Timeout (optional)
        :type timeout: int

        :raises: TokenExceptions

        :return: None
        """

        self.__base_url = 'https://api.nobitex.ir'
        self.__token = token
        self.__timeout = timeout
        self.__headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

    def set_token(self, token: str) -> str:
        """
        Set token

        :param token: Token
        :type token: str

        :return: Token
        :rtype: str
        """

        self.__token = token
        return self.__token

    def _get(
            self, url: str, headers: t.Dict = None,
            params: t.Dict = None, data: t.Dict = None, json_data: t.Dict = None,
    ) -> requests.Response:
        """
        Get data from the Nobitex API.

        :param url: URL
        :type url: str

        :param headers: Headers (optional)
        :type headers: dict

        :param params: Parameters (optional)
        :type params: dict

        :param data: Data (optional)
        :type data: dict

        :param json_data: JSON data (optional)
        :type json_data: dict

        :raises: NobitexAPIException

        :return: Response
        :rtype: requests.Response
        """

        response = requests.get(
            self.__base_url + url,
            headers=headers,
            params=params,
            json=json_data,
            data=data,
            timeout=self.__timeout
        )

        return response

    def _post(
            self, url: str, headers: t.Dict = None,
            params: t.Dict = None, data: t.Dict = None, json_data: t.Dict = None,
    ) -> requests.Response:
        """
        Post data to the Nobitex API.

        :param url: URL
        :type url: str

        :param headers: Headers (optional)
        :type headers: dict

        :param params: Parameters (optional)
        :type params: dict

        :param data: Data (optional)
        :type data: dict

        :param json_data: JSON data (optional)
        :type json_data: dict

        :raises: NobitexAPIException

        :return: Response
        :rtype: requests.Response
        """

        response = requests.post(
            self.__base_url + url,
            headers=headers,
            params=params,
            json=json_data,
            data=data,
            timeout=self.__timeout
        )

        return response

    def _request(
            self, method: str, url: str, auth: bool = False,
            params: t.Dict = None, data: t.Dict = None, json_data: t.Dict = None,
            func_name: str = '_request',
    ) -> requests.Response:
        """
        Make a request to the Nobitex API.

        :param method: HTTP method
        :type method: str

        :param url: URL
        :type url: str

        :param auth: Whether to use authentication (optional)
        :type auth: bool

        :param params: Query parameters (optional)
        :type params: dict

        :param data: Request body (optional)
        :type data: dict

        :param json_data: Request body (optional)
        :type json_data: dict

        :param func_name: Function name (optional)
        :type func_name: str

        :return: Response
        :rtype: requests.Response
        """

        __locals = locals()

        if auth is True:
            if self.__token is None:
                raise InvalidTokenExceptions(func_name, 'No token | Try setting via "set_token" method', __locals)
            headers = self.__headers
            headers['Authorization'] = 'Token ' + self.__token
        else:
            headers = self.__headers

        if method.upper() == 'GET':
            return self._get(url, headers, params, data, json_data)
        elif method.upper() == 'POST':
            return self._post(url, headers, params, data, json_data)
        else:
            raise NobitexExceptions(func_name, 'Invalid method', __locals)

    @staticmethod
    def _raise_for_exception(
            response: requests.Response,
            func_name: str = '_raise_for_exception',
            additional: t.Dict = None
    ) -> None:
        """
        Raise exception if response status code is not 200.

        :param response: Response
        :type response: requests.Response

        :param func_name: Function name (optional)
        :type func_name: str

        :raises: NobitexAPIException

        :return: None
        :rtype: None
        """

        additional.update(locals())

        if 200 <= response.status_code < 300:
            try:
                r_json: t.Dict = response.json()
            except Exception as e:
                raise JsonDecodingExceptions(func_name, e, additional)

            if "status" in r_json.keys():
                pass
            else:
                raise InvalidResponseExceptions(func_name, '"status" key not found', additional)

            if r_json['status'].lower() == 'ok':
                pass
            else:
                raise InvalidResponseExceptions(func_name, f'response status is not ok | {r_json}', additional)

        else:
            raise StatusCodeExceptions(
                func_name, response.status_code, f'invalid status code | {response.url}', additional
            )

    def _process_response(
            self,
            response: requests.Response,
            func_name: str = '_process_response',
            additional: t.Dict = None,
    ) -> t.Dict:
        """
        Process the response from the Nobitex API.

        :param response: Response
        :type response: requests.Response

        :param func_name: Function name (optional)
        :type func_name: str

        :param additional: Arguments (optional)
        :type additional: dict

        :raises: NobitexAPIException

        :return: Response
        :rtype: dict
        """

        self._raise_for_exception(response, func_name, additional)
        return response.json()

    def orderbook(self, symbol: str) -> t.Dict[str, t.List]:
        """
        Get orderbook

        :param symbol: Symbol
        :type symbol: str

        :return: Orderbook
        :rtype: dict
        """

        __locals = locals()
        url = f'/v2/orderbook/{symbol.upper()}'

        response = self._request(
            'GET', url, auth=False, params=None, data=None, json_data=None, func_name='orderbook'
        )

        return self._process_response(response, func_name='orderbook', additional=__locals)

    def trades(self, symbol: str) -> t.Dict:
        """
        Get orderbook

        :param symbol: Symbol
        :type symbol: str

        :return: Orderbook
        :rtype: dict
        """

        __locals = locals()
        url = f'/v2/trades/{symbol.upper()}'

        response = self._request(
            'GET', url, auth=False, params=None, data=None, json_data=None, func_name='trades'
        )

        return self._process_response(response, func_name='trades', additional=__locals)

    def market_stats(self, src_currency: str, dst_currency: Union[str, DstCurrency]) -> t.Dict:
        """
        Get market stats

        :param src_currency: Source currency
        :type src_currency: str

        :param dst_currency: Destination currency
        :type dst_currency: str | DstCurrency

        :return: Market stats
        :rtype: dict
        """

        __locals = locals()
        url = f'/market/stats'

        json_data = {
            'srcCurrency': src_currency.lower(),
            'dstCurrency': dst_currency.lower(),
        }

        response = self._request(
            'GET', url, auth=False, params=None, data=None, json_data=json_data, func_name='stats'
        )

        return self._process_response(response, func_name='stats', additional=__locals)

    def ohlc(self, symbol: str, resolution: Union[str, int, Resolution], from_date: int, to_data: int) -> t.Dict:
        """
        Get market OHLC data

        :param symbol: Symbol
        :type symbol: str

        :param resolution: Resolution
        :type resolution: str | int | Resolution

        :param from_date: From date
        :type from_date: int

        :param to_data: To date
        :type to_data: int

        :return: OHLC data
        :rtype: dict
        """

        __locals = locals()
        url = f'/market/udf/history'

        params = (
            ('symbol', symbol.upper()),
            ('resolution', resolution),
            ('from', from_date),
            ('to', to_data),
        )

        response = self._request(
            'GET', url, auth=False, params=None, data=None, json_data=None, func_name='stats'
        )

        return self._process_response(response, func_name='stats', additional=__locals)

    def global_stats(self) -> t.Dict:
        """
        Get global stats

        :return: Global stats
        :rtype: dict
        """

        __locals = locals()
        url = f'/market/global-stats'

        response = self._request(
            'GET', url, auth=False, params=None, data=None, json_data=None, func_name='global_stats'
        )

        return self._process_response(response, func_name='global_stats', additional=__locals)

    def create_order(
            self, side: Union[str, Side], execution: Union[str, ExecutionType],
            src_currency: str, dst_currency: Union[str, DstCurrency],
            amount: str, price: t.Union[int, float], stop_price: t.Union[int, float] = None,
    ) -> t.Dict:
        """
        Place new order

        :param side: Side ('buy', 'sell')
        :type side: str | Side

        :param execution: Execution type ('market', 'limit', 'stop_limit', 'stop_market')
        :type execution: str | ExecutionType

        :param src_currency: Source currency
        :type src_currency: str

        :param dst_currency: Destination currency
        :type dst_currency: str | DstCurrency

        :param amount: Amount
        :type amount: str

        :param price: Price
        :type price: int or float

        :param stop_price: Stop price
        :type stop_price: int or float

        :return: Order
        :rtype: dict
        """

        __locals = locals()
        url = f'/market/orders/add'

        json_data = {
            'type': side,
            'execution': execution.lower(),
            'srcCurrency': src_currency.lower(),
            'dstCurrency': dst_currency.lower(),
            'amount': amount,
            'price': price,
        }

        if execution.lower() in ('stop_limit', 'stop_market'):
            if stop_price is None:
                raise InvalidInputExceptions(
                    'create_order',
                    'stop_price is required for stop_limit and stop_market orders'
                )
            else:
                json_data['stopPrice'] = stop_price

        response = self._request(
            'POST', url, auth=True, params=None, data=None, json_data=json_data, func_name='create_order'
        )

        return self._process_response(response, func_name='create_order', additional=__locals)

    def order_status(self, order_id: int) -> t.Dict:
        """
        Get order status

        :param order_id: Order ID
        :type order_id: int

        :return: Order status
        :rtype: dict
        """

        __locals = locals()
        url = f'/market/orders/status'

        json_data = {
            'id': order_id,
        }

        response = self._request(
            'POST', url, auth=True, params=None, data=None, json_data=json_data, func_name='order_status'
        )

        return self._process_response(response, func_name='order_status', additional=__locals)

    def open_orders(
            self, status: Union[OpenOrderStatus, str] = OpenOrderStatus.Open,
            src_currency: str = None, dst_currency: Union[DstCurrency, str] = None, details: int = 1
    ) -> t.Dict:
        """
        Get user open orders

        :param status: Status
        :type status: str or OpenOrderStatus

        :param src_currency: Source currency
        :type src_currency: str

        :param dst_currency: Destination currency
        :type dst_currency: str or DstCurrency

        :param details: Details
        :type details: int

        :return: Open orders
        :rtype: dict
        """

        __locals = locals()
        url = f'/market/orders/list'

        json_data = {}

        if status:
            json_data['status'] = status
        if src_currency:
            json_data['srcCurrency'] = src_currency.lower()
        if dst_currency:
            json_data['dstCurrency'] = dst_currency.lower()
        if details:
            json_data['details'] = details

        response = self._request(
            'POST', url, auth=True, params=None, data=None, json_data=json_data, func_name='open_orders'
        )

        return self._process_response(response, func_name='open_orders', additional=__locals)

    def update_status(self, order_id: int, status: t.Union[str, UpdateOrderStatus]) -> t.Dict:
        """
        Update order status

        :param order_id: Order ID
        :type order_id: int

        :param status: Order status
        :type status: str | UpdateOrderStatus

        :return: Order status
        :rtype: dict
        """

        __locals = locals()
        url = f'/market/orders/update-status'

        json_data = {
            'id': order_id,
            'status': status,
        }

        response = self._request(
            'POST', url, auth=True, params=None, data=None, json_data=json_data, func_name='order_status'
        )

        return self._process_response(response, func_name='order_status', additional=__locals)

    def cancel_all_orders(
            self, src_currency: str, dst_currency: t.Union[str, DstCurrency],
            execution: t.Union[str, ExecutionType] = ExecutionType.Market, hours: float = None
    ) -> t.Dict:
        """
        Cancel all orders

        :param src_currency: Source currency
        :type src_currency: str

        :param dst_currency: Destination currency
        :type dst_currency: str or DstCurrency

        :param execution: Execution type
        :type execution: str or ExecutionType

        :param hours: Hours
        :type hours: float

        :return: Cancel all orders
        :rtype: dict
        """

        __locals = locals()
        url = f'/market/orders/cancel-all'

        json_data = {
            'srcCurrency': src_currency.lower(),
            'dstCurrency': dst_currency.lower(),
        }

        if execution:
            json_data['execution'] = execution.lower()
        if hours:
            json_data['hours'] = hours

        response = self._request(
            'POST', url, auth=True, params=None, data=None, json_data=json_data, func_name='cancel_all_orders'
        )

        return self._process_response(response, func_name='cancel_all_orders', additional=__locals)

    def user_profile(self) -> t.Dict:
        """
        Get user info

        :return: Get user info
        :rtype: dict
        """

        __locals = locals()
        url = f'/users/profile'

        response = self._request(
            'POST', url, auth=True, params=None, data=None, json_data=None, func_name='user_profile'
        )

        return self._process_response(response, func_name='user_profile', additional=__locals)

    def generate_wallet_address(self, currency: str) -> t.Dict:
        """
        Generate wallet address

        :param currency: Currency
        :type currency: str

        :return: Generate wallet address
        :rtype: dict
        """

        __locals = locals()
        url = f'/users/wallets/generate-address'

        json_data = {
            'currency': currency.lower(),
        }

        response = self._request(
            'POST', url, auth=True, params=None, data=None, json_data=json_data, func_name='generate_wallet_address'
        )

        return self._process_response(response, func_name='generate_wallet_address', additional=__locals)

    def add_bank_card(self, card_number: str, bank_name: str) -> t.Dict:
        """
        Add bank card

        :param card_number: Card number
        :type card_number: str

        :param bank_name: Bank name
        :type bank_name: str

        :return: Add bank card
        :rtype: dict
        """

        __locals = locals()
        url = f'/users/cards-add'

        json_data = {
            'number': card_number.lower(),
            'bank': bank_name.lower(),
        }

        response = self._request(
            'POST', url, auth=True, params=None, data=None, json_data=json_data, func_name='add_bank_card'
        )

        return self._process_response(response, func_name='add_bank_card', additional=__locals)

    def add_bank_account(self, card_number: str, shaba: str, bank_name: str) -> t.Dict:
        """
        Add bank card

        :param card_number: Card number
        :type card_number: str

        :param shaba: Shaba
        :type shaba: str

        :param bank_name: Bank name
        :type bank_name: str

        :return: Add bank card
        :rtype: dict
        """

        __locals = locals()
        url = f'/users/cards-add'

        json_data = {
            'number': card_number.lower(),
            'shaba': shaba.lower(),
            'bank': bank_name.lower(),
        }

        response = self._request(
            'POST', url, auth=True, params=None, data=None, json_data=json_data, func_name='add_bank_account'
        )

        return self._process_response(response, func_name='add_bank_account', additional=__locals)

    def user_limitations(self) -> t.Dict:
        """
        Get user limitations

        :return: User limitations
        :rtype: dict
        """

        __locals = locals()
        url = f'/users/limitations'

        response = self._request(
            'POST', url, auth=True, params=None, data=None, json_data=None, func_name='user_limitations'
        )

        return self._process_response(response, func_name='user_limitations', additional=__locals)

    def user_wallets(self, currencies: t.List = None) -> t.Dict:
        """
        Get user wallets

        :param currencies: Currencies
        :type currencies: list

        :return: User wallets
        :rtype: dict
        """

        __locals = locals()

        if currencies is None:
            url = f'/users/wallets/list'
            json_data = None
        else:
            url = f'/v2/wallets'
            json_data = {'currencies': ",".join(currencies)}

        response = self._request(
            'POST', url, auth=True, params=None, data=None, json_data=json_data, func_name='user_wallets'
        )

        return self._process_response(response, func_name='user_wallets', additional=__locals)

    def balance(self, currency: str) -> t.Dict:
        """
        Get user wallets

        :param currency: Currency
        :type currency: str

        :return: User balance
        :rtype: dict
        """

        __locals = locals()

        url = f'/users/wallets/balance'

        json_data = {
            'currency': currency.lower(),
        }

        response = self._request(
            'POST', url, auth=True, params=None, data=None, json_data=json_data, func_name='balance'
        )

        return self._process_response(response, func_name='balance', additional=__locals)

    def transactions_list(self, wallet_id: int) -> t.Dict:
        """
        Get user wallets

        :param wallet_id: Wallet id
        :type wallet_id: int

        :return: User transactions
        :rtype: dict
        """

        __locals = locals()

        url = f'/users/wallets/transactions/list'

        json_data = {
            'wallet': str(wallet_id),
        }

        response = self._request(
            'POST', url, auth=True, params=None, data=None, json_data=json_data, func_name='transactions_list'
        )

        return self._process_response(response, func_name='transactions_list', additional=__locals)

    def deposits_list(self, wallet_id: int = 'all') -> t.Dict:
        """
        Get user wallets

        :param wallet_id: Wallet id
        :type wallet_id: int

        :return: User transactions
        :rtype: dict
        """

        __locals = locals()

        url = f'/users/wallets/deposits/list'

        json_data = {
            'wallet': str(wallet_id),
        }

        response = self._request(
            'POST', url, auth=True, params=None, data=None, json_data=json_data, func_name='deposits_list'
        )

        return self._process_response(response, func_name='deposits_list', additional=__locals)

    def __str__(self):
        return f'{self.__class__.__name__} | (token={self.__token})'

    def __repr__(self):
        return self.__str__()
