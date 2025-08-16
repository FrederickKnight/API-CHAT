from pydantic import BaseModel, Field, PrivateAttr, model_validator, field_validator

class ExampleSchema(BaseModel):
    name:str
    quantity:int = Field(default=0)
    user_id:int

    @field_validator("quantity",mode="before")
    @classmethod
    def validate_quantity(cls,quantity):

        if not quantity:
            raise ValueError("Quantity must have a value")

        if not isinstance(quantity,int):
            raise TypeError(f"Expected integer not {type(quantity).__name__}")
        
        if quantity < 0:
            raise ValueError("Quantity can't be in the negatives")

        return quantity