from flask import Blueprint, jsonify, abort, request, session
from ..models import Comment, CommentRating, Rating, Blog
from sqlalchemy import func, and_

bp = Blueprint('comments', __name__, url_prefix='/comments')
