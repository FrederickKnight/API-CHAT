from app.models import (
    BaseModel
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
    Session
)

from sqlalchemy import (
    ForeignKey,
    event
)

from sqlalchemy.dialects.postgresql import ENUM
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models import (
        User
    )

class Example(BaseModel):
    name:Mapped[str] = mapped_column(default="")
    quantity:Mapped[int] = mapped_column(default=0)
    user_id:Mapped[int] = mapped_column(ForeignKey("user.id"))

    user:Mapped["User"] = relationship("User",back_populates="examples")

@event.listens_for(Example,"before_insert")
def check_positive_quantity(mapper,connection,target:Example):

    if target.quantity < 0:
        raise ValueError("Quantity can't be in the negatives")