from .settings import *

from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)  # loads the configs from .env
# From now on, you can use os.getenv("SOME_KEY_FROM_ENV_FILE") to get access to a secret key

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST")
    }
}

RQ_QUEUES = {
    "default": {
        "HOST": "localhost",
        "PORT": 6379,
        "DB": 0,
        "PASSWORD": os.getenv("REDIS_PASSWORD")
    },
}

# Email-sending configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_SUBJECT_PREFIX = "[dev-alert.riparias.be] "
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL = "LIFE RIPARIAS early alert - dev<info@dev-alert.riparias.be>"  # Used for normal messages
SERVER_EMAIL = "LIFE RIPARIAS early alert - dev<info@dev-alert.riparias.be>"

SITE_BASE_URL = "http://dev-alert.riparias.be"

ADMINS = [
    ("Nicolas", "nicolas@niconoe.eu"),
]


def build_gbif_predicate_belgium_after2000(species_list: "QuerySet[Species]"):
    """
    Build a GBIF.org download predicate for Belgian observations, after 2000.

    Species list is taken from the GBIF Alert database.
    """
    return {
        "predicate": {
            "type": "and",
            "predicates": [
                {"type": "equals", "key": "COUNTRY", "value": "BE"},
                {
                    "type": "in",
                    "key": "TAXON_KEY",
                    "values": [f"{s.gbif_taxon_key}" for s in species_list],
                },
                {"type": "equals", "key": "OCCURRENCE_STATUS", "value": "present"},
                {
                    "type": "greaterThanOrEquals",
                    "key": "YEAR",
                    "value": 2000,
                },
            ],
        }
    }

GBIF_ALERT = {
    "SITE_NAME": "LIFE RIPARIAS early alert",
    "NAVBAR_BACKGROUND_COLOR": "#00a58d",
    "NAVBAR_LIGHT_TEXT": True,
    "ENABLED_LANGUAGES": (
        "en",
        "fr",
    ),
    # A Gbif.org account is necessary to automatically download observations via the `import_observations` command
    "GBIF_DOWNLOAD_CONFIG": {
        "USERNAME": os.getenv("GBIF_USERNAME"),
        "PASSWORD": os.getenv("GBIF_PASSWORD"),
        "PREDICATE_BUILDER": build_gbif_predicate_belgium_after2000,
    },
    "SHOW_DEV_VERSION_WARNING": True,
    "MAIN_MAP_CONFIG": {
        "initialZoom": 8,
        "initialLat": 50.50,
        "initialLon": 4.47,
    },
}

ALLOWED_HOSTS = ['dev-alert.riparias.be']
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')