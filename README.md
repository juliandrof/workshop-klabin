# Workshop Hands-On Databricks | Klabin

Workshop prático de Databricks personalizado para o time da **Klabin**, com foco em
**low-code**: Ingestão, Transformação de Dados, consumo em Linguagem Natural e Visualização —
a **Data + AI Platform** de ponta a ponta.

</br>

## Apresentadores

<table>
  <tr>
    <td align="center" width="33%">
      <img src="https://raw.githubusercontent.com/juliandrof/workshop-klabin/main/images/juliandro_circle.png" width="150"/><br>
      <strong>Juliandro Figueiró</strong><br>
      <em>Sr. Solutions Architect</em><br>
      <em>Databricks</em>
    </td>
    <td align="center" width="33%">
      <img src="https://raw.githubusercontent.com/juliandrof/workshop-klabin/main/images/jean_circle.png" width="150"/><br>
      <strong>Jean Ertzogue</strong><br>
      <em>Account Executive</em><br>
      <em>Databricks</em>
    </td>
    <td align="center" width="33%">
      <img src="https://raw.githubusercontent.com/juliandrof/workshop-klabin/main/images/marcio_circle.png?v=2" width="150"/><br>
      <strong>Marcio Arbex</strong><br>
      <em>Field Engineering Director</em><br>
      <em>Databricks</em>
    </td>
  </tr>
</table>

</br>

## Ementa do Workshop (2 horas)

| # | Lab | Tópicos | Duração |
| -- | -- | -- | -- |
| 00 | **Setup** | Catálogo compartilhado `workshop_klabin` + schema pessoal (seu nome) | 10 min |
| 01 | **Ingestão de Dados** | Upload manual de arquivos (CSV + Excel) via Catalog (Create table), camada Bronze | 25 min |
| 02 | **Transformação — LakeFlow Designer** | Visual data prep (no-code): **uma** transformação → `gold_producao` | 25 min |
| 03 | **Genie Agent** | Consumo de dados em linguagem natural, instruções customizadas | 25 min |
| 04 | **AI/BI Dashboard** | Painel **padrão** criado **inteiramente via prompt**, nas cores da Klabin | 25 min |
|    | **Encerramento** | Considerações finais e perguntas | 10 min |

> **Total: ~120 min.** Ritmo pensado para uma sessão única de 2 horas.

</br>

## Modelo de Dados

O workshop usa um **modelo estrela** da produção de celulose e papel de Telêmaco Borba:
**1 tabela fato** (`fato_producao`, com a produção diária por máquina) e **2 dimensões**
(`dim_maquinas` e `dim_produtos`). Todas ingeridas na camada **Bronze** por upload manual
(Lab 1) e combinadas em uma única tabela **Gold** (`gold_producao`) no Lab 2.

| Tabela | Tipo | Descrição |
| -- | -- | -- |
| `fato_producao` | Fato | Produção diária por máquina (toneladas, meta, energia, paradas, refugo) — 90 dias × 9 máquinas |
| `dim_maquinas` | Dimensão | Máquinas e linhas de produção por unidade (Monte Alegre / Puma) |
| `dim_produtos` | Dimensão | Produtos: celulose (fibra curta/longa/fluff) e papéis (kraftliner, cartão, sacos) |

</br>

## Pré-requisitos

| Requisito | Detalhes |
| -- | -- |
| Workspace | Databricks com **Unity Catalog** habilitado |
| Compute | Cluster DBR 14.0+ ou **Serverless** |
| SQL Warehouse | Necessário para Labs 03 (Genie) e 04 (AI/BI) |

### Permissões necessárias

O perfil mais simples é conceder **`ALL PRIVILEGES`** no catálogo `workshop_klabin`, além de
acesso a compute, Pipelines (LakeFlow Designer), Genie e Dashboards.

> **Dica:** O catálogo `workshop_klabin` é **compartilhado** e criado uma única vez. Cada
> participante trabalha em um **schema com o próprio nome**, no formato `nome_sobrenome`
> (`workshop_klabin.<nome_sobrenome>`).

</br>

## Estrutura do Projeto

```
workshop-klabin/
│
├── dados/                            # Dados prontos para upload manual
│   ├── fato_producao.csv             # FATO: produção diária por máquina (CSV)
│   ├── dim_maquinas.xlsx             # Dimensão: máquinas/linhas de produção (Excel)
│   ├── dim_produtos.xlsx             # Dimensão: produtos de celulose e papel (Excel)
│   └── gerar_dados.py                # Script que (re)gera os arquivos de dados
│
├── 00_Setup/
│   └── 00_configuracao_catalogo.py   # Catálogo workshop_klabin + schema pessoal
│
├── 01_Lab_Ingestao/
│   ├── 01a_guia_upload_dados.py      # Guia passo-a-passo do upload manual
│   └── 01b_validacao.py              # Validação das 3 tabelas Bronze
│
├── 02_Lab_Transformacao/
│   └── 02a_guia_lakeflow_designer.py # Uma transformação → gold_producao
│
├── 03_Lab_Genie/
│   └── 03a_genie.py                  # Genie Agent + instruções customizadas
│
└── 04_Lab_AIBI/
    └── 04a_dashboard.py              # Dashboard padrão criado via prompt (cores Klabin)
```

