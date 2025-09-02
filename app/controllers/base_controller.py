from app import db
from app.custom_errors import (
    AttributeError,
    VersionError,
    InvalidIDError
)
from flask import Response,json,Request,request

from app.controllers.versions import (
    get_version
)

from sqlalchemy.orm import Query

from sqlalchemy import asc, desc

class BaseController:
    def __init__(self,model,schema):
        self._model = model
        self._schema = schema
        
        self.session = db.session  
        
        
    def controller_get_all(self,request:Request):
        version = request.headers.get("Accept")
        response,pagination_data = self.__query_args__(
            args = request.args
        )
        
        return self.__return_json__(
            response = response,
            version = version,
            pagination_data = pagination_data
        )
        
    
    def controller_register(self,request:Request):
        
        json_request = request.get_json()
        version = request.headers.get("Accept")
        json_request.pop("id",None)
            
        try:
            new_data = self._model(**json_request)
            self.session.add(new_data)
            self.session.commit()
            
        except Exception as e:
            self.session.rollback()
            raise e
        response = self.session.query(self._model).filter_by(id = new_data.id).first()
        return self.__return_json__(
            response = self.__parse_object__(response),
            version = version
        )
        
        
    def controller_update(self,id:int = None,request:Request = None):
        
        json_request = request.get_json()
        version = request.headers.get("Accept")

        if id and isinstance(id,int):
            if "id" in json_request:
                return Response(response=json.dumps({"message":"id in data and url"}),status=400,mimetype="application/json")
            _id = id
            json_request["id"] = id

        else:
            if not "id" in json_request:
                return Response(response=json.dumps({"message":"Not id in data"}),status=400,mimetype="application/json")
            _id = json_request["id"]
        
        _query = self.session.query(self._model).filter_by(id = _id).first()
        
        if not _query:
            return self.__return_json__(
                response = self.__parse_object__(_query),
                version = version
            )
        
        new_data = self._schema(**json_request).dict()

        try:
            for key,value in new_data.items():
                if hasattr(_query,key):
                    setattr(_query,key,value)
                    
            self.session.merge(_query)
            self.session.flush()
            self.session.commit()
            
        except Exception as e:
            self.session.rollback()
            raise e
        
        return self.__return_json__(
            response = self.__parse_object__(_query),
            version = version
        )
    
    def controller_delete(self,id):
        _query = self.session.query(self._model).filter_by(id=id).first()
        
        try:
            _query.soft_delete()
            
        except Exception as e:
            self.session.rollback()
            raise e
        
        return Response(status=204)

    def controller_get_by_id(self,id,request:Request):
        version = request.headers.get("Accept")

        response,pagination_data = self.__query_args__(
            args = request.args,
            _id = id
        )

        return self.__return_json__(
            response = response,
            version = version,
            pagination_data = pagination_data
        )

    ### Helpers
    def __return_json__(self,response,version:str = None,pagination_data:dict = {}):
        if isinstance(response,Response):
            return response
        
        res_version = get_version(
            version=version
        )

        if res_version:
            return res_version(
                response=response,
                type=type(self._model()).__name__,
                pagination_data = pagination_data
            ).get_response()
            
        else:
            raise VersionError("Error in versioning")
    
    def __query_args__(self,args = None,_id:int = None,need_all:bool = True):        
        query:Query = self.session.query(self._model)
        args = args if args else request.args

        is_active_text = args.get("is_active")
        if is_active_text:
            is_active = self.__str_to_bool__(is_active_text)
            query = query.filter_by(is_active = is_active)
        
        if _id:
            if isinstance(_id,int):
                query = query.filter_by(id = _id)
            else:
                raise InvalidIDError("Expected a number/interger id")
        
        filter_field = args.get("filter_field", type=str, default=None)
        filter_value = args.get("filter_value", type=str, default=None)
        if filter_field and filter_value:
            #busca todos los field separados por . en la query de la url
            if "." in filter_field:
                attrs = filter_field.split(".")
                
                rel_chain = []
                current_model = self._model
                
                #pasa por todos los atributos
                for attr in attrs[:-1]:
                    relation = getattr(current_model,attr)
                    related_model = relation.property.mapper.class_
                    rel_chain.append(relation)
                    current_model = related_model
            
                try:
                    final_attr = getattr(current_model,attrs[-1])
                     # junta los atributos con un join para el filtro
                    for rel in rel_chain:
                        query = query.join(rel)
                        
                    query = query.filter(final_attr == filter_value)
                    
                except:
                    raise AttributeError("Expected a valid attribute in query args")

            else:
                query = query.filter(getattr(self._model, filter_field) == filter_value)
        
        order = args.get("order",type=str,default="").lower()
        if order == "asc":
            query = query.order_by(self._model.created_at.asc())
        if order == "desc":
            query = query.order_by(self._model.created_at.desc())

        pagination_data = {}

        limit = args.get("limit",type=int,default=200)
        page = args.get("page",type=int,default=1)

        total = query.count()
        pagination_data["total"] = total

        pagination_data["limit"] = limit
        pagination_data["page"] = page
        pagination_data["pages"] = (total // limit) + (1 if total % limit else 0)

        offset = (page - 1) * limit
        query = query.limit(limit).offset(offset)

        result = query.all() if need_all else query.first()
        
        show_relations = self.__str_to_bool__(args.get("relations",default="false"))

        if result:
            return self.__parse_object__(
                data = result,
                show_relations = show_relations
            ), pagination_data
            
        else:
            return Response(status=204),pagination_data
        
    def __parse_object__(self,data,show_relations:bool = False):
        if isinstance(data,list):
            return [dt.get_json(show_relations) for dt in data]
        else:
            return [data.get_json(show_relations)]
        
    def __str_to_bool__(self,val:str):
        return val.lower() in ["true","1","yes","y"]