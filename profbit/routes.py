from flask import g
from flask import jsonify
from flask_login import login_required
from flask_login import logout_user
from social_flask.utils import load_strategy

from .app import app
from .coinbase_stats import get_coinbase_stats


@app.route('/stats/')
@login_required
def get_stats():
    social_auth_user = g.user.social_auth.get()
    access_token = social_auth_user.get_access_token(load_strategy())
    return jsonify(get_coinbase_stats(access_token))


@app.route('/logout/')
@login_required
def logout():
    """Logout view"""
    logout_user()
    return jsonify({
        'success': True,
    })
