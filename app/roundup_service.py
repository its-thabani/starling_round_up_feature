import math
from decimal import Decimal, ROUND_UP

class RoundUpService:
    @staticmethod
    def calculate_round_up(transactions: list[dict]) -> int:
        total = Decimal('0.00')
        for txn in transactions:
            amount_minor = txn.get('amount', {}).get('minorUnits', 0)

            if amount_minor <= 0:  # Skip non-positive amounts
                continue

            amount = Decimal(amount_minor) / 100

            rounded = Decimal(math.ceil(amount))

            # Calculate the round-up amount
            round_up = (rounded - amount).quantize(Decimal('0.01'), rounding=ROUND_UP)

            total += round_up

        return int(total * 100)  # return in minor units (pence)