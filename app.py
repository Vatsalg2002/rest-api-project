from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
import secrets
from flask import Flask, jsonify
import models



from db import db
from resources.user import blp as UserBlueprint
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from blocklist import BLOCKLIST


def create_app(db_url=None):
    app = Flask(__name__)
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or "sqlite:///data.db"

    #if we want to configure 2nd database with db2 

    # app.config['SQLALCHEMY_BINDS'] = {
    # 'db2': 'url link of data base 2'
    # }
    # Configuration for database 1

    #making mulirple instance of multiple data base

    # app.config['SQLALCHEMY_DATABASE_URI_DB1'] = 'database1_connection_url'
    # db1 = SQLAlchemy(app)

    # app.config['SQLALCHEMY_DATABASE_URI_DB2'] = 'database2_connection_url'
    # db2 = SQLAlchemy(app)

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)

    app.config["JWT_SECRET_KEY"] = "6362923995624453934117852946341749416"
    #recommende dot store key in evirimant instaed of in app
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    #cutsom error for logged out token / blocked list token
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )
    
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                { 
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )

    #jwt clains to add extra inf in jwt token
    @jwt.additional_claims_loader
    #here identity will be taht thing that we wil pass while creating aa jwt token while login tht will be passed here
    def add_claims_to_jwt(identity):
        #rhis info will be added to the jwt token and can be sued later on for special roles
        #good method to do so is look into db nd check for the role of idenity of input 
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}
    

    #custom errros for errors related to autorirztaion usinh jwt token
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            #jsonify to convert dict to json as retrun/reposne cant be a dictionary
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )
    #as we are making ou db using alemic migration hence no need odf this
    # with app.app_context():
    #     db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app


# app.config['SQLALCHEMY_DATABASE_URI_DB1'] = 'database1_url'
# db1 = SQLAlchemy(app)

# app.config['SQLALCHEMY_DATABASE_URI_DB2'] = 'database2_url'
# db2 = SQLAlchemy(app)

# #for models while making models w e will make them as

# class table1(db1.model)

# class table1(db2.model)

# #in route deifning we can access db according to our decision as

# if value%2==0
#  db=db1
# else
#  db=db2

# now using the db
# #data=db.session.query(table).filter() #whta ver u want to do u can do tht with tht particular table


# @app.post("/store")
# def create_store():
#     store_data = request.get_json()
#     if "name" not in store_data:
#          return {"message":"Bad request. Ensure 'name' is included in the JSON payload"},400
#         # abort(
#         #     400,
#         #     message="Bad request. Ensure 'name' is included in the JSON payload.",
#         # )
#     for store in stores.values():
#         if store_data["name"] == store["name"]:
#             return {"message":"Store already exists"},400
#             # abort(400, message=f"Store already exists.")

#     store_id = uuid.uuid4().hex
#     store = {**store_data, "id": store_id}
#     stores[store_id] = store

#     return store


# @app.delete("/store/<string:store_id>")
# def delete_store(store_id):
#     try:
#         del stores[store_id]
#         return {"message": "Store deleted."}
#     except KeyError:
#         return {"message":"Store already exists"},404
#         # abort(404, message="Store not found.")

# #ITEMS



# @app.get("/item")
# def get_all_items():
#     # return "hwllo world"
#     return {"items": list(items.values())}

# @app.get("/item/<string:item_id>") 
# def get_item(item_id):
#     try:
#         return items[item_id]
#     except KeyError:
#         # abort(404, message="Item not found.")
#         return {"message":"item nit found"},404


# @app.post("/item") 
# def create_item():
#     item_data = request.get_json()
#     # Here not only we need to validate data exists,
#     # But   also what type of data. Price should be a float,
#     # for example.
#     if (
#         "price" not in item_data
#         or "store_id" not in item_data
#         or "name" not in item_data
#     ):
#         return {"message":"Bad request. Ensure 'price', 'store_id', and 'name' are included in the JSON payload."},400
#         # abort(
#         #     400,
#         #     message="Bad request. Ensure 'price', 'store_id', and 'name' are included in the JSON payload.",
#         # )
#     for item in items.values():
#         if ( 
#             item_data["name"] == item["name"]
#             and item_data["store_id"] == item["store_id"]
#         ):
#             return {"message":"Item already exists."},400
#             # abort(400, message=f"Item already exists.")

#     item_id = uuid.uuid4().hex
#     item = {**item_data, "id": item_id}
#     items[item_id] = item

#     return item





