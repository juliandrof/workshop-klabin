# Databricks notebook source
# MAGIC %md
# MAGIC # Lab 2 — Transformação com o LakeFlow Designer (low-code)
# MAGIC
# MAGIC O **LakeFlow Designer** é a experiência **visual e sem código** ("Visual data prep")
# MAGIC para preparar e transformar dados no Databricks. Neste lab usamos o **Genie Code** —
# MAGIC uma barra onde você **descreve em português** o que quer e ele monta a transformação.
# MAGIC
# MAGIC > Neste workshop simplificado faremos **uma única transformação**: juntar a produção
# MAGIC > diária (`fato_producao`) com as dimensões de máquinas e produtos e calcular o
# MAGIC > **atingimento da meta**, gerando a tabela **`gold_producao`**.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Abrir o LakeFlow Designer (Visual data prep)
# MAGIC
# MAGIC 1. Na **barra lateral esquerda**, clique no ícone **+ (New)**
# MAGIC 2. Selecione **Visual data prep**
# MAGIC 3. Abre o **canvas** em branco com a tela de boas-vindas
# MAGIC
# MAGIC > O rascunho é salvo automaticamente. Você pode renomeá-lo no topo para
# MAGIC > `visual_prep_klabin_<seu_nome>`.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Adicionar as fontes de dados (operador Source)
# MAGIC
# MAGIC Para cada tabela que você ingeriu no Lab 1:
# MAGIC
# MAGIC 1. Clique em **Select a source** (ou, em **operadores**, no menu da esquerda, escolha **Source**)
# MAGIC 2. Na aba de configuração, escolha **Browse** e selecione a tabela existente em
# MAGIC    `workshop_klabin` > `<seu_nome>`
# MAGIC 3. Repita para as **3 tabelas** de entrada:
# MAGIC    - `fato_producao`
# MAGIC    - `dim_maquinas`
# MAGIC    - `dim_produtos`

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. A transformação — `gold_producao` (com o Genie Code)
# MAGIC
# MAGIC Abra a barra do **Genie Code** no canvas, **cole o prompt abaixo**, use o botão **@**
# MAGIC para mencionar as três tabelas e **aceite** a etapa gerada. Confira a **prévia dos
# MAGIC dados** no painel inferior.
# MAGIC
# MAGIC ```text
# MAGIC A partir de @fato_producao, junte com @dim_maquinas pela coluna id_maquina
# MAGIC (trazendo nome_maquina, unidade e linha) e com @dim_produtos pela coluna
# MAGIC id_produto (trazendo nome_produto, categoria, tipo_fibra e mercado).
# MAGIC Adicione uma coluna atingimento_meta_pct = producao_ton dividido por meta_ton,
# MAGIC multiplicado por 100 e arredondado com 1 casa decimal. Salve o resultado como
# MAGIC gold_producao.
# MAGIC ```
# MAGIC
# MAGIC > Dica: se o resultado não sair como esperado, ajuste o texto do prompt e envie de
# MAGIC > novo — é uma conversa. Você pode iniciar um novo tópico a qualquer momento.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Publicar a saída (operador Output) e executar
# MAGIC
# MAGIC 1. Adicione um operador **Output** ligado ao resultado da transformação
# MAGIC 2. Configure:
# MAGIC    - **Table name**: `gold_producao`
# MAGIC    - **Output location**: catálogo `workshop_klabin` + schema `<seu_nome>`
# MAGIC 3. Clique em **Run** — a execução **cria ou substitui** a tabela gerenciada
# MAGIC
# MAGIC > O Designer mostra o **grafo de linhagem** (lineage) entre as tabelas automaticamente.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Verificação (após executar)
# MAGIC
# MAGIC Execute a célula abaixo (em um cluster comum) para conferir a tabela Gold gerada.

# COMMAND ----------

dbutils.widgets.text("nome_participante", "", "Seu Nome (sem espaços/acentos)")
nome = dbutils.widgets.get("nome_participante").strip().lower().replace(" ", "_")
if nome:
    catalog_name = "workshop_klabin"
    schema_name = nome
    try:
        c = spark.table(f"{catalog_name}.{schema_name}.gold_producao").count()
        print(f"  ✓ gold_producao: {c} registros")
        display(
            spark.table(f"{catalog_name}.{schema_name}.gold_producao")
            .orderBy("id_registro")
            .limit(10)
        )
    except Exception:
        print("  ✗ gold_producao: ainda não criada — rode o pipeline no LakeFlow Designer")
else:
    print("Preencha o widget nome_participante para verificar a tabela.")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Conceitos abordados
# MAGIC - LakeFlow Designer (Visual data prep — low-code / no-code)
# MAGIC - **Genie Code**: construir transformações em linguagem natural (prompts)
# MAGIC - Enriquecimento (join) de fato com dimensões
# MAGIC - Coluna calculada (atingimento de meta)
# MAGIC - Medallion Architecture (camada Gold)
