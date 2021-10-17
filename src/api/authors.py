from flask import Blueprint, jsonify, abort, request
from ..models import Blog, db, User, BlogRating, Rating
from sqlalchemy import func

bp = Blueprint('authors', __name__, url_prefix='/authors')


@bp.route('/popular', methods=['GET'])
def popular_authors():
    """Only includes published users"""
    q = (
        db.session.query(User.id, User.name, User.avatar,
                         func.avg(Rating.stars).label('avg_stars'),
                         func.sum(Rating.stars-3).label('sum_stars')
                        )
        .select_from(User)
        .join(Blog)
        .join(BlogRating)
        .join(Rating)
        .filter(Blog.published is not None)
        .group_by(User.id, User.name, User.avatar)
        .order_by('sum_stars')
    )
    if request.args.get('page_size') is not None:
        page_size = int(request.args.get('page_size'))
        q = q.limit(page_size)
        if request.args.get('page') is not None:
            page = int(request.args.get('page'))
            q = q.offset(page_size * (page - 1))
    result = []
    for author in q.all():
        result.append({
            "id": author.id,
            "name": author.name,
            "avatar": author.avatar,
            "stars_avg": author.avg_stars
        })
    return jsonify(result)

