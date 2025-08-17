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

class BaseController:
    def __init__(self,model,defaults,schema):
        self._model = model
        self._defaults = defaults
        self._schema = schema
        
        self.session = db.session  
        
        
    def controller_get_all(self,request:Request):

        version = request.headers.get("Accept")
        return self.__return_json__(self.__query_args__(request.args),version)
        
    
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
        return self.__return_json__(self.session.query(self._model).filter_by(id = new_data.id).first(),version)
        
        
    def controller_update(self,id = None,request:Request = None):
        
        json_request = request.get_json()
        version = request.headers.get("Accept")
        
        if not id or not isinstance(id,int):
            if "id" in json_request:
                _id = json_request["id"]
            else:
                return Response(response=json.dumps({"message":"Not id in data"}),status=400,mimetype="application/json")
        else:
            _id = id
            if "id" in json_request:
                return Response(response=json.dumps({"message":"id in data and url"}),status=400,mimetype="application/json")
        
        self._defaults["id"] = _id
        _query = self.session.query(self._model).filter_by(id = _id).first()
        
        if not _query:
            return self.__return_json__(_query,version)
        
        new_data = {**self._defaults,**json_request}

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
        
        return self.__return_json__(_query,version)
    
    def controller_delete(self,id):
        _query = self.session.query(self._model).filter_by(id=id).first()
        
        try:
            # self.session.delete(_query)
            # self.session.commit()
            _query.soft_delete()
            
        except Exception as e:
            self.session.rollback()
            raise e
        
        return Response(status=204)


    def controller_get_by_id(self,id,request:Request):
        version = request.headers.get("Accept")
        return self.__return_json__(self.__query_args__(request.args,id),version)


    ### Helpers
    def __return_json__(self,response,version:str = None):
        if isinstance(response,Response):
            return response
        
        res_version = get_version(
            version=version
        )

        if res_version:
            return res_version(
                response=response,
                type=type(self._model()).__name__
            ).get_response()
            
        else:
            raise VersionError("Error in versioning")
    
    def __query_args__(self,args = None,_id:int = None):        
        _q = self.session.query(self._model)
        args = args if args else request.args
        
        if _id:
            if isinstance(_id,int):
                _q = _q.filter_by(id = _id)
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
                        _q = _q.join(rel)
                        
                    _q = _q.filter(final_attr == filter_value)
                    
                except:
                    raise AttributeError("Expected a valid attribute in query args")

            else:
                _q = _q.filter(getattr(self._model, filter_field) == filter_value)
        
        
        limit = args.get("limit",type=int,default=None)
        if limit is not None:
            _q = _q.limit(limit)
            
        offset = args.get("offset",type=int,default=0)
        if offset > 0:
            _q = _q.offset(offset)
            
        page = args.get("page",type=int,default=1)
        if page > 1:
            _p = (page - 1) * limit if limit else (page - 1)
            _q = _q.offset(_p)
            
        # return first or all
        first = args.get("first",type=bool,default=False)
        
        result = _q.first() if first else _q.all()
        
        show_relations = self.__str_to_bool__(args.get("relations",default="false"))
        if result:
            if isinstance(result,dict) or isinstance(result,list):
                _response = [item.get_json(show_relations) for item in result]

            else:
                _response = [result.get_json(show_relations)]
            return _response
        else:
            # retornar data vacio
            return Response(status=204)
        
    def __str_to_bool__(self,val:str):
        return val.lower() in ["true","1","yes","y"]