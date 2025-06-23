#utils.py
import re
import pandas as pd

def limpar_para_contagem(valor: str) -> str:
    if pd.isna(valor):
        return ""
    texto = str(valor).strip()
    return re.sub(r"[.\-/\s]", "", texto)

def somente_digitos(valor: str) -> str:
    if pd.isna(valor):
        return ""
    texto = str(valor)
    return re.sub(r"\D", "", texto)
