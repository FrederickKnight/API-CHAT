from flask import Response,json
from .custom_errors import AppError

from sqlalchemy.exc import (
    IntegrityError
)

def _get_schema_error(error,message,details):
    return {
        "data": [],
        "metadata": {
            "context": "",
            "error": error,
            "message": message,
            "details": details,
        }
    }

def register_error_handlers(app):
    @app.errorhandler(AppError)
    def handle_app_error(error):
        raise error
        schema_error = _get_schema_error(error.error,error.message,error.details)
        return Response(response=json.dumps(schema_error), status=400, mimetype="application/json")

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error):
        raise error
        schema_error = _get_schema_error(
            error="Integrity Error",
            message="Invalid given data or parameters",
            details=str(error.orig) if hasattr(error, "orig") else str(error)
        )
        return Response(response=json.dumps(schema_error), status=400, mimetype="application/json")

    @app.errorhandler(Exception)
    def handle_generic_error(error):
        raise error
        schema_error = _get_schema_error(error="Unhandled Error",message="Something went wrong",details=str(error))
        return Response(response=json.dumps(schema_error), status=500, mimetype="application/json") 
    
    
    @app.errorhandler(TypeError)
    def handle_type_error(error):
        raise error
        schema_error = _get_schema_error(error="Type Error",message="Invalid type given",details=str(error))
        return Response(response=json.dumps(schema_error), status=400, mimetype="application/json")