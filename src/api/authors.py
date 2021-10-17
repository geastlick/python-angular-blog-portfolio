from flask import Blueprint, jsonify, abort, request
from ..models import Blog, db, User, BlogRating, Rating
from sqlalchemy import func

bp = Blueprint('authors', __name__, url_prefix='/authors')


@bp.route('/popular', methods=['GET'])
def popular_authors():
    """Only includes published users"""
    authors = (
        db.session.query(User.id.label('id'),
                         User.name.label('name'),
                         User.avatar.label('avatar'),
                         func.avg(Rating.stars).label('stars_avg'),
                         func.sum(Rating.stars-3).label('stars_sum')
                         )
        .select_from(User)
        .join(Blog, Blog.author == User.id)
        .join(BlogRating)
        .join(Rating)
        .where(Blog.published != None)
        .group_by(User.id, User.name, User.avatar)
        .order_by('stars_sum', User.name)
    )
    if request.args.get('page_size') is not None:
        page_size = int(request.args.get('page_size'))
        authors = authors.limit(page_size)
        if request.args.get('page') is not None:
            page = int(request.args.get('page'))
            authors = authors.offset(page_size * (page - 1))

    authors_cte = authors.cte(name="published_authors", recursive=False)
    blogs = (
        db.session.query(authors_cte.c.id.label('id'),
                         Blog.id.label('blog_id'),
                         Blog.title.label('title'),
                         func.avg(Rating.stars).label("blog_stars_avg"))
        .select_from(authors_cte)
        .join(Blog)
        .join(BlogRating)
        .join(Rating)
        .where(Blog.published != None)
        .group_by(authors_cte.c.id, authors_cte.c.stars_sum, authors_cte.c.name, Blog.id, Blog.title)
        .order_by(authors_cte.c.stars_sum, authors_cte.c.name, Blog.title)
    )
    blogs_all = blogs.all()
    result = []
    current_blog = 0
    for author in authors.all():
        author_blogs = []
        while current_blog < len(blogs_all) and blogs_all[current_blog].id == author.id:
            author_blogs.append({"id": blogs_all[current_blog].blog_id,
                                 "title": blogs_all[current_blog].title,
                                 "blog_stars_avg": blogs_all[current_blog].blog_stars_avg
                                 })
            current_blog += 1
        result.append({
            "id": author.id,
            "name": author.name,
            "avatar": author.avatar,
            "stars_avg": author.stars_avg,
            "blogs": author_blogs
        })
    return jsonify(result)
