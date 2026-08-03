from pydantic import BaseModel

class Login(BaseModel):
    email: str
    senha: str

class Register(BaseModel):
    nome: str
    email: str
    senha: str