</br>

## Como Começar

### Passo 1: Importar os notebooks (Git folder)

1. No Databricks, vá em **Workspace** > **Users** > seu usuário
2. Clique em **Create** > **Git folder**
3. Cole a **URL do repositório**:

   ```
   https://github.com/juliandrof/workshop-klabin.git
   ```

4. Confirme em **Create Git folder** — todos os notebooks e a pasta `dados/` serão clonados

### Passo 2: Preparar seu schema pessoal

1. Abra `00_Setup/00_configuracao_catalogo.py`
2. **Execute a primeira célula** para o widget **nome_participante** aparecer
3. Preencha no formato **`nome_sobrenome`** (sem acentos, minúsculo — ex.: `joao_silva`)
4. Execute as demais células — seu schema fica em `workshop_klabin.<nome_sobrenome>`

### Passo 3: Baixar os dados do workshop

Os dados já estão na pasta [`dados/`](dados/): a **tabela fato** em **CSV** e as **dimensões**
em **XLSX**. Para fazer o upload no Lab 1, baixe-os para o seu computador:

1. No Databricks, abra a sua **Git folder** `workshop-klabin`
2. Selecione a pasta **`dados`**, clique nos **três pontos (⋮)** > **Download as** > **Zip - Source**
3. Descompacte — dentro estarão os 3 arquivos de dados:

| Arquivo | Formato | Registros | Tipo |
| -- | -- | -- | -- |
| `fato_producao.csv` | CSV | 810 | **Fato** |
| `dim_maquinas.xlsx` | XLSX | 9 | Dimensão |
| `dim_produtos.xlsx` | XLSX | 7 | Dimensão |

> Para **regenerar** os arquivos, rode `python3 dados/gerar_dados.py`.

</br>

---

## Lab 01 — Ingestão de Dados

| Item | Detalhes |
| -- | -- |
| **Objetivo** | Ingerir os 3 arquivos (fato em CSV, dimensões em Excel) na camada Bronze via **upload manual** |
| **Guia de upload** | `01_Lab_Ingestao/01a_guia_upload_dados.py` |
| **Notebook de validação** | `01_Lab_Ingestao/01b_validacao.py` |

### Instruções

1. **Suba cada arquivo** da pasta `dados/` para o **seu schema** (`workshop_klabin.<nome_sobrenome>`):
   1. No menu lateral, abra **Catalog** > `workshop_klabin` > schema **`<nome_sobrenome>`**
   2. Clique em **Create** > **Create table** (Upload files)
   3. Arraste o arquivo. Para o **CSV** (`fato_producao`), a opção **First row = header** fica em **Advanced attributes** — expanda e mantenha-a ativada. (Nos **XLSX** das dimensões o cabeçalho já é detectado automaticamente.)
   4. **Table name** = nome do arquivo sem a extensão (ex.: `fato_producao`) → **Create table**
   5. Repita para os 3 arquivos

| Arquivo | Tabela resultante |
| -- | -- |
| `fato_producao.csv` | `workshop_klabin.<nome_sobrenome>.fato_producao` |
| `dim_maquinas.xlsx` | `workshop_klabin.<nome_sobrenome>.dim_maquinas` |
| `dim_produtos.xlsx` | `workshop_klabin.<nome_sobrenome>.dim_produtos` |

2. **Valide** a ingestão. Como você está na página do **Catalog** (sem notebook aberto),
   vá em **Workspace** > abra a Git folder `workshop-klabin` >
   `01_Lab_Ingestao/01b_validacao.py`, preencha o widget `nome_participante` e clique em **Run all**.

</br>

---

## Lab 02 — Transformação com LakeFlow Designer

| Item | Detalhes |
| -- | -- |
| **Objetivo** | Construir **uma** tabela Gold (`gold_producao`) no LakeFlow Designer, sem código |
| **Notebook de apoio** | `02_Lab_Transformacao/02a_guia_lakeflow_designer.py` |

### A transformação (única)

Junta `fato_producao` com `dim_maquinas` e `dim_produtos` e calcula o **atingimento da meta**.

1. Abra o **LakeFlow Designer** (**+ New** > **Visual data prep**) e **renomeie** o rascunho no topo para `visual_prep_klabin_<nome_sobrenome>`
2. Adicione as 3 tabelas como **Source**
3. Abra o **Genie Code** e cole o prompt:

```text
A partir de @fato_producao, junte com @dim_maquinas pela coluna id_maquina
(trazendo nome_maquina, unidade e linha) e com @dim_produtos pela coluna
id_produto (trazendo nome_produto, categoria, tipo_fibra e mercado).
Adicione uma coluna atingimento_meta_pct = producao_ton dividido por meta_ton,
multiplicado por 100 e arredondado com 1 casa decimal. Salve o resultado como
gold_producao.
```

