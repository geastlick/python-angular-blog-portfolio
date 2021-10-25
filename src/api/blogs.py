from os import name
from sqlalchemy import func, case, text, bindparam, Integer, and_
from sqlalchemy.orm import aliased
from flask import Blueprint, jsonify, abort, request, session
from ..models import BlogEntry, User, db, Blog, BlogRating, Rating, BlogCategory, BlogEntryRating, follow_blog

bp = Blueprint('blogs', __name__, url_prefix='/blogs')


@bp.route('/popular', methods=['GET'])
def popular_blogs():
    """Blogs ordered by popularity"""
    author = aliased(User)
    blog_rating = aliased(BlogRating)
    blog_stars = aliased(Rating)
    user_rating = aliased(BlogRating)
    user_stars = aliased(Rating)
    if 'userid' in session:
        q = (
            db.session.query(Blog.id.label('id'),
                             Blog.title.label('title'),
                             Blog.description.label('description'),
                             BlogCategory.name.label('category_name'),
                             Blog.published.label('published'),
                             author.name.label('author_name'),
                             author.avatar.label('avatar'),
                             func.avg(blog_stars.stars).label('avg_stars'),
                             func.sum(blog_stars.stars-3).label('sum_stars'),
                             func.sum(case(value=blog_stars.stars, whens={
                                 1: 1}, else_=0)).label('stars_1'),
                             func.sum(case(value=blog_stars.stars, whens={
                                 2: 1}, else_=0)).label('stars_2'),
                             func.sum(case(value=blog_stars.stars, whens={
                                 3: 1}, else_=0)).label('stars_3'),
                             func.sum(case(value=blog_stars.stars, whens={
                                 4: 1}, else_=0)).label('stars_4'),
                             func.sum(case(value=blog_stars.stars, whens={
                                 5: 1}, else_=0)).label('stars_5'),
                             (follow_blog.c.blog_id != None).label('following'),
                             user_stars.stars.label('rating')
                             )
            .select_from(Blog)
            .outerjoin(blog_rating)
            .outerjoin(blog_stars)
            .join(BlogCategory)
            .join(author, author.id == Blog.author)
            .outerjoin(follow_blog, and_(follow_blog.c.blog_id == Blog.id, follow_blog.c.follower_id == session['userid']))
            .outerjoin(user_rating, and_(user_rating.blog == Blog.id, user_rating.user == follow_blog.c.follower_id))
            .outerjoin(user_stars, user_stars.id == user_rating.rating)
            .filter(Blog.published != None)
            .group_by(Blog.id, Blog.title, Blog.description, BlogCategory.name, Blog.published, author.name, author.avatar,
                (follow_blog.c.blog_id != None), user_stars.stars
            )
            .order_by('sum_stars')
        )
    else:
        q = (
            db.session.query(Blog.id.label('id'),
                             Blog.title.label('title'),
                             Blog.description.label('description'),
                             BlogCategory.name.label('category_name'),
                             Blog.published.label('published'),
                             author.name.label('author_name'),
                             author.avatar.label('avatar'),
                             func.avg(blog_stars.stars).label('avg_stars'),
                             func.sum(blog_stars.stars-3).label('sum_stars'),
                             func.sum(case(value=blog_stars.stars, whens={
                                 1: 1}, else_=0)).label('stars_1'),
                             func.sum(case(value=blog_stars.stars, whens={
                                 2: 1}, else_=0)).label('stars_2'),
                             func.sum(case(value=blog_stars.stars, whens={
                                 3: 1}, else_=0)).label('stars_3'),
                             func.sum(case(value=blog_stars.stars, whens={
                                 4: 1}, else_=0)).label('stars_4'),
                             func.sum(case(value=blog_stars.stars, whens={
                                 5: 1}, else_=0)).label('stars_5')
                             )
            .select_from(Blog)
            .outerjoin(blog_rating)
            .outerjoin(blog_stars)
            .join(BlogCategory)
            .join(author, author.id == Blog.author)
            .filter(Blog.published != None)
            .group_by(Blog.id, Blog.title, Blog.description, BlogCategory.name, Blog.published, author.name, author.avatar)
            .order_by('sum_stars')
        )
    count_blogs = q.count()
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
    return jsonify({"count_all_blogs": count_blogs, "blogs": result})


