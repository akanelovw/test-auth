from .permissions import PERMISSIONS

def has_permission(user, resource, action):
    if not user or not user.is_active:
        return False

    role = user.role

    if role == "admin":
        return True

    role_permissions = PERMISSIONS.get(role, {})

    allowed_actions = role_permissions.get(resource, [])

    return action in allowed_actions