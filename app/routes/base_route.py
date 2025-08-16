from flask import Blueprint,request
from app.controllers import BaseController
from app.decorators import requires_auth

class BaseRoute:
    def __init__(self,blueprint:Blueprint,controller:BaseController):
        self._blueprint = blueprint
        self._controller = controller
        
        self._create_routes()
        
        
    def _create_routes(self):
        
        @self._blueprint.route("/",methods=["GET"],strict_slashes=False)
        def route_get_all():
            return self._controller.controller_get_all(request)

        @self._blueprint.route("/",methods=["POST","OPTIONS"],strict_slashes=False)
        @requires_auth(["admin"])
        def route_add():
            return self._controller.controller_register(request)

        @self._blueprint.route("/",methods=["PUT","OPTIONS"],strict_slashes=False)
        @requires_auth(["admin"])
        def route_update():
            return self._controller.controller_update(request=request)

        @self._blueprint.route("/<int:id>",methods=["PUT"],strict_slashes=False)
        @requires_auth(["admin"])
        def route_update_by_id(id):
            return self._controller.controller_update(id=id,request=request)

        @self._blueprint.route("/<int:id>",methods=["DELETE"],strict_slashes=False)
        @requires_auth(["admin"])
        def route_delete_by_id(id):
            return self._controller.controller_delete(id=id)

        @self._blueprint.route("/<int:id>",methods=["GET"],strict_slashes=False)
        def route_get_by_id(id):
            return self._controller.controller_get_by_id(id=id,request=request)
        
    def get_blueprint(self):
        return self._blueprint