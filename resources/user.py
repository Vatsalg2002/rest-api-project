from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256  #for hashing this si hashing algo for hasing passowrd
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    jwt_required,
    create_refresh_token,
    get_jwt_identity
) # for craeting token jwt while user login
from db import db
from models import UserModel
from schemas import UserSchema , LoginSchema
from blocklist import BLOCKLIST

blp=Blueprint("Users","users",description="Operations on users")

#for registering user
@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self,user_data):
        #to check if alredy exists
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, message="A user with that username already exists.")

        #user bana do naya pasword ko hash krke store kro
        user=UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"]),
            role=user_data["role"],
        )
        db.session.add(user)
        db.session.commit()

        return {"message": "User created successfully."}, 201
    
#for logj user
@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(LoginSchema)
    def post(self, user_data):
        #check user exits
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()
        #user exits now validate the passowrd nd return the token
        #agar use hai toh hi ye hoag wrna ye lfow abort m chla jaega
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            #acces tooen bana ke return krdo
            access_token = create_access_token(identity=user.id,additional_claims={'role': user.role}, fresh=True)
            #refresh token
            refresh_token = create_refresh_token(user.id,additional_claims={'role': user.role})
            return {"access_token": access_token, "refresh_token": refresh_token}, 200 
 
        abort(401, message="Invalid credentials.")

#refresh
@blp.route("/refresh")
class TokenRefresh(MethodView):
    #rrefresh true means it needs a token but it should be a refresh token not a fresh token
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()   # this is just short form of get_jwt().get("sub")
        new_token = create_access_token(identity=current_user, fresh=False) #fresh shoudld be false 
        # Make it clear that when to add the refresh token to the blocklist will depend on the app design
        # by adding refresh token to block list we ensure that rfesh token should be uysed only once we can set limit alos tht how ,any time refresh can be used
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"access_token": new_token}, 200
    
#for logout
@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        #it will grap jwt unique identifuer means jti and add tht jti to the blocklist
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200

#for deleting ans getting user info
@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}, 200
    

