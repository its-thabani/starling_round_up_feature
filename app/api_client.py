import uuid

import requests
import logging
import time
from datetime import datetime, timedelta

class StarlingApiClient:
    def __init__(self, base_url: str, auth_token: str):
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Bearer {auth_token}',
            'Content-Type': 'application/json'
        }

    def _request(self, method: str, endpoint: str, retries: int = 3, timeout: int = 5, **kwargs) -> dict:
        # Construct the full URL for the API request
        url = f"{self.base_url}{endpoint}"

        # Retry the request up to the specified number of retries
        for attempt in range(retries):
            try:
                response = requests.request(method, url, headers=self.headers, timeout=timeout, **kwargs)

                # Handle rate-limiting by retrying with exponential backoff if status code is 429 (too many requests)
                # depended on rate limiting policy of the API
                if response.status_code == 429:
                    time.sleep(2 ** attempt)  # Wait longer with each retry
                    continue

                # Raise an exception for HTTP errors (e.g., 4xx or 5xx responses)
                response.raise_for_status()

                # Return the JSON response if the request is successful
                return response.json()
            except requests.exceptions.RequestException as e:
                # Log the error for debugging purposes
                logging.error(f"API request error: {e}")

                # Raise the exception if this is the last retry attempt
                if attempt == retries - 1:
                    raise

    def get_accounts(self):
        return self._request('GET', '/accounts')

    def get_transactions(self, account_id: str , category_uid: str, min_timestamp: str = None, max_timestamp: str = None):
        # If no timestamps are provided, default to the last week
        if max_timestamp is None or min_timestamp is None:
            max_timestamp = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
            min_timestamp = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%S.000Z")

        return self._request(
            'GET',
            f'/feed/account/{account_id}/category/{category_uid}/transactions-between?minTransactionTimestamp={min_timestamp}&maxTransactionTimestamp={max_timestamp}')

    def create_savings_goal(self, account_id: str, name: str ="My Round Up Goal") -> dict:
        data = {
            "name": name,
            "currency": "GBP",
            "target": {"currency": "GBP", "minorUnits": 1000000}
        }
        return self._request('PUT', f'/account/{account_id}/savings-goals', json=data)

    def add_to_savings_goal(self, account_id: str, savings_goal_id: str, amount_minor: int) -> dict:
        transfer_uid = str(uuid.uuid4())
        data = {
            "amount": {"currency": "GBP", "minorUnits": amount_minor}
        }
        return self._request('PUT', f'/account/{account_id}/savings-goals/{savings_goal_id}/add-money/{transfer_uid}', json=data)
