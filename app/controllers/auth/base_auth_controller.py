from app import db
from flask import Response,json,Request,request

from os import urandom
import binascii
from hashlib import sha256

from datetime import datetime, timedelta
from app.utils import create_timestampt

from app.custom_errors import (
    ValidationError,
    AttributeError,
    VersionError,
    InvalidIDError
)

from app.controllers.versions import (
    get_version
)
from app.models.users import(
    BaseUser
)

class BaseAuthController:
    def __init__(self,user_model,session_model,user_schema,session_schema):
        self._model:BaseUser = user_model
        self._user_session = session_model

        self._user_schema = user_schema
        self._session_schema = session_schema

        self.session = db.session

    def register_user(self,data,request:Request):
        version = request.headers.get("Accept")

        if "id" in data:
            data["id"] = None
        
        user_already_exist = True if self.__query_username__(data["username"]) else False
        if not user_already_exist:
            if not "password" in data:
                raise ValidationError("invalid given data, not password")
            
            try:

                user_data = self._user_schema(**data).dict()
                new_data:BaseUser = self._model(**user_data)
                new_data.set_password(data["password"])

                self.session.add(new_data)
                self.session.commit()
                
            except Exception as e:
                self.session.rollback()
                raise e

            register_result = self.session.query(self._model).filter_by(id = new_data.id).first()
            return self.__return_json__(
                response=register_result,
                version=version
            )
        else:
            raise ValidationError("User already exist")
        
    def delete_user_by_id(self,id):
    
        _user:BaseUser = self.__query_id__(id)
        
        if _user != None:
            try:
                _user.soft_delete()
                
            except Exception as e:
                self.session.rollback()
                raise e
            
            return Response(status=204)
        else:
            raise ValidationError("User doesn't exist or invalid given data")
        
    
    def get_all(self,request:Request):
        version= request.headers.get("Accept")
        users = self.session.query(self._model).all()

        if len(users) > 0 and users:
            return self.__return_json__(
                response=users,
                version=version
            )
        else:
            raise ValidationError("There is no users")

    def get_by_id(self,id,request:Request):
        version = request.headers.get("Accept")
        user = self.__query_id__(id)
        
        if user != None:
            return self.__return_json__(
                response=user,
                version=version
            )
        else:
            raise ValidationError("User doesn't exist or invalid given data")
            
    def validate_user(self,data,request:Request):
        if "username" in data and "password" in data:
            version = request.headers.get("Accept")

            _user = self.__query_username__(data["username"])
            if _user == None:
                raise ValidationError("User doesn't exist or invalid given data")
                
            data_pass = _user.validate_password(data["password"])
            
            if data_pass == False:
                raise ValidationError("Password is incorrect or invalid given data")
                
            return self.__return_json__(
                response=_user,
                version=version
            )
        
        else:
            raise ValidationError("invalid given data, not username or password")
        

    # auth
    def generateSessionToken(self):
        bytes = urandom(20)
        token = binascii.hexlify(bytes).decode()
        return Response(response=json.dumps({"token":token}),status=200,mimetype="application/json")
        

    def createSessionToken(self,_json,UserId:int):
        if not "token" in _json:
            raise ValidationError("there is no token")
        
        token = _json["token"]    
        userSessionId = sha256(token.encode('utf-8'),usedforsecurity=True).hexdigest()

        session_data = self._session_schema(
            id_user = UserId,
            session = userSessionId
        ).dict()

        try:
            new_session = self._user_session(**session_data)
            self.session.add(new_session)
            self.session.commit()
            
        except Exception as e:
            self.session.rollback()
            raise e
        
        return Response(response=json.dumps(session_data),status=200,mimetype="application/json")
        
        
    def validateSessionToken(self,token:str) -> Response:
        userSessionId = sha256(token.encode('utf-8'),usedforsecurity=True).hexdigest()
        _query = self.session.query(self._user_session).filter_by(session = userSessionId).first()
        
        sessionData = {
            "session":None,
            "user":None
        }
        
        if not _query:
            return {
            "session":None,
            "user":None
        }
        
        sessionJson = _query.get_json(True)
        expiration_Date = datetime.fromtimestamp(sessionJson["expires_at"])
        if datetime.now() >= expiration_Date:
            # si expiro
            self.session.delete(_query)
            self.session.commit()
            return {
                "session":None,
                "user":None
            }
        
        if datetime.now() >= (expiration_Date - timedelta(days=-15)):
            # si es menor a 15 dias
            _query.expires_at = create_timestampt()
            self.session.merge(_query)
            self.session.flush()
            self.session.commit()

        id_user = sessionJson["user"]["id"]
        sessionData["user"] = sessionJson["user"]
        
        del sessionJson["user"]
        sessionJson["id_user"] = id_user
        sessionData["session"] = sessionJson
        return Response(response=json.dumps(sessionData),status=200,mimetype="application/json")

    def invalidateSession(self,userSessionId:str):
        _query = self.session.query(self._user_session).filter_by(session = userSessionId).first()
        if _query:
            self.session.delete(_query)
            self.session.commit()
            return Response(status=204,mimetype="application/json")
        else:
            raise ValidationError("Invalid Session")

    #helpers
    def __return_json__(self,response:Response,version:str = None):
        if isinstance(response,Response):
            return response
        
        res_version = get_version(
            version=version
        )

        if res_version:

            if isinstance(response,list):
                _response = [res.get_json() for res in response]

            else:
                _response = [response.get_json()]

            return res_version(
                response=_response,
                type=type(self._model()).__name__
            ).get_response()
        
        else:
            raise VersionError("Error in versioning")
            
    def __query_id__(self,_id):
        if isinstance(_id,int):
            return self.session.query(self._model).filter_by(id = _id).first()
        return None

    def __query_username__(self,_username):
        if isinstance(_username,str):
            return self.session.query(self._model).filter_by(username = _username).first()
        return None