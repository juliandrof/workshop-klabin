#!/usr/bin/env python3
"""
Gera os dados sintéticos do Workshop Klabin, prontos para upload manual no
Databricks (Catalog > Create table > Upload files).

Produz 3 tabelas (1 fato + 2 dimensões):
- a **fato** (`fato_producao`) **apenas em .csv**;
- as **dimensões** (`dim_maquinas`, `dim_produtos`) **apenas em .xlsx**.

(Os labs usam o CSV da fato e o Excel das dimensões.)

Modelo estrela da produção de celulose e papel do complexo de Telêmaco Borba (PR):
unidade Monte Alegre (máquinas de papel: kraftliner, cartão, papel para sacos) e a
vizinha unidade Puma, em Ortigueira (celulose de fibra curta/longa/fluff + Puma II).

Não depende de bibliotecas externas: o XLSX é escrito com um mini-writer baseado
apenas na biblioteca padrão (zipfile + xml).

Uso:  python3 gerar_dados.py
"""

import csv
import os
import random
import datetime
import zipfile
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
random.seed(42)


# ─────────────────────────────────────────────────────────────────────────────
# Mini-writer de XLSX (somente biblioteca padrão)
# ─────────────────────────────────────────────────────────────────────────────

def _col_ref(idx):
    """0 -> A, 1 -> B, ... 26 -> AA."""
    s = ""
    idx += 1
    while idx:
        idx, rem = divmod(idx - 1, 26)
        s = chr(65 + rem) + s
    return s


def write_xlsx(path, header, rows):
    """Escreve um .xlsx de uma única planilha. Números viram células numéricas."""
    def cell(c, r, value):
        ref = f"{_col_ref(c)}{r}"
        if isinstance(value, bool):
            value = int(value)
        if isinstance(value, (int, float)):
            return f'<c r="{ref}"><v>{value}</v></c>'
        return f'<c r="{ref}" t="inlineStr"><is><t xml:space="preserve">{escape(str(value))}</t></is></c>'

    sheet_rows = []
    # header (linha 1)
    cells = "".join(cell(c, 1, h) for c, h in enumerate(header))
    sheet_rows.append(f'<row r="1">{cells}</row>')
    # dados
    for ri, row in enumerate(rows, start=2):
        cells = "".join(cell(c, ri, v) for c, v in enumerate(row))
        sheet_rows.append(f'<row r="{ri}">{cells}</row>')

    sheet_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        f'<sheetData>{"".join(sheet_rows)}</sheetData></worksheet>'
    )
    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
        '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        '</Types>'
    )
    root_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
        '</Relationships>'
    )
    workbook = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        '<sheets><sheet name="Dados" sheetId="1" r:id="rId1"/></sheets></workbook>'
    )
    workbook_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
        '</Relationships>'
    )

    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", root_rels)
        z.writestr("xl/workbook.xml", workbook)
        z.writestr("xl/_rels/workbook.xml.rels", workbook_rels)
        z.writestr("xl/worksheets/sheet1.xml", sheet_xml)


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def salvar(nome, header, rows, formatos=("csv", "xlsx")):
    escritos = []
    if "csv" in formatos:
        write_csv(os.path.join(HERE, f"{nome}.csv"), header, rows)
        escritos.append(f"{nome}.csv")
    if "xlsx" in formatos:
        write_xlsx(os.path.join(HERE, f"{nome}.xlsx"), header, rows)
        escritos.append(f"{nome}.xlsx")
    print(f"  {nome}: {len(rows)} linhas  ->  {' + '.join(escritos)}")


# ─────────────────────────────────────────────────────────────────────────────
# 1. Dimensão: Máquinas / Linhas de Produção (complexo Telêmaco Borba)
# ─────────────────────────────────────────────────────────────────────────────
# unidade: Monte Alegre (Telêmaco Borba/PR) ou Puma (Ortigueira/PR, ao lado)
# id_produto: produto principal fabricado na máquina (liga com dim_produtos)

maquinas = [
    # id, nome_maquina,            unidade,        linha,               id_produto, capacidade_ton_dia, ano_operacao
    (1,  "Linha Fibra Curta",      "Puma",         "Celulose",          1, 4200, 2016),
    (2,  "Linha Fibra Longa",      "Puma",         "Celulose",          2, 1500, 2016),
    (3,  "Linha Fluff",            "Puma",         "Celulose",          3,  900, 2016),
    (4,  "Máquina MP27",           "Puma",         "Kraftliner",        4, 1230, 2021),
    (5,  "Máquina MP28",           "Puma",         "Cartão",            6, 1260, 2021),
    (6,  "Máquina de Papel MA-1100","Monte Alegre","Kraftliner",        4, 1100, 2008),
    (7,  "Máquina de Cartão MA-16","Monte Alegre", "Cartão",            6,  780, 1998),
    (8,  "Máquina de Sacos MA-9",  "Monte Alegre", "Papel para Sacos",  7,  520, 1985),
    (9,  "Máquina White Top MA-22","Monte Alegre", "White Top Kraftliner", 5, 640, 2014),
]
HDR_MAQUINAS = ["id_maquina", "nome_maquina", "unidade", "linha",
                "id_produto", "capacidade_ton_dia", "ano_operacao"]


