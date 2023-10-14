from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask_smorest import abort

def role_required(required_role):
    def decorator(func):
        # @jwt_required
        def wrapper(*args, **kwargs):
            current_user_id = get_jwt_identity()
            user_role = get_jwt().get("role")
            if user_role == required_role:
                return func(*args, **kwargs)
            abort(
                403,
                message="u don't have permission to dleete a item",
            )
        return wrapper
    return decorator
