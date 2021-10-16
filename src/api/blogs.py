from os import name
from sqlalchemy import func
from flask import Blueprint, jsonify, abort, request
from ..models import User, db, Blog, BlogRating, Rating, BlogCategory

bp = Blueprint('blogs', __name__, url_prefix='/blogs')


@bp.route('/popular', methods=['GET'])
def popular_blogs():
    """Blogs ordered by popularity"""
    q = (
        db.session.query(Blog.id, Blog.title, Blog.description, BlogCategory.name.label('category_name'),
                         User.name.label('author_name'), User.avatar,
                         func.sum(Rating.stars-3).label('sum_stars'))
        .select_from(Blog)
        .join(BlogRating)
        .join(Rating)
        .join(BlogCategory)
        .join(User, User.id == Blog.author)
        .filter(Blog.published is not None)
        .group_by(Blog.id, Blog.title, Blog.description, BlogCategory.name, User.name, User.avatar,)
        .order_by('sum_stars')
    ).all()
    result = []
    for blog in q:
        result.append({
            "id": blog.id,
            "title": blog.title,
            "description": blog.description,
            "category": blog.category_name,
            "author": blog.author_name,
            "avatar": blog.avatar
        })
    return jsonify(result)
