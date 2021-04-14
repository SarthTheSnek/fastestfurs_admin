import os
import secrets
from flask import Flask
from flask_discord import DiscordOAuth2Session

discord = DiscordOAuth2Session()

def create_app():
    app = Flask(__name__)

    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'
    app.config['SECRET_KEY'] = secrets.token_urlsafe(32)
    app.config['DISCORD_CLIENT_ID'] = os.getenv('DISCORD_CLIENT_ID')
    app.config['DISCORD_CLIENT_SECRET'] = os.getenv('DISCORD_CLIENT_SECRET')
    app.config['DISCORD_REDIRECT_URI'] = os.getenv('DISCORD_REDIRECT_URI')
    app.config['DISCORD_BOT_TOKEN'] = os.getenv('DISCORD_BOT_TOKEN')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    discord.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')


    return app
