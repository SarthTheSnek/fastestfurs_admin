import os
import requests
from flask import Blueprint, redirect, url_for, session, current_app as app
from flask_discord import Unauthorized

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return app.discord.create_session(scope='identify guilds')


@auth.route('/callback')
def callback():
    app.discord.callback()
    check_permissions()
    return redirect(url_for('main.index'))


@auth.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect(url_for('.login'))


@auth.route('/logout')
def logout():
    app.discord.revoke()
    session.pop('PERM', None)
    return redirect(url_for('main.index'))


def check_permissions():
    user = app.discord.fetch_user()
    guilds = app.discord.fetch_guilds()
    if next((x for x in guilds if x._payload.get('id') == os.getenv('FF_SERVER_ID')), None):
        session['PERM'] = call_server(user.id)
    else:
        session['PERM'] = 1
    return session


def call_server(user) -> int:
    base_url = "https://discord.com/api"
    path = f"/guilds/{os.getenv('FF_SERVER_ID')}/members/{user}"
    token_value = f"Bot {os.getenv('DISCORD_BOT_SECRET')}"
    headers = {
            "Authorization": token_value
            }
    response = requests.get(base_url + path, headers=headers)
    if os.getenv('FF_LEADERSHIP_ROLE') in response.json().get('roles'):
        return 4
    elif os.getenv('FF_VOLUNTEER_ROLE') in response.json().get('roles'):
        return 2
    else:
        return 1
