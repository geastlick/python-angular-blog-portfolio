from os import name
from sqlalchemy import func, case
from flask import Blueprint, jsonify, abort, request
from ..models import User, db, Blog, BlogRating, Rating, BlogCategory

bp = Blueprint('blogs', __name__, url_prefix='/blogs')


@bp.route('/popular', methods=['GET'])
def popular_blogs():
    """Blogs ordered by popularity"""
    q = (
        db.session.query(Blog.id, Blog.title, Blog.description, BlogCategory.name.label('category_name'),
                         User.name.label('author_name'), User.avatar,
                         func.avg(Rating.stars).label('avg_stars'),
                         func.sum(Rating.stars-3).label('sum_stars'),
                         func.sum(case(value=Rating.stars, whens={1: 1}, else_=0)).label('stars_1'),
                         func.sum(case(value=Rating.stars, whens={2: 1}, else_=0)).label('stars_2'),
                         func.sum(case(value=Rating.stars, whens={3: 1}, else_=0)).label('stars_3'),
                         func.sum(case(value=Rating.stars, whens={4: 1}, else_=0)).label('stars_4'),
                         func.sum(case(value=Rating.stars, whens={5: 1}, else_=0)).label('stars_5')
                        )
        .select_from(Blog)
        .join(BlogRating)
        .join(Rating)
        .join(BlogCategory)
        .join(User, User.id == Blog.author)
        .filter(Blog.published is not None)
        .group_by(Blog.id, Blog.title, Blog.description, BlogCategory.name, User.name, User.avatar,)
        .order_by('sum_stars')
    )
    if request.args.get('page_size') is not None:
        page_size = int(request.args.get('page_size'))
        q = q.limit(page_size)
        if request.args.get('page') is not None:
            page = int(request.args.get('page'))
            q = q.offset(page_size * (page - 1))
    result = []
    for blog in q.all():
        result.append({
            "id": blog.id,
            "title": blog.title,
            "description": blog.description,
            "category": blog.category_name,
            "author": blog.author_name,
            "avatar": blog.avatar,
            "stars_avg": blog.avg_stars,
            "stars_1": blog.stars_1,
            "stars_1": blog.stars_2,
            "stars_1": blog.stars_3,
            "stars_1": blog.stars_4,
            "stars_1": blog.stars_5
        })
    return jsonify(result)
