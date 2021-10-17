from os import name
from sqlalchemy import func, case, text, bindparam, Integer
from flask import Blueprint, jsonify, abort, request
from ..models import BlogEntry, User, db, Blog, BlogRating, Rating, BlogCategory, BlogEntryRating

bp = Blueprint('blogs', __name__, url_prefix='/blogs')


@bp.route('/popular', methods=['GET'])
def popular_blogs():
    """Blogs ordered by popularity"""
    q = (
        db.session.query(Blog.id, Blog.title, Blog.description, BlogCategory.name.label('category_name'),
                         Blog.published, User.name.label('author_name'), User.avatar,
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
        .group_by(Blog.id, Blog.title, Blog.description, BlogCategory.name, Blog.published, User.name, User.avatar)
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
            "published": blog.published,
            "author": blog.author_name,
            "avatar": blog.avatar,
            "stars_avg": blog.avg_stars,
            "stars_1": blog.stars_1,
            "stars_2": blog.stars_2,
            "stars_3": blog.stars_3,
            "stars_4": blog.stars_4,
            "stars_5": blog.stars_5
        })
    return jsonify(result)


@bp.route('/<int:id>', methods=['GET'])
def blog_by_id(id: int):
    """Blog for an ID"""
    blog = (
        db.session.query(Blog.id, Blog.title, Blog.description, BlogCategory.name.label('category_name'),
                         Blog.published, User.name.label('author_name'), User.avatar,
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
        .filter(Blog.id == id)
        .group_by(Blog.id, Blog.title, Blog.description, BlogCategory.name, Blog.published, User.name, User.avatar)
    ).first()
    return jsonify({
            "id": blog.id,
            "title": blog.title,
            "description": blog.description,
            "category": blog.category_name,
            "published": blog.published,
            "author": blog.author_name,
            "avatar": blog.avatar,
            "stars_avg": blog.avg_stars,
            "stars_1": blog.stars_1,
            "stars_2": blog.stars_2,
            "stars_3": blog.stars_3,
            "stars_4": blog.stars_4,
            "stars_5": blog.stars_5
        })



@bp.route('/<int:id>/entries', methods=['GET'])
def blog_entries_for_blog_id(id: int):
    """Blog Entries (published) for a blog"""
    q = (
        db.session.query(BlogEntry.id, BlogEntry.entry, BlogEntry.published,
                         func.avg(Rating.stars).label('avg_stars'),
                         func.sum(Rating.stars-3).label('sum_stars'),
                         func.sum(case(value=Rating.stars, whens={1: 1}, else_=0)).label('stars_1'),
                         func.sum(case(value=Rating.stars, whens={2: 1}, else_=0)).label('stars_2'),
                         func.sum(case(value=Rating.stars, whens={3: 1}, else_=0)).label('stars_3'),
                         func.sum(case(value=Rating.stars, whens={4: 1}, else_=0)).label('stars_4'),
                         func.sum(case(value=Rating.stars, whens={5: 1}, else_=0)).label('stars_5')
                        )
        .select_from(BlogEntry)
        .join(BlogEntryRating)
        .join(Rating)
        .filter(BlogEntry.published is not None and BlogEntry.blog == id)
        .group_by(BlogEntry.id, BlogEntry.entry, BlogEntry.published)
    )
    if request.args.get('page_size') is not None:
        page_size = int(request.args.get('page_size'))
        q = q.limit(page_size)
    if request.args.get('page') is not None:
        page = int(request.args.get('page'))
        q = q.offset(page_size * (page - 1))
    result = []
    for blogEntry in q.all():
        result.append({
            "id": blogEntry.id,
            "entry": blogEntry.entry,
            "published": blogEntry.published,
            "stars_avg": blogEntry.avg_stars,
            "stars_1": blogEntry.stars_1,
            "stars_2": blogEntry.stars_2,
            "stars_3": blogEntry.stars_3,
            "stars_4": blogEntry.stars_4,
            "stars_5": blogEntry.stars_5
        })
    return jsonify(result)

