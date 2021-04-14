from flask import Blueprint, render_template, redirect, url_for, session, current_app as app
from flask_discord import requires_authorization, Unauthorized
from .auth import must_be_leadership

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if session.get('PERM'):
        user = app.discord.fetch_user()
        perm_level = session['PERM']
    else:
        user = None
        perm_level = 1

    return render_template(
        'index.html',
        user=user,
        authorized=app.discord.authorized,
        perm_level=perm_level
    )


@main.route('/stream')
@must_be_leadership
def stream():
    user = app.discord.fetch_user()
    perm_level = session['PERM']
    return render_template(
        'stream.html',
        user=user,
        authorized=app.discord.authorized,
        perm_level=perm_level
    )


@main.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect(url_for('auth.login'))

