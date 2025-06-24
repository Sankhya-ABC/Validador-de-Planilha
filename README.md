# Validador-de-Planilha
Um aplicativo desktop em Python que valida cadastros de parceiros (clientes e fornecedores), garantindo conformidade de campos e integridade de dados via regras customizadas e consulta de CEP.

## Tecnologias e Dependências
- **Python** (>= 3.8)
- **Bibliotecas**:
    - pandas: manipulação de dados
    - requests: requisições HTTP
    - tkinter: GUI (incluso no Python)
    - pillow: manipulação de imagens (GIF/logo animado)

**Instalação**:
```python
    pip install pandas requests pillow
```

## Funcionalidades
1. **Validação de Campos**
    - Checa obrigatoriedade `(obrigatorio)`, tipo `(booleano, numerico, alfanumerico)` e tamanho máximo `(max_tamanho)`.
    - Campos com pontuação são limpos antes de contar (ex.: INSCR_ESTAD/IDENTIDADE).
2. **Limpeza de Dados (utils.py)**
    - `limpar_para_contagem(valor)`: remove `.`, `-`, `/`, espaços
    - `somente_digitos(valor)`: extrai apenas dígitos
3. **Validação de CEP**
    - Consulta BrasilAPI via `https://brasilapi.com.br/api/cep/v1/{CEP}`.
    - Cache LRU (até 2000 resultados) para performance.
    - Preenche automaticamente `BAIRRO`, `CIDADE` E `UF` quando CEP válido.
4. **Interface Gráfica**
    - Seleção de arquivos Excel/CSV (.xlsx ou .csv) na aba `Infos`.
    - Barra de progresso com contagem de linhas válidas/invalidas.
    - Botão de cancelamento para interromper processo.
    - Logo animado (GIF) opcional.
5. **Relatórios de Saída** (pasta `saida/`)
    - `dados_validos.xlsx`: registro sem erros.
    - `dados_invalidos.xlsx`: registros com descrição dos erros em `OBS_Validação`.
    - `validacao_cep.xlsx`: detalhes da consulta de CEP (cep_original, cep_limpo, valido, logradouro, bairro, localidade, uf, erro).

## Estrutura de Arquivos
```python
├── regra_validacao.py             # Definição de regras e validação de campos
├── utils.py                       # Funções auxiliares de limpeza e extração
├── validador_cep.py               # Consulta e validação de CEP via BrasilAPI
├── validador_com_cep.py           # Aplicativo GUI que orquestra validações
├── futuro_animado.gif             # GIF opcional para animação do logo
└── saida/                         # Diretório gerado após execução
    ├── dados_validos.xlsx
    ├── dados_invalidos.xlsx
    └── validacao_cep.xlsx
```

## Como Executar
1. Preparar Arquivo de Entrada
    - Formato Excel (`.xlsx`) ou CSV.
    - Aba chamada `Infos` (apenas no caso do Excel).
    - Colunas obrigatórias conforme `REGRAS` em `regra_validacao.py`.
2. Executar Aplicação
```python
    python validador_com_cep.py
```
3. Selecionar Arquivo
    - Clique em **Procurar**, escolha o arquivo e clique em **Executar Validação**.
4. Monitorar Progresso
    - Acompanhe a barra e o texto que informa linhas processadas e inválidas.
    - Para interromper, clique em **Parar**.
5. Verificar Saída
    - Abra os arquivos gerados na pasta `saida/`.
  
## Exemplo de Uso
Suponha um arquivo `cadastro.xlsx` com aba `Infos`. Após seleção e execução:
- Linhas sem inconsistências vão para `saida/dados_validos.xlsx`.
- Linhas com erros (tipo, falta de dado obrigatório, comprimento excedido) vão para `saida/dados_invalidos.xlsx`, coluna `OBS_Validação` detalha cada erro.
- Consulta de CEP em `saida/validacao_cep.xlsx` informando resultado e preenchendo endereço quando possível.

## Personalizações
- **Regras de Validação**: modifique o dicionário `REGRAS` em `regra_validacao.py` (adicione campos, ajuste `max_tamanho`, `tipo` ou `obrigatorio`).
- **GUI**: em `validador_com_cep.py`, altere cores, fontes, layout e tempo de animação.
- **Cache/Timeout CEP**: ajuste `@lru_cache(maxsize=...)` ou `timeout` da requisição em `validador_cep.py`.