# ─────────────────────────────────────────────────────────────────────────────
# 2. Dimensão: Produtos (celulose e papel)
# ─────────────────────────────────────────────────────────────────────────────

produtos = [
    # id, nome_produto,             categoria,   tipo_fibra,   gramatura_g_m2, mercado
    (1, "Celulose Fibra Curta",     "Celulose",  "Eucalipto",  0,   "Exportação"),
    (2, "Celulose Fibra Longa",     "Celulose",  "Pínus",      0,   "Exportação"),
    (3, "Celulose Fluff",           "Celulose",  "Pínus",      0,   "Mercado Interno"),
    (4, "Kraftliner",               "Papel",     "Pínus",      175, "Embalagem"),
    (5, "White Top Kraftliner",     "Papel",     "Pínus",      140, "Embalagem"),
    (6, "Cartão",                   "Papel",     "Mista",      300, "Embalagem"),
    (7, "Papel para Sacos",         "Papel",     "Pínus",       80, "Mercado Interno"),
]
HDR_PRODUTOS = ["id_produto", "nome_produto", "categoria", "tipo_fibra",
                "gramatura_g_m2", "mercado"]


# ─────────────────────────────────────────────────────────────────────────────
# 3. FATO: Produção diária por máquina (tabela plana)
# ─────────────────────────────────────────────────────────────────────────────

DIAS = 90   # ~3 meses de produção diária
HDR_FATO = ["id_registro", "data", "id_maquina", "id_produto", "turno",
            "producao_ton", "meta_ton", "tempo_operacao_h", "paradas_h",
            "consumo_energia_mwh", "umidade_pct", "refugo_ton"]

# mapa auxiliar: id_maquina -> (id_produto, capacidade, linha)
maq_info = {m[0]: (m[4], m[5], m[3]) for m in maquinas}

turnos = ["Turno A", "Turno B", "Turno C"]

fato = []
registro_id = 1
data_base = datetime.date(2025, 4, 1)

for d in range(DIAS):
    data = data_base + datetime.timedelta(days=d)
    fim_de_semana = data.weekday() >= 5
    for m in maquinas:
        id_maquina = m[0]
        id_produto, capacidade, linha = maq_info[id_maquina]

        # turno predominante do registro do dia (rotativo)
        turno = turnos[(d + id_maquina) % 3]

        # fábrica opera em regime contínuo; leve queda em fim de semana p/ manutenção
        fator_utilizacao = random.uniform(0.82, 0.99)
        if fim_de_semana:
            fator_utilizacao *= random.uniform(0.85, 0.98)

        tempo_operacao_h = round(24 * fator_utilizacao, 1)
        paradas_h = round(24 - tempo_operacao_h, 1)

        producao_ton = round(capacidade * fator_utilizacao * random.uniform(0.94, 1.03), 1)
        meta_ton = round(capacidade * 0.95, 1)

        # celulose consome mais energia por tonelada que papel
        if linha == "Celulose":
            energia_por_ton = random.uniform(0.55, 0.75)
        else:
            energia_por_ton = random.uniform(0.75, 1.05)
        consumo_energia_mwh = round(producao_ton * energia_por_ton, 1)

        umidade_pct = round(random.uniform(6.5, 9.5), 1)
        refugo_ton = round(producao_ton * random.uniform(0.005, 0.03), 2)

        fato.append((registro_id, data.strftime("%Y-%m-%d"), id_maquina, id_produto,
                     turno, producao_ton, meta_ton, tempo_operacao_h, paradas_h,
                     consumo_energia_mwh, umidade_pct, refugo_ton))
        registro_id += 1


def main():
    print("Gerando dados do Workshop Klabin...")
    # Dimensões: apenas XLSX (os labs usam só o Excel das dimensões)
    salvar("dim_maquinas", HDR_MAQUINAS, maquinas, formatos=("xlsx",))
    salvar("dim_produtos", HDR_PRODUTOS, produtos, formatos=("xlsx",))
    # Fato: apenas CSV (usado nos labs)
    salvar("fato_producao", HDR_FATO, fato, formatos=("csv",))
    print(f"\nConcluído! {len(fato)} registros de produção ({DIAS} dias x {len(maquinas)} máquinas).")
    print(f"Arquivos salvos em: {HERE}")


if __name__ == "__main__":
    main()