@bp.route('/followed', methods=['GET'])
def followed_blogs():
    """Blogs followed ordered by popularity"""
    if "username" not in session or "userid" not in session:
        return abort(400)
    q = (
        db.session.query(Blog.id.label('id'),
                         Blog.title.label('title'),
                         Blog.description.label('description'),
                         BlogCategory.name.label('category_name'),
                         Blog.published.label('published'),
                         User.name.label('author_name'),
                         User.avatar.label('avatar'),
                         func.avg(Rating.stars).label('avg_stars'),
                         func.sum(Rating.stars-3).label('sum_stars'),
                         func.sum(case(value=Rating.stars, whens={
                                  1: 1}, else_=0)).label('stars_1'),
                         func.sum(case(value=Rating.stars, whens={
                                  2: 1}, else_=0)).label('stars_2'),
                         func.sum(case(value=Rating.stars, whens={
                                  3: 1}, else_=0)).label('stars_3'),
                         func.sum(case(value=Rating.stars, whens={
                                  4: 1}, else_=0)).label('stars_4'),
                         func.sum(case(value=Rating.stars, whens={
                                  5: 1}, else_=0)).label('stars_5')
                         )
        .select_from(Blog)
        .join(follow_blog, and_(follow_blog.c.blog_id == Blog.id, follow_blog.c.follower_id == session["userid"]))
        .outerjoin(BlogRating)
        .outerjoin(Rating)
        .join(BlogCategory)
        .join(User, User.id == Blog.author)
        .filter(Blog.published != None)
        .group_by(Blog.id, Blog.title, Blog.description, BlogCategory.name, Blog.published, User.name, User.avatar)
        .order_by('sum_stars')
    )
    count_blogs = q.count()
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
    return jsonify({"count_all_blogs": count_blogs, "blogs": result})


@bp.route('/<int:id>', methods=['GET'])
def blog_by_id(id: int):
    """Blog for an ID"""
    blog = (
        db.session.query(Blog.id, Blog.title, Blog.description, BlogCategory.name.label('category_name'),
                         Blog.published, User.name.label(
                             'author_name'), User.avatar,
                         func.avg(Rating.stars).label('avg_stars'),
                         func.sum(Rating.stars-3).label('sum_stars'),
                         func.sum(case(value=Rating.stars, whens={
                                  1: 1}, else_=0)).label('stars_1'),
                         func.sum(case(value=Rating.stars, whens={
                                  2: 1}, else_=0)).label('stars_2'),
                         func.sum(case(value=Rating.stars, whens={
                                  3: 1}, else_=0)).label('stars_3'),
                         func.sum(case(value=Rating.stars, whens={
                                  4: 1}, else_=0)).label('stars_4'),
                         func.sum(case(value=Rating.stars, whens={
                                  5: 1}, else_=0)).label('stars_5')
                         )
        .select_from(Blog)
        .outerjoin(BlogRating)
        .outerjoin(Rating)
        .join(BlogCategory)
        .join(User, User.id == Blog.author)
        .filter(Blog.id == id)
        .group_by(Blog.id, Blog.title, Blog.description, BlogCategory.name, Blog.published, User.name, User.avatar)
    ).one()
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
        db.session.query(BlogEntry.id.label('id'),
                         BlogEntry.entry.label('entry'),
                         BlogEntry.published.label('published'),
                         func.avg(Rating.stars).label('avg_stars'),
                         func.sum(Rating.stars-3).label('sum_stars'),
                         func.sum(case(value=Rating.stars, whens={
                                  1: 1}, else_=0)).label('stars_1'),
                         func.sum(case(value=Rating.stars, whens={
                                  2: 1}, else_=0)).label('stars_2'),
                         func.sum(case(value=Rating.stars, whens={
                                  3: 1}, else_=0)).label('stars_3'),
                         func.sum(case(value=Rating.stars, whens={
                                  4: 1}, else_=0)).label('stars_4'),
                         func.sum(case(value=Rating.stars, whens={
                                  5: 1}, else_=0)).label('stars_5')
                         )
        .select_from(BlogEntry)
        .outerjoin(BlogEntryRating)
        .outerjoin(Rating)
        .filter(BlogEntry.published != None, BlogEntry.blog == id)
        .group_by(BlogEntry.id, BlogEntry.entry, BlogEntry.published)
    )
    entry_count = q.count()
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
    return jsonify({"count_all_entries": entry_count, "blog_entries": result})


@bp.route('/<int:id>/follow', methods=['POST'])
def user_follow_blog(id: int):
    b = Blog.query.get_or_404(id)
    if "username" not in session or "userid" not in session:
        return abort(400)
    try:
        insert = follow_blog.insert().values(
            {"blog_id": id, "follower_id": session["userid"]})
        db.session.execute(insert)
        db.session.commit()
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)


@bp.route('/<int:id>/unfollow', methods=['POST'])
def user_unfollow_blog(id: int):
    b = Blog.query.get_or_404(id)
    if "username" not in session or "userid" not in session:
        return abort(400)
    try:
        delete = follow_blog.delete().where(and_(follow_blog.c.blog_id == id,
                                                 follow_blog.c.follower_id == session["userid"]))
        db.session.execute(delete)
        db.session.commit()
        return jsonify(True)
    except:
        # something went wrong :(
        print(db.error)
        return jsonify(False)
