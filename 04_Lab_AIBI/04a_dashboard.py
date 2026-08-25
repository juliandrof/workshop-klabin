# Databricks notebook source
# MAGIC %md
# MAGIC # Lab 4 — AI/BI Dashboard criado **inteiramente via prompt**
# MAGIC
# MAGIC Neste lab final vamos construir **um painel padrão de produção** para todos os
# MAGIC participantes — o mesmo dashboard, criado do zero **usando apenas linguagem natural**
# MAGIC (sem arrastar widget por widget). A IA do AI/BI monta os gráficos a partir do seu prompt.
# MAGIC
# MAGIC > O objetivo é todo mundo sair com o **mesmo dashboard de referência**, nas
# MAGIC > **cores da Klabin**, e entender como gerar visualizações por prompt.

# COMMAND ----------

dbutils.widgets.text("nome_participante", "", "Nome no formato nome_sobrenome (ex.: joao_silva)")

# COMMAND ----------

nome = dbutils.widgets.get("nome_participante").strip().lower().replace(" ", "_")
assert nome != "", "Por favor, preencha seu nome no widget acima!"
catalog_name = "workshop_klabin"
schema_name = nome
spark.sql(f"USE CATALOG {catalog_name}")
spark.sql(f"USE SCHEMA {schema_name}")
print(f"Usando: {catalog_name}.{schema_name}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Validar a tabela Gold antes de montar o dashboard

# COMMAND ----------

display(spark.sql(f"""
    SELECT
        ROUND(SUM(producao_ton), 1)          AS producao_total_ton,
        COUNT(DISTINCT nome_maquina)         AS maquinas_ativas,
        ROUND(AVG(atingimento_meta_pct), 1)  AS atingimento_medio_pct,
        ROUND(SUM(consumo_energia_mwh), 1)   AS energia_total_mwh
    FROM {catalog_name}.{schema_name}.gold_producao
"""))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Criar o Dashboard e abrir o Genie Code
# MAGIC
# MAGIC 1. Vá em **Dashboards** > **Create dashboard**
# MAGIC 2. **Nome**: `Dashboard Produção Klabin - <seu_nome>`
# MAGIC 3. Na aba **Data**, adicione a tabela `workshop_klabin.<seu_nome>.gold_producao`
# MAGIC    como dataset (ou cole `SELECT * FROM workshop_klabin.<seu_nome>.gold_producao`)
# MAGIC 4. Na aba **Untitled** (a página inicial do dashboard), abra o **Genie Code** e
# MAGIC    **cole o prompt padrão** da próxima célula. A IA vai gerar todos os widgets.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. O prompt padrão do dashboard (copie e cole no Genie Code)
# MAGIC
# MAGIC Execute a célula abaixo para imprimir o prompt completo. **Cole exatamente esse texto**
# MAGIC no Genie Code do dashboard — ele descreve os gráficos, a ordem e as **cores da Klabin**.

# COMMAND ----------

# Paleta de cores da Klabin (usada no prompt do dashboard)
# Verde Klabin (primário) -> tons de verde -> kraft/papel (marrom) -> neutros
PALETA_KLABIN = {
    "verde_primario":  "#00843D",   # verde Klabin
    "verde_escuro":    "#004B23",
    "verde_claro":     "#7AB800",
    "kraft":           "#B07A3E",   # tom de papel kraft
    "cinza":           "#6E6E6E",
    "areia":           "#E8DFCF",
}

prompt_dashboard = f"""
Crie um dashboard de produção industrial para a Klabin (complexo de Telêmaco Borba, PR),
usando o dataset gold_producao. Título do dashboard: "Produção Klabin — Telêmaco Borba".

Use SEMPRE esta paleta de cores da Klabin, nesta ordem de prioridade:
- Verde primário {PALETA_KLABIN['verde_primario']}
- Verde escuro {PALETA_KLABIN['verde_escuro']}
- Verde claro {PALETA_KLABIN['verde_claro']}
- Kraft (marrom papel) {PALETA_KLABIN['kraft']}
- Cinza {PALETA_KLABIN['cinza']}
- Areia {PALETA_KLABIN['areia']}

Monte os seguintes widgets, nesta ordem:

1. Uma linha com 4 indicadores (counters) no topo:
   - Produção total (soma de producao_ton), em toneladas
   - Máquinas ativas (contagem distinta de nome_maquina)
   - Atingimento médio da meta (média de atingimento_meta_pct), em %
   - Energia total consumida (soma de consumo_energia_mwh), em MWh

2. Um gráfico de rosca (donut) com a participação da produção total (producao_ton)
   por categoria de produto (Celulose vs Papel). Use o verde primário e o kraft.

3. Um gráfico de barras horizontais com a produção total (producao_ton) por
   nome_maquina, ordenado do maior para o menor, colorido em verde primário.

4. Um gráfico de barras com a produção total (producao_ton) por unidade
   (Monte Alegre e Puma), colorido com verde escuro e verde claro.

5. Um gráfico de linha com a produção diária total (soma de producao_ton por data),
   mostrando a evolução ao longo do tempo, na cor verde primário.

6. Uma tabela com: nome_maquina, unidade, linha, produção total (producao_ton),
   atingimento médio da meta (atingimento_meta_pct) e refugo total (refugo_ton),
   ordenada pela maior produção.

Adicione filtros (por unidade, por categoria de produto e por período/data) para tornar
o painel interativo. Formate produção em toneladas e energia em MWh com separador de
milhar, e percentuais com uma casa decimal.
"""

print("=" * 72)
print("PROMPT PADRÃO DO DASHBOARD (copie e cole no Genie Code do AI/BI)")
print("=" * 72)
print(prompt_dashboard)
print("=" * 72)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Refinar por prompt (opcional)
# MAGIC
# MAGIC Depois de gerar o painel, você pode continuar conversando com o Genie Code para ajustar,
# MAGIC **sempre por prompt**. Exemplos:
# MAGIC
# MAGIC - *"Troque o gráfico de produção por máquina para mostrar também a meta lado a lado."*
# MAGIC - *"Adicione um card com o produto de maior refugo."*
# MAGIC - *"Deixe o fundo dos títulos em verde {PALETA_KLABIN['verde_primario']}."*
# MAGIC
# MAGIC > Todos terminam com o **mesmo dashboard de referência**, nas cores da Klabin — o
# MAGIC > foco é aprender a criar e ajustar visualizações **por linguagem natural**.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Parabéns! Workshop Concluído!
# MAGIC
# MAGIC Você completou os 4 labs do Workshop Klabin:
# MAGIC
# MAGIC - **Lab 1** — Ingestão: upload manual de CSV/XLSX → camada Bronze
# MAGIC - **Lab 2** — Transformação: LakeFlow Designer (uma transformação → `gold_producao`)
# MAGIC - **Lab 3** — Genie Agent: análise da produção em linguagem natural
# MAGIC - **Lab 4** — AI/BI Dashboard: painel padrão criado **inteiramente via prompt**
