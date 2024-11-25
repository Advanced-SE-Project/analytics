from flask import Blueprint, jsonify

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/analytics/summary', methods=['GET'])
def get_summary():
    return jsonify({'message': 'Analytics summary data here.'})
