import os
import jwt

from flask import jsonify, request
from functools import wraps

# decorator for api routes
def required_params(*params):
    def route_decorator(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            missing_params = []
            for param in params:
                if not param in request.json:
                    missing_params.append(param)
            if missing_params:
                return jsonify("missing parameters: %s" % (", ".join(missing_params))), 400
            return func(args, **kwargs)
        return func_wrapper
    return route_decorator

# class decorator to apply validate_request_token on all routes
def validate_jwt_all_routes():
    """
    enforces basic jwt checking on all routes
    """
    def valiate_routes(cls):
        for attr in cls.__dict__: # there's propably a better way to do this
            if callable(getattr(cls, attr)):
                setattr(cls, attr, _jwt_validation_decorator(getattr(cls, attr)))
        return cls
    return valiate_routes

# decorator for tokens and perms
def validate_jwt():
    return _jwt_validation_decorator

def validate_request_perms(*perms):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        if perms:
            allowed_perms = payload.get("perms")
            if not set(perms).issubset(set(allowed_perms)):
                return jsonify({'message': 'Invalid Permissions'}), 401
        return func(*args, **kwargs)
    return func_wrapper

# def _jwt_validation_decorator(func):
    # @wraps(func)
    # def func_wrapper(*args, **kwargs):
    #     request.user = None
    #
    #     token = request.headers.get('authorization')
    #     if not token:
    #         return jsonify({'message': 'Invalid Token'}), 401
    #
    #     try:
    #         payload = jwt.decode(token, os.environ.get("JWT_SECRET", 'super-secret'), algorithms=['HS256'])
    #     except (jwt.DecodeError, jwt.ExpiredSignatureError):
    #         return jsonify({'message': 'Invalid Token'}), 401
    #
    #     request.user = Users.query.get(payload['user_id'])
    #     return func(*args, **kwargs)
    # return func_wrapper
