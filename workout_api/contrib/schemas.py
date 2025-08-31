from pydantic import BaseModel, Field, UUID4
from typing import Annotated
from datetime import datetime

class BaseSchema(BaseModel):
    """
    Schema base que todos os outros schemas herdarão.
    
    model_config:
        - extra = 'forbid': Não permite campos extras que não estejam definidos no schema.
        - from_attributes = True: Permite que o Pydantic crie o schema a partir de
                                  um modelo da base de dados (ORM), lendo os seus atributos.
                                  
    """
    model_config = {
        "extra": "forbid",
        "from_attributes": True
    }

class OutMixin(BaseSchema):
    """
    Mixin para schemas de saída que inclui campos comuns como id e created_at.
    """
    id: Annotated[UUID4, Field(description='Identificador')]
    created_at: Annotated[datetime, Field(description='Data de criação')]

