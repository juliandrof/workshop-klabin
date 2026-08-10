# Databricks notebook source
# MAGIC %md
# MAGIC # Lab 1 — Validação da Ingestão
# MAGIC
# MAGIC Depois de fazer o upload manual dos 3 arquivos para o seu schema
# MAGIC (veja `01a_guia_upload_dados.py`), execute este notebook para conferir se tudo
# MAGIC foi ingerido corretamente.

# COMMAND ----------

dbutils.widgets.text("nome_participante", "", "Seu Nome (sem espaços/acentos)")

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
# MAGIC ## 1. Conferir se as 3 tabelas existem e têm dados

# COMMAND ----------

esperado = {
    "fato_producao": 810,   # 90 dias x 9 máquinas
    "dim_maquinas": 9,
    "dim_produtos": 7,
}

print(f"\n{'='*60}")
print(f"VALIDAÇÃO — {catalog_name}.{schema_name}")
print(f"{'='*60}")
tudo_ok = True
for tabela, qtd_esperada in esperado.items():
    try:
        c = spark.table(f"{catalog_name}.{schema_name}.{tabela}").count()
        status = "✓" if c == qtd_esperada else "⚠"
        if c != qtd_esperada:
            tudo_ok = False
        print(f"  {status} {tabela}: {c} linhas (esperado ~{qtd_esperada})")
    except Exception:
        tudo_ok = False
        print(f"  ✗ {tabela}: NÃO ENCONTRADA — faça o upload deste arquivo")
print(f"{'='*60}")
print("Tudo certo! Siga para o Lab 2." if tudo_ok else
      "Revise os uploads faltantes/divergentes antes de seguir.")
print(f"{'='*60}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Amostra da tabela fato (`fato_producao`)

# COMMAND ----------

display(
    spark.table(f"{catalog_name}.{schema_name}.fato_producao")
    .orderBy("id_registro")
    .limit(10)
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Conferir os tipos de coluna
# MAGIC
# MAGIC A UI de Create table infere os tipos automaticamente. Confirme que colunas numéricas
# MAGIC (como `producao_ton`, `consumo_energia_mwh`) vieram como número, e datas/textos como
# MAGIC string. No Lab 2 faremos o enriquecimento com o LakeFlow Designer.

# COMMAND ----------

for tabela in esperado:
    try:
        print(f"\n--- {tabela} ---")
        spark.table(f"{catalog_name}.{schema_name}.{tabela}").printSchema()
    except Exception:
        print(f"  ({tabela} ainda não existe)")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Próximo passo
# MAGIC
# MAGIC Com as tabelas ingeridas, siga para o **Lab 2 — Transformação** usando o
# MAGIC **LakeFlow Designer** para construir a tabela Gold de produção.
