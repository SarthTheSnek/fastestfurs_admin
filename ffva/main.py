from flask import Blueprint, render_template, redirect, url_for, current_app as app
from flask_discord import requires_authorization, Unauthorized

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template(
        'index.html',
        authorized=app.discord.authorized
    )


@main.route('/profile')
@requires_authorization
def profile():
    user = app.discord.fetch_user()
    return render_template(
        'profile.html',
        name=user.name,
        authorized=app.discord.authorized
    )


@main.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect(url_for('auth.login'))
