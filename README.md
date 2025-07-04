# Validador de Cadastro de Parceiros
Este é um aplicativo desktop desenvolvido em Python para validar planilhas de cadastro de parceiros (clientes/fornecedores) de acordo com regras específicas. O sistema verifica cada linha do arquivo de entrada (Excel), aplica regras de validação, valida CEPs via API e gera três arquivos de saída: válidos, inválidos (com mensagens de erro) e resultados da validação de CEP.

## Funcionalidades Principais
- Validação de planilhas de parceiros (Excel)
- Validação de CEP em tempo real via BrasilAPI
- Preenchimento automático de endereço a partir do CEP
- Intergace gráfica amigável com logo animado
- Barra de progresso em tempo real
- Botão de cancelamento durante a execução
- Geração de relatórios de validação

## Requisitos do Sistema
- Python 3.8 ou superior
- Bibliotecas Python:
```python
pip install pandas, tkinter, pillow, openpyxl, requests
```

## Como Usar
### Execução do Programa
1. Clone o repositório ou faça download dos arquivos
2. Execute o arquivo principal:
```python
python validador_com_cep.py
```
### Interface Gráfica
1. Seleção de Arquivo:
    - Clique em "Procurar" para selecionar um arquivo Excel
    - O caminho do arquivo aparecerá no campo de texto
2. Validação:
    - Clique em "Executar Validação" para iniciar o processo
    - A barra de progresso mostrará o andamento
    - O contador exibirá linhas processadas e inválidas
3. Cancelamento:
    - Clique em "Parar" para interromper a validação a qualquer momento
4. Resultados:
    - Após a conclusão, uma mensagem mostrará estatpisticas
    - Os arquivos de saída serão salvos na pasta `saida/`:
        - `dados_validos.xlsx`: Parceiros sem erros
        - `dados_invalidos.xlsx`: Parceiros com erros e mensagens de validação
        - `validacao_cep.xlsx`: Resultados detalhados da validação de CEP

### Preparação da Planilha
A planilha de entrada deve conter uma aba chamada "Infos" com as seguintes colunas:
| Coluna | Obrigatório | Tipo | Tamanho | Descrição |
| ------ | :-----------: | ---- | :-------: | --------- |
| COD_SIST_ANTERIOR       | NÃO | Alfanumérico | -    | Código do sistema anterior |
| CLIENTE                 | SIM | Booleano     | -    | 'S' ou 'N'                 |
| FORNECEDOR              | SIM | Booleano     | -    | 'S' ou 'N'                 |
| RAZAO_SOCIAL            | NÃO | Alfanumérico | 80   | -                          |
| NOME_FANTASIA           | SIM | Alfanumérico | 80   | -                          |
| CNPJ_CPF                | SIM | Alfanumérico | 14   | -                          |
| INSCR_ESTAD/IDENTIDADE  | NAO | Alfanumérico | 16   | -                          |
| CEP                     | NÃO | Numérico     | 8    | -                          |
| TIPO_LOGRADOURO         | NAO | Alfanumérico | 8    | -                          |
| ENDERECO                | NÃO | Alfanumérico | 60   | -                          | 
| NRO_END                 | NÃO | Alfanumérico | 6    | -                          |
| COMPLEMENTO             | NÃO | Alfanumérico | 30   | -                          |
| BAIRRO                  | NÃO | Alfanumérico | 50   | -                          |
| CIDADE                  | NÃO | Alfanumérico | 50   | -                          |
| UF                      | NÃO | Alfanumérico | 2    | -                          |
| EMAIL                   | NÃO | Alfanumérico | 80   | -                          |
| TELEFONE                | NÃO | Numérico     | 13   | -                          |
| LIMITE_CREDITO          | NÃO | Numérico     | -    | -                          |
| OBSERVAÇÕES             | NÃO | Alfanumérico | 4000 | -                          |
| CEP_ENTREGA             | NÃO | Numérico     | 8    | -                          |
| TIPO_LOGRADOURO_ENTREGA | NAO | Alfanumérico | 8    | -                          |
| ENDERECO_ENTREGA        | NÃO | Alfanumérico | 60   | -                          | 
| NRO_END_ENTREGA         | NÃO | Alfanumérico | 6    | -                          |
| COMPLEMENTO_ENTREGA     | NÃO | Alfanumérico | 30   | -                          |
| BAIRRO_ENTREGA          | NÃO | Alfanumérico | 50   | -                          |
| CIDADE_ENTREGA          | NÃO | Alfanumérico | 50   | -                          |
| UF_ENTREGA              | NÃO | Alfanumérico | 2    | -                          |

