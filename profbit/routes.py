import logging
from functools import wraps

from coinbase.wallet.error import APIError
from flask import g
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import login_required
from flask_login import logout_user
from htmlmin.minify import html_minify
from requests.exceptions import HTTPError
from social_flask.utils import load_strategy

from .app import app
from .app import sentry
from .coinbase_stats import get_coinbase_stats

logger = logging.getLogger(__name__)

CURRENCIES = {'total', 'btc', 'bch', 'eth', 'ltc'}
PERIODS = {None, 'hour', 'day', 'week', 'month', 'year', 'all'}


def minified_response(f):
    @wraps(f)
    def minify(*args, **kwargs):
        rendered_template = f(*args, **kwargs)
        return html_minify(rendered_template)
    return minify


@app.route('/keybase.txt')
def keybase():
    return app.send_static_file('keybase.txt')


@app.route('/')
@minified_response
def index():
    return render_template('index.html')


@app.route('/donate/')
@minified_response
def donate():
    return render_template('donate.html', donate_active='active')


@app.route('/stats/')
@login_required
@minified_response
def stats():
    return render_template('stats.html')


@app.route('/api/stats/')
@login_required
def stats_api():
    social_auth_user = g.user.social_auth.get()
    # Coinbase returns `expires_in` but PSA expects `expires`
    social_auth_user.extra_data['expires'] = social_auth_user.extra_data[
            'expires_in']
    access_token = social_auth_user.get_access_token(load_strategy())
    currency = request.args.get('currency', 'total').lower()
    period = request.args.get('period', 'hour').lower()
    redirect_url = url_for('error')
    if currency not in CURRENCIES or period not in PERIODS:
        response = {
            'error': True
        }
    else:
        try:
            response = get_coinbase_stats(access_token, currency, period)
        except Exception as e:
            logger.exception('APIError')
            if isinstance(e, APIError) and e.id == 'revoked_token':
                redirect_url = url_for('logout')
            if isinstance(e, HTTPError) and e.response.status_code == 401:
                redirect_url = url_for('logout')
            response = {
                'error': True
            }
    response['redirect_url'] = redirect_url

    return jsonify(response)


@app.route('/logout/')
@login_required
def logout():
    """Logout view"""
    logout_user()
    return redirect(url_for('index'))


@app.route('/error/')
def error():
    return internal_server_error(None, {
        'error_title': 'Oops',
        'page_title': 'Error',
        'refresh_stats': True,
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


@app.errorhandler(500)
def internal_server_error(e, context=None):
    if context is None:
        context = {
            'error_title': 500,
            'page_title': '500 Internal Server Error',
        }
    if sentry:
        context['event_id'] = g.sentry_event_id
    return render_template('error.html', **context), 500
