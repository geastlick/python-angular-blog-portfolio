import hashlib
import secrets
from flask import Blueprint, jsonify, abort, request
from ..models import db, User

bp = Blueprint('users', __name__, url_prefix='/users')

def scramble(password: str):
    """Hash and salt the given password"""
    salt = secrets.token_hex(16).encode('utf-8')
    rtn = hashlib.scrypt(password.encode('utf-8'), salt=salt, n=2,
                              r=8, p=1).hex() + ";" + salt.hex()
    return rtn

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    user:User = User.query.get_or_404(id)
    return jsonify({
        "name": user.name,
        "avatar": user.avatar,
    })


@bp.route('', methods=['POST'])
def create():
    # req body must contain username and password
    if 'username' not in request.json or 'password' not in request.json:
        return abort(400)
    if len(request.json['username']) < 3 or len(request.json['password']) < 8:
        return abort(400)
    # construct User
    u = User(
        username=request.json['username'],
        password=scramble(request.json['password'])
    )
    db.session.add(u)  # prepare CREATE statement
    db.session.commit()  # execute CREATE statement
    return jsonify(u.serialize())


@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    u = User.query.get_or_404(id)
    try:
        db.session.delete(u)  # prepare DELETE statement
        db.session.commit()  # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)


@bp.route('/<int:id>', methods=['PUT', 'PATCH'])
def update(id: int):
    u = User.query.get_or_404(id)
    if 'username' in request.json:
        if len(request.json['username']) < 3:
            return abort(400)
        else:
            u.username = request.json['username']
    if 'password' in request.json:
        if len(request.json['password']) < 8:
            return abort(400)
        else:
            u.password = scramble(request.json['password'])
    try:
        db.session.commit()  # execute UPDATE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)
