from .base_controller import BaseController

from app.models import (
    UserZoe,
    MessageWelcome
)

from app.schemas import (
    UserZoeSchema
)
from app.chat import handle_zoe_welcome_message
from flask import Response,Request
from app.controllers.versions import (
    get_version
)

class ZoeController(BaseController):
    def __init__(self):
        super().__init__(
            model=UserZoe,
            schema=UserZoeSchema
        )

    def controller_welcome_message(self,id:int,request:Request) -> Response:
        query_message = self.session.query(MessageWelcome).filter_by(id_user = id).first()
        create_new = self.__str_to_bool__(request.args.get("new",type=str,default="false")) or not query_message
        
        try:
            if create_new:
                message = handle_zoe_welcome_message(id)
                if query_message:
                    query_message.message = message
                else:
                    self.session.add(MessageWelcome(id_user=id, message=message))
            else:
                message = query_message.message

            self.session.commit()

        except Exception as e:
            self.session.rollback()
            raise e
        
        return Response(response=message, status=200)