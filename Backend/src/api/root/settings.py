import os
import sys
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


DEBUG = sys.gettrace()
LOCALHOST = "localhost"
BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# Spotify credentials
SPOTIFY_CLIENT_ID = str(os.getenv("SPOTIFY_CLIENT_ID"))
SPOTIFY_SECRET = str(os.getenv("SPOTIFY_SECRET"))
SPOTIFY_CALLBACK_REDIRECT_URI = str(os.getenv("SPOTIFY_CALLBACK_REDIRECT_URI"))
SPOTIFY_CALLBACK_REDIRECT_URI_IOS = str(os.getenv("SPOTIFY_CALLBACK_REDIRECT_URI_IOS"))

# JWT
ALGORITHM = str(os.getenv("ALGORITHM"))
SECRET_KEY = str(os.getenv("SECRET_KEY"))
SECRET_KEY_REFRESH = str(os.getenv("SECRET_KEY_REFRESH"))
EXPIRED_TIME_ACCESS_TOKEN = int(os.getenv("EXPIRED_TIME_ACCESS_TOKEN"))
EXPIRED_TIME_REFRESH_TOKEN = int(os.getenv("EXPIRED_TIME_REFRESH_TOKEN"))

# EXTERNAL BASE URL
EXTERNAL_URL = str(os.getenv("EXTERNAL_URL"))

# SERVICES NAMES
SPOTIFY = "Spotify"
APPLE_MUSIC = "Apple Music"


# Apple Credentials
APPLE_MUSIC_DEVELOPER_TOKEN = os.getenv("APPLE_MUSIC_DEVELOPER_TOKEN")

MONGO_SERVER = str(os.getenv("MONGO_SERVER"))
MONGO_PORT = str(os.getenv("MONGO_PORT"))
MONGO_INITDB_DATABASE = str(os.getenv("MONGO_INITDB_DATABASE"))
MONGO_INITDB_ROOT_USERNAME = str(os.getenv("MONGO_INITDB_ROOT_USERNAME"))
MONGO_INITDB_ROOT_PASSWORD = str(os.getenv("MONGO_INITDB_ROOT_PASSWORD"))
