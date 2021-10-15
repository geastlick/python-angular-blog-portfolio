from sqlalchemy import func
from flask import Blueprint, jsonify, abort, request
from ..models import db, Blog, BlogRating, Rating, BlogCategory

bp = Blueprint('blogs', __name__, url_prefix='/blogs')

@bp.route('/popular', methods=['GET'])
def popular_authors():
    """Blogs ordered by popularity"""
    q = (
        db.session.query(Blog.id, Blog.title, Blog.description, BlogCategory.name,
                   func.sum(Rating.stars-3).label('sum_stars'))
        .select_from(Blog)
        .join(BlogRating)
        .join(Rating)
        .join(BlogCategory)
        .filter(Blog.published is not None)
        .group_by(Blog.id, Blog.title, Blog.description, BlogCategory.name)
        .order_by('sum_stars')
    ).all()
    result = []
    for blog in q:
        result.append({
            "id": blog.id,
            "name": blog.title,
            "description": blog.description,
            "category": blog.name
        })
    return jsonify(result)
