from flask import Blueprint, render_template, current_app, jsonify
from .api_client import StarlingApiClient
from .roundup_service import RoundUpService

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/roundup', methods=['POST'])
def roundup():
    try:
        client = StarlingApiClient(
            current_app.config['STARLING_API_BASE_URL'],
            current_app.config['STARLING_AUTH_TOKEN']
        )
        accounts = client.get_accounts()

        # Use first account and category for simplicity. Future improvement: allow user to select account and category.
        account_id = accounts['accounts'][0]['accountUid']
        category_uid = accounts['accounts'][0]['defaultCategory']

        # Fetch transactions for the account and category (default is for the last week)
        transactions = client.get_transactions(account_id, category_uid)

        amount = RoundUpService.calculate_round_up(transactions['feedItems'])
        savings_goal = client.create_savings_goal(account_id)
        goal_id = savings_goal['savingsGoalUid']

        result = client.add_to_savings_goal(account_id, goal_id, amount)
        return jsonify({"success": True, "saved_minor": amount, "details": result})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500