import time

from dydx3.helpers.request_helpers import generate_now_iso
from dydx3.helpers.request_helpers import generate_query_path
from dydx3.eth_signing import generate_api_key_action
from dydx3.eth_signing import sign_off_chain_action
from dydx3.helpers.requests import request


class ApiKeys(object):
    """Module for adding, querying, and deleting API keys."""

    def __init__(
        self,
        host,
        eth_signer,
        default_address,
    ):
        self.host = host
        self.eth_signer = eth_signer
        self.default_address = default_address

    # ============ Request Helpers ============

    def _request(
        self,
        method,
        endpoint,
        opt_ethereum_address,
        data={}
    ):
        ethereum_address = opt_ethereum_address or self.default_address

        request_path = '/'.join(['/v3', endpoint])
        timestamp = generate_now_iso()
        action = generate_api_key_action(
            request_path,
            method.upper(),
            data,
        )
        signature = sign_off_chain_action(
            self.eth_signer,
            ethereum_address,
            action,
            timestamp,
        )

        return request(
            self.host + request_path,
            method,
            {
                'DYDX-SIGNATURE': signature,
                'DYDX-TIMESTAMP': timestamp,
                'DYDX-ETHEREUM-ADDRESS': ethereum_address,
            },
            data,
        )

    def _get(
        self,
        endpoint,
        opt_ethereum_address,
    ):
        return self._request(
            'get',
            endpoint,
            opt_ethereum_address,
        )

    def _post(
        self,
        endpoint,
        opt_ethereum_address,
        data={},
    ):
        return self._request(
            'post',
            endpoint,
            opt_ethereum_address,
            data,
        )

    def _delete(
        self,
        endpoint,
        opt_ethereum_address,
        params={},
    ):
        url = generate_query_path(endpoint, params)
        return self._request(
            'delete',
            url,
            opt_ethereum_address,
        )

# ============ Requests ============

    def get_api_keys(
        self,
        ethereum_address=None,
    ):
        '''
        Get API keys.

        :param ethereum_address: optional
        :type ethereum_address: str

        :returns: Object containing an array of apiKeys

        :raises: DydxAPIError
        '''
        return self._get(
            'api-keys',
            ethereum_address,
        )

    def register_api_key(
        self,
        api_public_key,
        ethereum_address=None,
    ):
        '''
        Register an API key.

        :param api_public_key: required
        :type api_public_key: str

        :param ethereum_address: optional
        :type ethereum_address: str

        :returns: Object containing an apiKey

        :raises: DydxAPIError
        '''
        return self._post(
            'api-keys',
            ethereum_address,
            {
                'apiKey': api_public_key,
            },
        )

    def delete_api_key(
        self,
        api_public_key,
        ethereum_address=None,
    ):
        '''
        Delete an API key.

        :param api_public_key: required
        :type api_public_key: str

        :param ethereum_address: optional
        :type ethereum_address: str

        :returns: None

        :raises: DydxAPIError
        '''
        self._delete(
            'api-keys',
            ethereum_address,
            {
                'apiKey': api_public_key,
            },
        )
