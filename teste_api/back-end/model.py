from pydantic import BaseModel
from typing import Optional

class OperadoraResponse(BaseModel):
    registro_operadora: int
    cnpj: str
    razao_social: str
    nome_fantasia: Optional[str]
    modalidade: Optional[str]
    cidade: Optional[str]
    uf: Optional[str]
    telefone: Optional[str]
    email: Optional[str]
    representante: Optional[str]
    data_registro: str