# @app.put("/item/<string:item_id>")
# def update_item(item_id):
#     item_data = request.get_json()
#     # There's  more validation to do here!
#     # Like making sure price is a number, and also both items are optional
#     # Difficult to do with an if statement...
#     if "price" not in item_data or "name" not in item_data:
#         return {"message":"Bad request. Ensure 'price', and 'name' are included in the JSON payload."},400
#         # abort(
#         #     400,
#         #     message="Bad request. Ensure 'price', and 'name' are included in the JSON payload.",
#         # )
#     try:
#         item = items[item_id]

#         # https://blog.teclado.com/python-dictionary-merge-update-operators/
#         #dictionary updat e operator |=
#         item |= item_data

#         return item
#     except KeyError:
#         return {"message":"tem not found"},404
#         # abort(404, message="Item not found.")

# @app.delete("/item/<string:item_id>")
# def delete_item(item_id):
#     try:
#         del items[item_id]
#         return {"message": "Item deleted."}
#     except KeyError:
#         return {"message":"Item not found"},404
#         # abort(404, message="Item not found.")






# if __name__ == "__main__":
#     app().run()




# # from flask import Flask,request
# # from flask import request 
# from db import items,stores
# import uuid
# from flask import Flask, request
# from flask_smorest import abort

# app=Flask(__name__)  #this will create a flask app

# #rn we are using list to store the data
# # stores={
     
# # }

# # items={
# #      1:{
# #           "name":"chair",
# #           "price":17.99
# #      },
# #      2:{
# #           "name":"Table",
# #           "price":180.67
# #      }
# # }

# # items[1] #this wil give item with id 1 hence finidng item with id is easy

# #creating endpoint that will return the data when client request it

# #app pr ek get type ki request on route /store

# #https://127.0.0.1:5000/store


# #getting all stores

# @app.get("/store")   #/stor eis the endpoint and get_store is the  function associated uwth this endpoint
# def get_stores():
#     # #returning data in response
#     # return {"stores":stores}
#     # #this data is seen on browser
#     return {"stores":list(stores.values())}


# #creating new store

# @app.post("/store")
# def create_store():
#     #get json that client has send
#     #this request daat is a dictionary
#     store_data=request.get_json()
#     if "name" not in store_data:
#          abort(
#               400,
#               message="bad request ensure name is included inpayload"
#          )
#     for store in stores.values():
#          if store_data["name"]==store["name"]:
#               abort(400,message="store laredy eixsts")
#     store_id=uuid.uuid4().hex
#     #new dictonary bana di
#     # new_store={"name":request_data["name"],"items":[]}
#     #** will unpack the data of storedata which is dictionary and include them in this new dictiomanry
#     store={**store_data,"id":store_id}
#     #append krdo
#     # stores.append(new_store)
#     stores[store_id]=store
#     #return the data and a ststus code of success
#     return store, 201
    
# #creating item

# #client will sen dstore nam ein url

# @app.post("/item")
# #this is how data from url is fetched here as name variable and passed in function
# def create_item():
#     #fetch upcimg data
#     item_data=request.get_json()
#     #for full validation we not only need to check the data preseicne but also its type  for ex price should be floaat
#     if(
#          "price" not in item_data
#          or "store_id" not in item_data
#          or "name" not in item_data
#     ):
#          abort(
#               400,
#               message="bad request ensre price name nd id must be there in the requesr"
#          )
#     for item in items.value():
#          if(
#               item_data["name"]==item["name"]
#               and item_data["store_id"]==item["store_id"]
#          ):
#               abort(400, message="item already exists")
#     if item_data["store_id"] not in stores:
#          #check if valiud
#         #  return {"message":"stor enit found"},404
#         abort(404,message="stor enot found")

#     item_id=uuid.uuid4().hex
#     item={**item_data,"id":item_id}
#     item[item_id]=item

#     return item,201
#     # for store in stores:
#     #     if store["name"]==name:
#     #         #new item bnai hai use store ki items m append krdia
#     #         new_item={"name":item_data["name"],"price":request_data["price"]}
#     #         store["items"].append(new_item)
#     #         return new_item, 201
#     # #wht if store is not found in the stores return the message in a json and a status code with comma
#     # return {"message":"store not found"},404

# #all items as saved in seprate dict
# @app.get("/item")
# def get_all_items():
#      return {"items":list(items.values())}

# #getting specific store details with its items

# @app.get("/store/<string:store_id>")
# def get_store(store_id):
#         # for store in stores:
#         #      if store["name"]==name:
#         #           return store,201
#         try:
#              return stores[store_id]
#         #for if data fo this store not found
#         except KeyError:
#             abort(404,message="stor enot found")

# #getting items of specific store

# @app.get("/item/<string:item_id>")
# def get_item(item_id):
#     try:
#          return items[item_id]
#     except:
#          abort(404,message="item enot found")
