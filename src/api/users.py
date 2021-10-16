import hashlib
import secrets
import binascii
from flask import Blueprint, jsonify, abort, request, session
from ..models import db, User

bp = Blueprint('users', __name__, url_prefix='/users')


def scramble(password: str):
    """Hash and salt the given password"""
    salt = secrets.token_hex(16).encode('utf-8')
    rtn = binascii.hexlify(hashlib.scrypt(password.encode('utf-8'), salt=salt, n=2,
                                          r=8, p=1)).decode('utf-8') + ";" + salt.decode('utf-8')
    return rtn


@bp.route('', methods=['POST'])
def create():
    # req body must contain username, password, name, and email
    if 'username' not in request.json or len(request.json['username']) < 3:
        # username must be present and at least 3 characters
        return abort(400)
    if 'password' not in request.json or len(request.json['password']) < 8:
        # password must be present and at least 8 characters
        return abort(400)
    if 'name' not in request.json or 'email' not in request.json:
        # name and email must both be present
        return abort(400)
    t = User.query.filter(User.username == request.json['username']).first()
    if t is not None:
        # duplicate username -- not allowed
        return jsonify({"error": "Duplicate username"})
    t = User.query.filter(User.email == request.json['email']).first()
    if t is not None:
        # duplicate email -- not allowed
        return jsonify({"error": "Duplicate email"})
    # construct User
    u = User(
        username=request.json['username'],
        password=scramble(request.json['password']),
        name=request.json['name'],
        email=request.json['email']
    )
    db.session.add(u)  # prepare CREATE statement
    db.session.commit()  # execute CREATE statement
    return jsonify({"success": u.serialize()})


@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    u = User.query.get_or_404(id)
    if "username" not in session or u.username != session["username"]:
        # You must be logged in as current user to modify
        return abort(400)
    try:
        db.session.delete(u)  # prepare DELETE statement
        db.session.commit()  # execute DELETE statement
        session.pop('username', None)
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)


@bp.route('/<int:id>', methods=['PUT', 'PATCH'])
def update(id: int):
    u = User.query.get_or_404(id)
    if "username" not in session or u.username != session["username"]:
        # You must be logged in as current user to modify
        return abort(400)
    # req body may contain username, password, name, and email
    if 'username' in request.json and request.json['username'] != u.username:
        if len(request.json['username']) < 3:
            # username must be at least 3 characters
            return abort(400)
        t = User.query.filter_by(username=request.json['username']).first()
        if t is not None:
            # duplicate username -- not allowed
            return abort(400)
        u.username = request.json['username']
    if 'email' in request.json:
        u.email = request.json['email']
    if 'name' in request.json:
        u.name = request.json['name']
    if 'password' in request.json:
        if len(request.json['password']) < 8:
            # password must be at least 8 characters
            return abort(400)
        if 'old_password' not in request.json:
            # old_password must be present when changing password
            return abort(400)
        if not u.verify(request.json['old_password']):
            # password verification failed
            return abort(400)
        u.password = scramble(request.json['password'])
    try:
        db.session.commit()  # execute UPDATE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)
