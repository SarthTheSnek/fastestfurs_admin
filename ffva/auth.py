from flask import Blueprint, redirect, url_for, render_template
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized

auth = Blueprint('auth', __name__)
discord = DiscordOAuth2Session()


@auth.route('/login')
def login():
    return discord.create_session()


@auth.route('/callback')
def callback():
    discord.callback()
    return redirect(url_for('auth.profile'))


@auth.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect(url_for('.login'))


@auth.route('/logout')
def logout():
    return 'Logout'


@auth.route('/profile')
@requires_authorization
def profile():
    user = discord.fetch_user()
    return render_template('profile.html', name=user.name)