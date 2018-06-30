# -*- encoding: utf-8 -*-

"""
endpoint_users.py  
- provides the API endpoints for consuming and producing
	REST requests and responses
"""

from log_config import log
log.debug(">>> api_users ... creating api endpoints for USERS")

from  datetime import datetime, timedelta
from	bson import json_util
from	bson.objectid import ObjectId
from	bson.json_util import dumps

from flask import current_app, request
from flask_restplus import Namespace, Resource, fields, marshal, reqparse
from 	werkzeug.security 	import 	generate_password_hash, check_password_hash

### import JWT utils
import jwt
from flask_jwt_extended import (
		jwt_required, jwt_optional, create_access_token, create_refresh_token,
		get_jwt_identity, get_jwt_claims
)
from solidata_api._auth import admin_required

### import mongo utils
from solidata_api.application import mongo
from solidata_api._core.queries_db import * # mongo_users, etc...

### import auth utils
# from solidata_api._auth import token_required

# ### import data serializers
from solidata_api._serializers.schema_users import *  

### create namespace
ns = Namespace('users', description='Users list ')

### import parsers
from solidata_api._parsers.parser_pagination import pagination_arguments

### import models 
# from .models import * # model_user, model_new_user
from solidata_api._models.models_user import *  
model_new_user  = NewUser(ns).model
model_user			= User_infos(ns).model_complete


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### ROUTES
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

@ns.doc(security='apikey')
@ns.route('/')
class UsersList(Resource):

	@ns.doc('users_list')
	# @token_required
	# @jwt_required
	@admin_required
	@ns.expect(pagination_arguments)
	@ns.marshal_list_with( model_user, skip_none=True)#, envelop="users_list" ) 
	def get(self):
		"""
		list of all users in db 
		without _id 
		"""
		### DEBUGGING
		print()
		print("-+- "*40)
		log.debug( "ROUTE class : %s", self.__class__.__name__ )
		log.debug ("payload : \n{}".format(pformat(ns.payload)))

		### DEBUG check
		user_identity = get_jwt_identity()
		log.debug('useremail from jwt : \n%s', user_identity )  

		### get pagination
		args = pagination_arguments.parse_args(request)
		page = args.get('page', 1)
		per_page = args.get('per_page', 10)

		### retrieve from db
		cursor = mongo_users.find({}, {"_id": 0 })
		users = list(cursor)
		log.debug( "users : \n %s", pformat(users) )

		return users, 200