4. O prompt **já cria o passo de Output** — você não precisa adicioná-lo, apenas **configurá-lo**: selecione o tipo de saída **Table** (é o que **persiste** o resultado como tabela), confirme **Table name** `gold_producao` e o destino (catálogo `workshop_klabin` + schema `<nome_sobrenome>`)
5. Clique em **Run** — a execução **cria ou substitui** a tabela `gold_producao`

</br>

---

## Lab 03 — Genie Agent

| Item | Detalhes |
| -- | -- |
| **Objetivo** | Criar e curar uma Genie Agent para consultar a produção em linguagem natural |
| **Notebook** | `03_Lab_Genie/03a_genie.py` |

### Instruções

1. Execute o notebook para **adicionar comentários** à tabela Gold e às dimensões
2. **Crie a Genie Agent**: **Genie** (menu lateral) > **New**
3. **Adicione as tabelas**: na aba **Configure**, clique em **Add tables** (seção **Data**),
   navegue no **Catalog** até `workshop_klabin` > `<nome_sobrenome>` e **marque** as 3 tabelas:
   `gold_producao`, `dim_maquinas` e `dim_produtos` > **Confirm**
4. **Cole as instruções customizadas** (impressas pelo notebook) no campo **Instructions**,
   também dentro da aba **Configure**
5. **Teste** com perguntas como:
   - *"Qual máquina produziu mais no período?"*
   - *"Qual o atingimento médio da meta por unidade?"*
   - *"Compare a produção de celulose com a de papel"*
   - *"Qual produto teve mais refugo?"*

</br>

---

## Lab 04 — AI/BI Dashboard (criado inteiramente via prompt)

| Item | Detalhes |
| -- | -- |
| **Objetivo** | Criar **um dashboard padrão de produção**, igual para todos, **usando apenas prompt** |
| **Notebook** | `04_Lab_AIBI/04a_dashboard.py` |

> **Sem competição.** Todos os participantes terminam com o **mesmo dashboard de referência**,
> nas **cores da Klabin**. O foco é aprender a gerar e ajustar visualizações **por linguagem
> natural** — sem montar widget por widget na mão.

### Cores da Klabin usadas no painel

| Cor | Hex |
| -- | -- |
| Verde primário | `#00843D` |
| Verde escuro | `#004B23` |
| Verde claro | `#7AB800` |
| Kraft (papel) | `#B07A3E` |
| Cinza | `#6E6E6E` |
| Areia | `#E8DFCF` |

### Instruções

1. Vá em **Dashboards** > **Create dashboard** e nomeie `Dashboard Produção Klabin - <seu_nome>`
2. Na aba **Data**, adicione a tabela `gold_producao` como dataset
3. Na aba **Untitled** (a página inicial do dashboard), abra o **Assistant** e **cole o prompt padrão** (impresso pelo notebook)
4. A IA gera todos os widgets (KPIs, donut, barras, linha e tabela) já nas cores da Klabin
5. (Opcional) Continue conversando com o Assistant para ajustar — **sempre por prompt**

O prompt padrão gera:
- **4 counters**: produção total, máquinas ativas, atingimento médio da meta, energia total
- **Donut**: produção por categoria (Celulose vs Papel)
- **Barras horizontais**: produção por máquina
- **Barras**: produção por unidade (Monte Alegre vs Puma)
- **Linha**: produção diária ao longo do tempo
- **Tabela**: detalhe por máquina (produção, atingimento e refugo)

</br>

---

## Dicas Importantes

> **Use sempre o mesmo `nome_participante`** em todos os notebooks para manter suas tabelas consistentes.

> **No Lab 1**, use exatamente os nomes de arquivo como nome de tabela (ex.: `fato_producao`) — os labs seguintes dependem desses nomes.

</br>

## Limpeza (Pós-Workshop)

```sql
-- Substitua <seu_nome> pelo nome usado no workshop.
-- Apague apenas o SEU schema — o catálogo workshop_klabin é compartilhado.
DROP SCHEMA IF EXISTS workshop_klabin.<seu_nome> CASCADE;
```

</br>

## Referências

* [LakeFlow Designer](https://docs.databricks.com/ingestion/lakeflow-designer/index.html)
* [Criar tabela via upload de arquivo](https://docs.databricks.com/ingestion/add-data/upload-data.html)
* [AI/BI Genie](https://docs.databricks.com/genie/index.html)
* [AI/BI Dashboards](https://docs.databricks.com/dashboards/index.html)
* [Unity Catalog](https://docs.databricks.com/data-governance/unity-catalog/index.html)

</br>

---

<p align="center">
  <strong>Workshop Hands-On Databricks — Klabin</strong><br>
  <em>Data & AI na prática · Telêmaco Borba (PR)</em>
</p>
