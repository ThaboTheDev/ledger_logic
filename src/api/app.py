from flask import Blueprint, jsonify

main_bp = Blueprint('app', __name__)

@main_bp.route("/health")
def health_check():
    return jsonify({
        "Service": "Ledger Logic",
        "Health": "Healthy"
    }), 200