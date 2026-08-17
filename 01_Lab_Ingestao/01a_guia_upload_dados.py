# Databricks notebook source
# MAGIC %md
# MAGIC # Lab 1 — Ingestão de Dados (guia de upload manual)
# MAGIC
# MAGIC Neste lab vamos ingerir os dados fazendo o **upload manual** dos arquivos da pasta
# MAGIC `dados/` — sem escrever código. É a forma mais simples e comum de trazer planilhas e
# MAGIC extrações (CSV/Excel) para o Databricks.
# MAGIC
# MAGIC > **Destino:** todas as tabelas vão para o **seu schema pessoal** dentro do catálogo
# MAGIC > compartilhado: `workshop_klabin.<seu_nome>`.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Arquivos que vamos ingerir
# MAGIC
# MAGIC A pasta `dados/` do repositório contém 3 tabelas — a **fato em CSV** e as
# MAGIC **dimensões em Excel (XLSX)** — modelando a produção de celulose e papel do
# MAGIC complexo de **Telêmaco Borba (PR)**: unidade **Monte Alegre** e unidade **Puma**.
# MAGIC
# MAGIC | Arquivo | Formato | Tipo | Descrição |
# MAGIC | -- | -- | -- | -- |
# MAGIC | `fato_producao.csv` | CSV | **Fato** | Produção diária por máquina (toneladas, energia, paradas, refugo) |
# MAGIC | `dim_maquinas.xlsx` | XLSX | Dimensão | Máquinas e linhas de produção (Celulose, Kraftliner, Cartão, Sacos) |
# MAGIC | `dim_produtos.xlsx` | XLSX | Dimensão | Produtos: celulose (fibra curta/longa/fluff) e papéis (gramatura, mercado) |

# COMMAND ----------

# MAGIC %md
# MAGIC ## Passo a passo — Catalog > Create table (Upload files)
# MAGIC
# MAGIC Repita para **cada um dos 3 arquivos**:
# MAGIC
# MAGIC 1. No menu lateral, abra **Catalog**
# MAGIC 2. Navegue até o catálogo `workshop_klabin` > seu schema **`<seu_nome>`**
# MAGIC 3. Clique em **Create** > **Create table** (ou **Add data** > **Create or modify table**)
# MAGIC 4. **Arraste o arquivo** (ex.: `fato_producao.csv`) ou clique para selecioná-lo
# MAGIC 5. Confira a prévia:
# MAGIC    - **Catalog**: `workshop_klabin`
# MAGIC    - **Schema**: `<seu_nome>`
# MAGIC    - **Table name**: use o nome do arquivo sem a extensão (ex.: `fato_producao`)
# MAGIC    - **First row contains header**: ativado — para o **CSV** (`fato_producao`) essa opção fica em **Advanced attributes** (expanda a seção); nos **XLSX** das dimensões o cabeçalho já é detectado
# MAGIC    - Confira os tipos de coluna sugeridos (número vs texto)
# MAGIC 6. Clique em **Create table**
# MAGIC
# MAGIC > **Dica:** a UI de Create table aceita **CSV e XLSX**. Para os arquivos Excel
# MAGIC > (`.xlsx`), a primeira planilha (`Dados`) é usada automaticamente.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Tabelas esperadas ao final
# MAGIC
# MAGIC Depois de subir os 3 arquivos, o seu schema deve conter:
# MAGIC
# MAGIC ```
# MAGIC workshop_klabin.<seu_nome>.fato_producao
# MAGIC workshop_klabin.<seu_nome>.dim_maquinas
# MAGIC workshop_klabin.<seu_nome>.dim_produtos
# MAGIC ```
# MAGIC
# MAGIC > Use o notebook **`01b_validacao.py`** para conferir se todas as tabelas foram
# MAGIC > criadas corretamente antes de seguir para o Lab 2.