## Descrição dos Arquivos
### validador_com_cep.py
Arquivo principal que contém a interface gráfica e a lógica de controle.

**Principais componentes**:
- `ValidadorApp`: Classe principal da aplicação
    - `__init__`: Inicializa a interface
    - `_build_widgets_`: Constrói os elementos da interface
    - `_load_gif_logo`: Carrega e anima o logo
    - `_run_validation`: Lógica principal de validação
    - `_start_validation`: Inicia a validação em thread separada

**Fluxo de validação**:
1. Seleção do arquivo de entrada
2. Leitura da aba "Infos"
3. Validação linha por linha:
    - Aplica regras de validalção
    - Valida CEP via API
    - Preenche endereço automaticamente (se CEP válido)
4. Geração de arquivos de saída
5. Exibição de estatísticas

### validar_cep.py
Responsável pela validação de CEPs usando a BrasilAPI.

**Funções**:
- `validar_cep_simples(raw_cep: str) → dict`:
    - Limpa o CEP (remove não dígitos)
    - Verifica se tem 8 dígitos
    - Consulta a API (com cache)
    - Retorna dicionário com resultados

### utils.py
Funções utilitárias para tratamento de texto.

**Funções**:
- `limpar_para_contagem(valor: str) → str`:
    - Remove pontuação e espaços
- `somente_digitos(valor: str) → str`:
    - Remove tudo que não for dígito

### regra_validacao.py
Contém as regras de validação e funções auxiliares.

**Componentes principais**:
- `REGRAS`: Dicionáirio com todas as regras de validação
- `extrair_regras_do_apoio`: Retorna regras formatadas
- `validar_campo`: Valida um campo individual
- `validar_linha`: Valida uma linha completa

## Regras de Validação Detalhadas
### Campos Booleanos (CLIENTE, FORNECEDOR)
1. Deve conter 'S' ou 'N' (maiúsculo ou minúsculo)
2. Campo obrigatório

### Campos Numéricos
1. Deve conter apenas dígitos
2. Tamanho máximo em dígitos
3. CEPs devem ter exatamente 8 dígitos

### Campos Alfanuméricos
1. Verificação de tamanho máximo (após remoção de espaços extras)
2. Campos obrigatórios não podem estar vazios

### Validação Especial do CEP
1. Remove não dígitos
2. Verifica se tem 8 dígitos
3. Consulta API para validar e obter endereço
4. Atualiza automaticamente:
    - BAIRRO
    - CIDADE
    - UF

## Fluxo de Trabalho Recomendado
1. Prepare sua planilha na aba "Infos"
2. Execute o validador
3. Analise o arquivo `dados_invalidos.xlsx`
4. Corrija os erros indicados na coluna "OBS_Validação"
5. Use o arquivo `dados_validos.xlsx` em seus sistemas
6. Consulte `validacao_cep.xlsx` para detalhes de CEPs

## Notas Importantes
1. A planilha de entrada deve ter a aba exatamente nomeada "Infos"
2. Colunas ausentes serão consideradas como erro
3. O sistema usa cache para consultas de CEP (evita repetições)
4. Aquivos de saída são sobrescritos a cada execução

## Limitações Conhecidas
1. Só processa a primeira aba do Excel (chamada "Infos")
2. Arquivos muito grandes (> 10.000 linhas) podem demorar devido à API de CEP
3. Não suporta validação assíncrona de CEPs (pode ser lento)

## Exemplo de Saída
**dados_invalidos.xlsx**:
| NOME_FANTASIA | CNPJ_CPF | ... | OBS_Validação |
| ------------- | -------- | --- | ------------- |
| Empresa A     | 12.345.678/0001-99 | ... | CNPJ_CPF: Dígitos = 14, máximo 14, CLIENTE: Esperado 'S' ou 'N', veio 'X' |
| Empresa B     | 12345678901234     | ... | FORNECEDOR: Campo obrigatório não preenchido |

**validacao_cep.xlsx**:
| cep_original | cep_limpo | valido | logradouro | ... | erro |
| ------------ | --------- | ------ | ---------- | --- | ---- |
| 01001-000    | 010010000 | Sim    | Praça da Sé | ... | -   |
| 0000000      | 0000000   | Não    | -           | ... | CEP deve ter 8 dígitos, veio 7 |

