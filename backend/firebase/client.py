import firebase_admin
from firebase_admin import credentials, firestore

_app = None


def get_db():
    global _app
    if _app is None:
        from config import settings
        cred = credentials.Certificate(settings.firebase_credentials_path)
        _app = firebase_admin.initialize_app(cred)
    return firestore.client()
