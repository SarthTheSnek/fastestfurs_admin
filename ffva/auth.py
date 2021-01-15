from flask import Blueprint, redirect, url_for, render_template, current_app as app
from flask_discord import requires_authorization, Unauthorized

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return app.discord.create_session(scope='identify guilds')


@auth.route('/callback')
def callback():
    app.discord.callback()
    return redirect(url_for('auth.profile'))


@auth.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect(url_for('.login'))


@auth.route('/logout')
def logout():
    app.discord.revoke()
    return redirect(url_for('main.index'))
