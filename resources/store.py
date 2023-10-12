from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required

from db import db
from models import StoreModel
from schemas import StoreSchema


blp = Blueprint("Stores", "stores", description="Operations on stores")


@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @jwt_required()
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store
    
    @jwt_required()
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted"}, 200


@blp.route("/store")
class StoreList(MethodView):
    @jwt_required()
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @jwt_required()
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A store with that name already exists.",
            )
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the store.")

        return store


# @blp.route("/store/<string:store_id>")


# @blp.route("/store", methods=['GET'])
# def get_stores():
#         return {"stores": list(stores.values())}

# @blp.route("/store", methods=['POST'])
# def create_store():
#         store_data = request.get_json()
#         if "name" not in store_data:
#             return {"message":"Bad request. Ensure 'name' is include in the JSON payload."}, 400
    
#         for store in stores.values():
#             if store_data["name"] == store["name"]:
#                 return {"message":"Store already exists."}, 400
    
#         store_id = uuid.uuid4().hex #Genreate code unique id
#         new_store = {**store_data, "id":store_id}
#         stores[store_id] = new_store
    
#         return new_store, 201


# @blp.route("/store/<string:store_id>", methods=['GET'])
# def get_store(store_id):
#         try:
#             return stores[store_id]
#         except:
#             return {"message":"Store not found"}, 404


# @blp.route("/store/<string:store_id>", methods=['DELETE'])
# def delete_store(store_id):
#     try:
#         del stores[store_id]
#         return {"message":"Store deleted"}
#     except:
#         return {"message":"Store not found"}, 404



# import uuid
# from flask import request
# from flask.views import MethodView
# from flask_smorest import Blueprint
# from db import stores

# blp= Blueprint("stores",__name__,description="Operations on Store")

# @blp.route("/store/<string:store_id>")
# #this will connect flask somrest with method view 
# class Store(MethodView):
#     #get method ke lie
#     def get(self,store_id):
#         try:
#             # Here you might also want to add the items in this store
#             # We'll do that later on in the course
#             return stores[store_id] 
#         except KeyError:
#             return {"message":"store not found"},404
#             # abort(404, message="Store not found.")
#     #delete req ke lie   
#     def delete(self,store_id):
#         try:
#             del stores[store_id]
#             return {"message": "Store deleted."}
#         except KeyError:
#             return {"message":"Store already exists"},404
#             # abort(404, message="Store not found.")


# @blp.route("/store") 
# class StoreList(MethodView):
#     def get(Self):
#         return {"stores": list(stores.values())}
    
#     def post(self):
#         store_data = request.get_json()
#         if "name" not in store_data:
#             return {"message":"Bad request. Ensure 'name' is included in the JSON payload"},400
#             # abort(
#             #     400,
#             #     message="Bad request. Ensure 'name' is included in the JSON payload.",
#             # )
#         for store in stores.values():
#             if store_data["name"] == store["name"]:
#                 return {"message":"Store already exists"},400
#                 # abort(400, message=f"Store already exists.")

#         store_id = uuid.uuid4().hex
#         store = {**store_data, "id": store_id}
#         stores[store_id] = store

#         return store