from flask import Blueprint, jsonify
from sqlalchemy import func, case
from ..models import BlogEntry, BlogEntryRating, Rating, db

bp = Blueprint('blog-entries', __name__, url_prefix='/blog-entries')

@bp.route('/<int:id>', methods=['GET'])
def blog_entry_by_id(id: int):
    """Blog Entry for an ID"""
    blogEntry = (
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
        .filter(BlogEntry.id == id)
        .group_by(BlogEntry.id, BlogEntry.entry, BlogEntry.published)
    ).first()
    return jsonify({
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