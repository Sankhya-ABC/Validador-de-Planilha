#regra_validacao.py
import pandas as pd
import re
from utils import limpar_para_contagem, somente_digitos

REGRAS = {
    "COD_SIST_ANTERIOR":           {"obrigatorio": False, "tipo": "alfanumerico", "max_tamanho": None},
    "CLIENTE":                     {"obrigatorio": True,  "tipo": "booleano",   "max_tamanho": None},
    "FORNECEDOR":                  {"obrigatorio": True,  "tipo": "booleano",   "max_tamanho": None},
    "RAZAO_SOCIAL":                {"obrigatorio": False, "tipo": "alfanumerico", "max_tamanho": 80},
    "NOME_FANTASIA":               {"obrigatorio": True,  "tipo": "alfanumerico", "max_tamanho": 80},
    "CNPJ_CPF":                    {"obrigatorio": True,  "tipo": "alfanumerico",    "max_tamanho": 14},
    "INSCR_ESTAD/IDENTIDADE":      {"obrigatorio": False, "tipo": "alfanumerico",    "max_tamanho": 16},
    "CEP":                         {"obrigatorio": False, "tipo": "numerico",    "max_tamanho": 8},
    "TIPO_LOGRADOURO":             {"obrigatorio": False, "tipo": "alfanumerico", "max_tamanho": 8},
    "ENDERECO":                    {"obrigatorio": False, "tipo": "alfanumerico", "max_tamanho": 60},
    "NRO_END":                     {"obrigatorio": False, "tipo": "alfanumerico",    "max_tamanho": 6},
    "COMPLEMENTO":                 {"obrigatorio": False, "tipo": "alfanumerico", "max_tamanho": 30},
    "BAIRRO":                      {"obrigatorio": False, "tipo": "alfanumerico", "max_tamanho": 50},
    "CIDADE":                      {"obrigatorio": False, "tipo": "alfanumerico", "max_tamanho": 50},
    "UF":                          {"obrigatorio": False, "tipo": "alfanumerico", "max_tamanho": 2},
    "EMAIL":                       {"obrigatorio": False, "tipo": "alfanumerico", "max_tamanho": 80},
    "TELEFONE":                    {"obrigatorio": False, "tipo": "numerico",    "max_tamanho": 13},
    "LIMITE_CREDITO":              {"obrigatorio": False, "tipo": "numerico",    "max_tamanho": None},
    "OBSERVACOES":                 {"obrigatorio": False, "tipo": "alfanumerico", "max_tamanho": 4000},
    "CEP_ENTREGA":                 {"obrigatorio": False, "tipo": "numerico",    "max_tamanho": 8},
    "TIPO_LOGRADOURO_ENTREGA":     {"obrigatorio": False, "tipo": "alfanumerico", "max_tamanho": 8},
    "ENDERECO_ENTREGA":            {"obrigatorio": False, "tipo": "alfanumerico", "max_tamanho": 60},
    "NRO_END_ENTREGA":             {"obrigatorio": False, "tipo": "alfanumerico",    "max_tamanho": 6},
    "COMPLEMENTO_ENTREGA":         {"obrigatorio": False, "tipo": "alfanumerico", "max_tamanho": 30},
    "BAIRRO_ENTREGA":              {"obrigatorio": False, "tipo": "alfanumerico", "max_tamanho": 50},
    "CIDADE_ENTREGA":              {"obrigatorio": False, "tipo": "alfanumerico", "max_tamanho": 50},
    "UF_ENTREGA":                  {"obrigatorio": False, "tipo": "alfanumerico", "max_tamanho": 2},
}

def extrair_regras_do_apoio() -> dict:
    return {col: dict(props, coluna=col.lower()) for col, props in REGRAS.items()}

def validar_campo(valor, regra: dict) -> (bool, str):
    obrig = regra["obrigatorio"]
    tipo = regra["tipo"]
    max_tam = regra["max_tamanho"]
    col   = regra["coluna"]

    if obrig and (pd.isna(valor) or not str(valor).strip()):
        return False, "Campo obrigatório não preenchido"

    if pd.isna(valor) or not str(valor).strip():
        return True, ""

    txt = str(valor).strip()

    if col == "inscr_estad/identidade":
        txt = limpar_para_contagem(txt)

    if tipo == "booleano":
        if not re.fullmatch(r"[SsNn]", txt):
            return False, f"Esperado 'S' ou 'N', veio '{txt}'"

    elif tipo == "numerico":
        digits = somente_digitos(txt)
        if not digits.isdigit():
            return False, f"Esperado somente dígitos, veio '{txt}'"
        if max_tam and len(digits) > max_tam:
            return False, f"Dígitos = {len(digits)}, máximo {max_tam}"

    else: 
        length = len(txt)
        if max_tam and length > max_tam:
            return False, f"Tamanho = {length}, máximo {max_tam}"

    return True, ""

def validar_linha(row: pd.Series, regras: dict) -> list:
    erros = []
    for col, regra in regras.items():
        if col not in row.index:
            erros.append(f"{col}: coluna ausente")
            continue
        ok, msg = validar_campo(row[col], regra)
        if not ok:
            erros.append(f"{col}: {msg}")
    return erros
