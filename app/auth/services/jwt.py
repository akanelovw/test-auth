import jwt
import datetime
import uuid
from django.conf import settings

SECRET_KEY = settings.SECRET_KEY

def generate_jwt(user):
    payload = {
        "user_id": str(user.id),
        "email": user.email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        "iat": datetime.datetime.utcnow(),
        "jti": str(uuid.uuid4())
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token