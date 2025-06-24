# Validador-de-Planilha
Aplicativo desktop em Python para validação automática de cadastros de parceiros (clientes e fornecedores). Combina regras customizadas de validação de campos, limpeza de dados e consulta de CEP via BrasilAPI, com interface Tkinter e geração de relatórios em Excel.

## Tecnologias e Dependências
- **Python** (>=3.8)
- **Bibliotecas**:
    - `pandas`: manipulação de planilhas e séries de dados
    - `requests`: requisições HTTP para consulta de CEP
    - `tkinter`: construção da interface gráfica (já incluída no Python)
    - `pillow`: exibição e animação e GIFs na GUI
- **Instalação**:
```python
git clone https://github.com/usuario/repo.git
cd repo
pip install pandas requests pillow
```

## Funcionalidades
1. **Validação de Campos**
    - Verifica obrigatoriedade, tipo (`booleano`, `numerico`, `alfanumerico`) e comprimento máximo segundo regras definidas em `regras_validacao.py`.
    - Limpeza de caracteres de pontuação e espaços para contagem correta em campos alfanuméricos (ex.: inscrição estadual).
2. **Limpeza de Dados** (`utils.py`)
    - `limpar_para_contagem(valor: str) -> str`: remove `.`, `-`, `/`, espaços.
    - `somente_digitos(valor: str) -> str`: mantém apenas caracteres de 0 a 9.
3. **Validação de CEP** (`validador_cep.py`)
    - Função `validar_cep_simples(raw_cep: str) -> dict`: retorna dicionário com campos:
          `cep_original`, `cep_limpo`, `valido`(bool), `logradouro`, `bairro`, `localidade`, `uf`, `erro`.
    - Utiliza cache LRU de até 2000 entradas para evitar chamadas repetidas.
    - Consulta `https://brasilapi.com.br/api/cep/v1/{CEP}` com timeout configurável.
4. **Interface Gráfica** (`validador_com_cep.py`)
    - Janela Tkinter com seleção de arquivo Excel/CSV e botões de iniciar/parar.
    - Barra de progresso e contador de registros válidos/invalidos.
    - Animação de logo via GIF (arquivo `futuro_animado.gif`).
    - Multithreading para manter a GUI responsiva durante processamento.
5. **Geração de Relatórios**
    - Diretório `saida/` com:
    -     `dados_validos.xlsx`: registros sem erros.
