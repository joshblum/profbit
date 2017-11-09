from flask import g
from flask import jsonify
from flask import render_template
from flask_login import login_required
from flask_login import logout_user
from social_flask.utils import load_strategy

from .app import app
from .coinbase_stats import get_coinbase_stats


def _get_stats():
    social_auth_user = g.user.social_auth.get()
    # Coinbase returns `expires_in` but PSA expects `expires`
    social_auth_user.extra_data['expires'] = social_auth_user.extra_data[
            'expires_in']
    access_token = social_auth_user.get_access_token(load_strategy())
    return get_coinbase_stats(access_token)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/stats/')
@login_required
def stats():
    stats = _get_stats()
    return render_template('stats.html', stats=stats)


@app.route('/api/stats/')
@login_required
def stats_api():
    return jsonify(_get_stats())


@app.route('/logout/')
@login_required
def logout():
    """Logout view"""
    logout_user()
    return jsonify({
        'success': True,
    })
