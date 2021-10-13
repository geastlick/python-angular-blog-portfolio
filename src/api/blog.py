from flask import Blueprint, jsonify, abort, request
from ..models import db

bp = Blueprint('blogs', __name__, url_prefix='/blogs')
