from flask import g
from flask import jsonify
from flask import render_template
from flask_login import login_required
from flask_login import logout_user
from social_flask.utils import load_strategy

from .app import app
from .app import sentry
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

@app.errorhandler(403)
def forbidden(e):
    return render_template('error.html',
            error_title=403,
            page_title="403 Forbidden"
            ), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html',
            error_title=404,
            page_title="404 Page Not Found"
            ), 404


@app.errorhandler(Exception)
@app.errorhandler(500)
def internal_server_error(error):
    context = {
        'error_title': 500,
        'page_title': '500 Internal Server Error',
    }
    if sentry:
        context['event_id'] = g.sentry_event_id
        context['public_dsn'] = sentry.client.get_public_dsn('https')
    return render_template('error.html',**context), 500
