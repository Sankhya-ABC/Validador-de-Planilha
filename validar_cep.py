#validador_cep.py
import requests
import pandas as pd
from utils import somente_digitos
from functools import lru_cache

BRASILAPI_URL_TEMPLATE = "https://brasilapi.com.br/api/cep/v1/{}"

@lru_cache(maxsize=2000)
def validar_cep_simples(raw_cep: str) -> dict:
    resultado = {
        "cep_original": raw_cep,
        "cep_limpo": "",
        "valido": False,
        "logradouro": "",
        "bairro": "",
        "localidade": "",
        "uf": "",
        "erro": None
    }

    if pd.isna(raw_cep) or not str(raw_cep).strip():
        resultado["erro"] = "CEP vazio"
        return resultado

    cep_limpo = somente_digitos(raw_cep)
    resultado["cep_limpo"] = cep_limpo

    if len(cep_limpo) != 8:
        resultado["erro"] = f"CEP deve ter 8 dígitos, mas veio '{raw_cep}'"
        return resultado

    try:
        resp = requests.get(BRASILAPI_URL_TEMPLATE.format(cep_limpo), timeout=5)
        resp.raise_for_status()
        dados = resp.json()
    except Exception as e:
        resultado["erro"] = f"Falha na requisição: {e}"
        return resultado

    resultado.update({
        "valido": True,
        "logradouro": dados.get("street", ""),
        "bairro": dados.get("neighborhood", ""),
        "localidade": dados.get("city", ""),
        "uf": dados.get("state", "")
    })

    return resultado
