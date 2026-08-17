# Databricks notebook source
# MAGIC %md
# MAGIC # Lab 3 — Criando e Curando uma Genie Agent
# MAGIC
# MAGIC O **Genie** permite que qualquer pessoa pergunte aos dados em **linguagem natural**
# MAGIC (português!). Neste lab vamos:
# MAGIC 1. Adicionar **comentários** na tabela Gold e nas dimensões (ajudam o Genie a entender os dados)
# MAGIC 2. Criar uma **Genie Agent** com a tabela `gold_producao` e as dimensões
# MAGIC 3. Colar **instruções customizadas** (o segredo de um bom Genie)
# MAGIC 4. Testar com perguntas de negócio

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
# MAGIC ## 1. Comentários nas tabelas (metadados = melhores respostas)
# MAGIC
# MAGIC O Genie usa os **comentários** de tabelas e colunas como contexto. Quanto melhores
# MAGIC os comentários, melhores as respostas. Execute as células abaixo.

# COMMAND ----------

spark.sql(f"""
    COMMENT ON TABLE {catalog_name}.{schema_name}.gold_producao IS
    'Produção diária das máquinas do complexo Klabin de Telêmaco Borba (unidades Monte Alegre e Puma), em toneladas, com energia, paradas, refugo e atingimento de meta'
""")
spark.sql(f"""
    COMMENT ON TABLE {catalog_name}.{schema_name}.dim_maquinas IS
    'Máquinas e linhas de produção (Celulose, Kraftliner, Cartão, Papel para Sacos) por unidade'
""")
spark.sql(f"""
    COMMENT ON TABLE {catalog_name}.{schema_name}.dim_produtos IS
    'Produtos fabricados: celulose (fibra curta/longa/fluff) e papéis, com gramatura e mercado'
""")
print("Comentários de tabela adicionados!")

# COMMAND ----------

comentarios_colunas = [
    ("gold_producao", "producao_ton", "Produção do dia, em toneladas"),
    ("gold_producao", "meta_ton", "Meta de produção do dia, em toneladas"),
    ("gold_producao", "atingimento_meta_pct", "Percentual de atingimento da meta (producao_ton / meta_ton * 100)"),
    ("gold_producao", "consumo_energia_mwh", "Energia consumida na produção do dia, em MWh"),
    ("gold_producao", "paradas_h", "Horas de parada da máquina no dia (24h - tempo de operação)"),
    ("gold_producao", "refugo_ton", "Toneladas de refugo/perda no dia"),
    ("gold_producao", "unidade", "Unidade fabril: Monte Alegre ou Puma"),
    ("gold_producao", "linha", "Linha de produção: Celulose, Kraftliner, Cartão, White Top Kraftliner ou Papel para Sacos"),
]
for tabela, coluna, comentario in comentarios_colunas:
    spark.sql(f"ALTER TABLE {catalog_name}.{schema_name}.{tabela} "
              f"ALTER COLUMN {coluna} COMMENT '{comentario}'")
print("Comentários de coluna adicionados!")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Criar a Genie Agent (na UI)
# MAGIC
# MAGIC 1. Vá em **Genie** (menu lateral) > **New**
# MAGIC 2. **Título**: `Produção Klabin - <seu_nome>`
# MAGIC 3. **Adicione as tabelas**: na aba **Configure**, clique em **Add tables** (seção **Data**),
# MAGIC    navegue no **Catalog** até `workshop_klabin` > `<seu_nome>` e **marque** as 3 tabelas
# MAGIC    abaixo, depois **Confirm**:
# MAGIC    - `gold_producao`
# MAGIC    - `dim_maquinas`
# MAGIC    - `dim_produtos`

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Instruções customizadas do Genie
# MAGIC
# MAGIC Este é o passo mais importante! Execute a célula abaixo e **copie o texto** para o
# MAGIC campo **Instructions** da sua Genie Agent — ele fica dentro da aba **Configure**.

# COMMAND ----------

instrucoes_genie = """
## Contexto do Negócio
Você é um assistente de análise de dados da Klabin, a maior produtora e exportadora de
papéis para embalagens do Brasil e maior fabricante de papel para embalagens do país.
Os dados representam a produção diária das máquinas do complexo de Telêmaco Borba (Paraná),
que reúne a unidade Monte Alegre (máquinas de papel) e a unidade Puma (celulose de mercado
e Puma II). Os produtos incluem celulose de fibra curta (eucalipto), fibra longa (pínus),
fluff, além de kraftliner, white top kraftliner, cartão e papel para sacos.

## Glossário (jargão do setor)
- **Celulose de mercado**: celulose vendida como produto final (fibra curta, longa ou fluff).
- **Fibra curta**: celulose de eucalipto. **Fibra longa**: celulose de pínus.
- **Fluff**: celulose fofa, usada em produtos absorventes (fraldas, higiene).
- **Kraftliner**: papel de alta resistência para a capa de caixas de papelão ondulado.
- **Cartão**: papel de alta gramatura para embalagens (cartuchos, líquidos).
- **Gramatura**: peso do papel por metro quadrado (g/m²).
- **Atingimento de meta**: produção realizada dividida pela meta, em percentual.
- **Refugo**: material perdido/rejeitado no processo produtivo.

## Regras de Resposta
- Sempre expresse produção em **toneladas (t)** e energia em **MWh**, com separador de milhar.
- Percentuais com uma casa decimal (ex.: 96,5%).
- Quando perguntarem por "maior produção", use a soma de `producao_ton` como métrica padrão.
- "Atingimento da meta" = coluna `atingimento_meta_pct` de gold_producao.
- Ao comparar Monte Alegre e Puma, deixe claro que Puma concentra a celulose de mercado.

## Exemplos de Perguntas
- "Qual máquina produziu mais no período?"
- "Qual o atingimento médio da meta por unidade?"
- "Compare a produção de celulose com a de papel."
- "Qual produto teve mais refugo?"
- "Qual o consumo total de energia por linha de produção?"
"""

print("=" * 70)
print("INSTRUÇÕES PARA A GENIE AGENT (copie e cole no campo 'Instructions')")
print("=" * 70)
print(instrucoes_genie)
print("=" * 70)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Testar o Genie
# MAGIC
# MAGIC Após criar a Genie Agent, teste com perguntas como:
# MAGIC
# MAGIC 1. **"Qual máquina produziu mais no período?"**
# MAGIC 2. **"Qual o atingimento médio da meta por unidade?"**
# MAGIC 3. **"Compare a produção de celulose com a de papel"**
# MAGIC 4. **"Qual produto teve mais refugo?"**
# MAGIC 5. **"Qual o consumo total de energia por linha de produção?"**
# MAGIC
# MAGIC Cadastre 3–5 dessas perguntas como **Sample Questions** para orientar os usuários.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Próximo passo
# MAGIC
# MAGIC Siga para o **Lab 4 — AI/BI Dashboard** para criar um painel de produção
# MAGIC **inteiramente via prompt**, com as cores da Klabin.
