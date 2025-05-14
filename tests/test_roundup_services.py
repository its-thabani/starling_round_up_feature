from app.roundup_service import RoundUpService

def test_roundup():
    txns = [
        {'amount': {'minorUnits': 435}},
        {'amount': {'minorUnits': 520}},
        {'amount': {'minorUnits': 87}},
    ]
    result = RoundUpService.calculate_round_up(txns)
    assert result == 158

def test_roundup_empty_transactions():
    # Test with an empty list of transactions
    txns = []
    result = RoundUpService.calculate_round_up(txns)
    assert result == 0

def test_roundup_already_rounded():
    # Test with transactions that are already rounded
    txns = [
        {'amount': {'minorUnits': 500}},
        {'amount': {'minorUnits': 1000}},
        {'amount': {'minorUnits': 200}},
    ]
    result = RoundUpService.calculate_round_up(txns)
    assert result == 0

def test_roundup_single_transaction():
    # Test with a single transaction
    txns = [{'amount': {'minorUnits': 123}}]
    result = RoundUpService.calculate_round_up(txns)
    assert result == 77

def test_roundup_negative_transactions():
    # Test with negative transaction amounts
    txns = [
        {'amount': {'minorUnits': -435}},
        {'amount': {'minorUnits': -520}},
        {'amount': {'minorUnits': -87}},
    ]
    result = RoundUpService.calculate_round_up(txns)
    assert result == 0  # Assuming negative amounts are ignored

def test_roundup_mixed_transactions():
    # Test with a mix of positive and negative transaction amounts
    txns = [
        {'amount': {'minorUnits': 435}},
        {'amount': {'minorUnits': -520}},
        {'amount': {'minorUnits': 87}},
    ]
    result = RoundUpService.calculate_round_up(txns)
    assert result == 78  # Assuming negative amounts are ignored