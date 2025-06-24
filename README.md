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
    - `dados_validos.xlsx`: registros sem erros.
    - `dados_invalidos.xlsx`: registros com lista de erros na coluna `OBS_Validação`.
    - `validacao_cep.xlsx`: detalhes da validação de CEP para cada registro.

## Estrutura de Arquivos
```python
├── regra_validacao.py                # def. regras e funçõs de validação de campos
├── utils.py                          # funções de limpeza de texto e extração de dígitos
├── validador_cep.py                  # validação de CEP via BrasilAPI e cache LRU
├── validador_com_cep.py              # interface Tkinter e fluxo de validação completo
├── futuro_animado.gif                # GIF para animação do logo
└── saida/                            # pasta criada após execução, com resultados
    ├── dados_validos.xlsx
    ├── dados_invalidos.xlsx
    └── validacao_cep.xlsx
```

## Descrição Detalhada dos Scripts
### 1.regra_validacao.py
- `**REGRAS**`: dicionário que define para cada coluna:
    - `obrigatorio`: se o campo deve ser preenchido.
    - `tipo`: `booleano`, `numerico` ou `alfanumerico`.
    - `max_tamanho`: comprimento máximo (ou `None`).
- `**extrair_regras_do_apoio()**`: retorna cópia das `REGRAS` incluindo chave `coluna` em lowercase.
- `**validar_campo(valor, regra)**`:
    1. Verifica obrigatoriedade.
    2. Ignora campos vaxios não obrigatórios.
    3. Limpa pontuação para inscrição estadual.
    4. Valida tipo e tamanho.
    5. Retorna `(True, "")` se ok, ou `(False, mensagem)`.
- `validar_linha(row: pd.Series, regras)`: faz loop por cada regra, aplica `validar_campo` e acumula erros.
### 2.utils.py
- `limpar_para_contagem(valor)`: usa regex para remover `.`, `-`, `/`, espaços.
- `somente_digitos(valor)`: usa regex para extrair apenas dígitos.
### 3.validador_cep.py
- Constante: `BRASILAPI_URL_TEMPLATE` com endpoint BrasilAPI.
- `@lru_cache(maxsize=2000)` em `validar_cep_simples(raw_cep)` para acelerar múltiplas chamadas.
- Fluxo:
    1. Normalize e valida formato (8 dígitos).
    2. Realiza `GET` na API com `requests`.
    3. Popula resultado com campos de endereço ou mensagem de erro.
### 4.validador_com_cep.py
- Classe `ValidadorApp`:
    - Contrói janela principal, frames, botões e estilos.
    - Carrega e anima logo GIF.
    - Métodos de seleção de arquivo, iniciar/parar validação.
    - `_run_validation`:
    - 1. Lê planilha (`sheet_name="Infos"`).
      2. Para cada linha, aplica limpeza e validação de campos.
      3. 












