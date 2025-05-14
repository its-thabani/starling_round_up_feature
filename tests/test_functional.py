import pytest
from app.api_client import StarlingApiClient
from app.roundup_service import RoundUpService

@pytest.fixture
def client():
    return StarlingApiClient("https://api.mockstarling.com", "mock-token")

def test_end_to_end_roundup(client, mocker):
    # Mock API responses
    mock_accounts_response = {"accounts": [{"accountUid": "12345", "defaultCategory": "67890"}]}
    mock_transactions_response = {
        "feedItems": [
            {"amount": {"minorUnits": 435}},
            {"amount": {"minorUnits": 520}},
            {"amount": {"minorUnits": 87}},
        ]
    }
    mock_savings_goal_response = {"savingsGoalUid": "goal123"}
    mock_add_to_savings_response = {"success": True}

    # Mock API client methods
    mocker.patch.object(client, '_request', side_effect=[
        mock_accounts_response,  # get_accounts
        mock_transactions_response,  # get_transactions
        mock_savings_goal_response,  # create_savings_goal
        mock_add_to_savings_response  # add_to_savings_goal
    ])

    # Step 1: Get accounts
    accounts = client.get_accounts()
    account_id = accounts["accounts"][0]["accountUid"]
    category_uid = accounts["accounts"][0]["defaultCategory"]

    # Step 2: Get transactions
    transactions = client.get_transactions(account_id, category_uid)

    # Step 3: Calculate roundup
    roundup_amount = RoundUpService.calculate_round_up(transactions["feedItems"])

    # Step 4: Create savings goal
    savings_goal = client.create_savings_goal(account_id)
    savings_goal_id = savings_goal["savingsGoalUid"]

    # Step 5: Add roundup amount to savings goal
    result = client.add_to_savings_goal(account_id, savings_goal_id, roundup_amount)

    # Assertions
    assert accounts == mock_accounts_response
    assert transactions == mock_transactions_response
    assert roundup_amount == 158  # Expected roundup amount
    assert savings_goal == mock_savings_goal_response
    assert result == mock_add_to_savings_response