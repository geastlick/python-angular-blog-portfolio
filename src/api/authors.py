from flask import Blueprint, jsonify, abort, request
from ..models import Blog, db, User

bp = Blueprint('authors', __name__, url_prefix='/authors')


@bp.route('', methods=['GET'])
def all_authors():
    """Only includes published users"""
    q = (
        User.query
        .join(Blog)
        .filter(Blog.published is not None)
        .order_by(User.name)
    ).all()
    result = []
    for author in q:
        result.append({
            "id": author.id,
            "name": author.name,
            "avatar": author.avatar
        })
    return jsonify(result)

