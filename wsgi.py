from flask import Flask, session, jsonify, abort, request
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
    if user.verify(session['password']):
        return jsonify(True)
    return jsonify(False)


@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return jsonify(True)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
