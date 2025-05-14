import pytest
from app.api_client import StarlingApiClient

@pytest.fixture
def client():
    return StarlingApiClient("https://api.mockstarling.com", "mock-token")

def test_client_headers(client):
    assert 'Authorization' in client.headers
    assert client.headers['Authorization'].startswith('Bearer')

def test_get_accounts(client, mocker):
    mock_response = {"accounts": [{"accountUid": "12345", "defaultCategory": "67890"}]}
    mocker.patch.object(client, '_request', return_value=mock_response)
    accounts = client.get_accounts()
    assert accounts == mock_response
    client._request.assert_called_once_with('GET', '/accounts')

def test_get_transactions(client, mocker):
    account_id = "12345"
    category_uid = "67890"
    mock_response = {"feedItems": [{"amount": {"minorUnits": 100}}, {"amount": {"minorUnits": 200}}]}
    mocker.patch.object(client, '_request', return_value=mock_response)
    transactions = client.get_transactions(account_id, category_uid, min_timestamp="2025-05-07T07:59:06.000Z", max_timestamp="2025-05-14T07:59:06.000Z")
    assert transactions == mock_response
    client._request.assert_called_once_with('GET', f'/feed/account/{account_id}/category/{category_uid}/transactions-between?minTransactionTimestamp=2025-05-07T07:59:06.000Z&maxTransactionTimestamp=2025-05-14T07:59:06.000Z')

def test_create_savings_goal(client, mocker):
    account_id = "12345"
    mock_response = {"savingsGoalUid": "goal123"}
    mocker.patch.object(client, '_request', return_value=mock_response)
    savings_goal = client.create_savings_goal(account_id)
    assert savings_goal == mock_response
    client._request.assert_called_once_with('PUT', f'/account/{account_id}/savings-goals', json=mocker.ANY)

def test_add_to_savings_goal(client, mocker):
    account_id = "12345"
    goal_id = "goal123"
    amount = 100
    mock_response = {"success": True}
    mocker.patch.object(client, '_request', return_value=mock_response)
    result = client.add_to_savings_goal(account_id, goal_id, amount)
    assert result == mock_response

def test_request_error_handling(client, mocker):
    mocker.patch.object(client, '_request', side_effect=Exception("API error"))
    with pytest.raises(Exception, match="API error"):
        client.get_accounts()