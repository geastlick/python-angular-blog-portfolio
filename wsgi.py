from flask import session, jsonify, abort, request
from src import create_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.wrappers import Response

from src.models import User

app = create_app()
app.wsgi_app = DispatcherMiddleware(
    Response('Not Found', status=404),
    {'/api': app.wsgi_app}
)


@app.route('/login', methods=['POST'])
def login():
    if 'username' not in request.json or 'password' not in request.json:
        return abort(400)
    user = User.query.filter_by(username=request.json['username']).first()
    if user is None:
        return abort(400)
    if user.verify(request.json['password']):
        session['username'] = user.username
        session['userid'] = user.id
        return jsonify(True)
    return jsonify(False)


@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    session.pop('userid', None)
    return jsonify(True)


@app.route('/self')
def self():
    if "username" not in session or "userid" not in session:
        return abort(400)
    user = User.query.get(session['userid'])
    if user is None:
        # This is a security issue ... username set in the session for an invalid user!
        session.pop('username', None)
        session.pop('userid', None)
        return abort(400)
    return jsonify(user.serialize())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
