from flask import Blueprint, render_template, redirect, url_for, session, current_app as app
from flask_discord import requires_authorization, Unauthorized

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if session.get('PERM'):
        user = app.discord.fetch_user()
    else:
        user = None

    return render_template(
        'index.html',
        user=user,
        authorized=app.discord.authorized,
        perm_level=session['PERM']
    )


@main.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect(url_for('auth.login'))