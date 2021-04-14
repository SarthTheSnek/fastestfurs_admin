from flask import Blueprint, render_template, redirect, url_for, session, current_app as app
from flask_discord import requires_authorization, Unauthorized
from .auth import must_be_leadership

admin = Blueprint('admin', __name__)

@admin.route('/')
@must_be_leadership
def index():
    return render_template(
        'admin.html',
        user=app.discord.fetch_user(),
        authorized=app.discord.authorized,
        perm_level=session['PERM']
    )


@admin.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect(url_for('main.index'))

