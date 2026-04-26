from fastapi.encoders import jsonable_encoder
from app.schemas.response import StandardResponse

def to_compatible_response(standard_resp: StandardResponse, legacy: bool = True):
    """
    Converte um StandardResponse para o formato consumido pelo frontend (legado).
    Se legacy=True, retorna apenas o campo 'data'.
    Se legacy=False, retorna o StandardResponse completo.
    """
    if legacy:
        # Retorna apenas o conteúdo de data, preservando o shape original
        return jsonable_encoder(standard_resp.data)
    return jsonable_encoder(standard_resp)
