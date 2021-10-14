from flask import Blueprint, jsonify, abort, request
from ..models import db, User

bp = Blueprint('users', __name__, url_prefix='/authors')

@bp.route('', methods=['GET'])
def all_authors():
    """Only includes published users"""
    return jsonify({})

@bp.route('/popular', methods=['GET'])
def popular_authors():
    """Authors ordered by popularity"""
    return jsonify({})
