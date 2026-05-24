# Arquitetura - Como Funciona Internamente

Documentação técnica para desenvolvedores que querem entender o projeto.

---

## Visão Geral

```
PowerBI PBIX
    ↓
Python extractor.py (descompacta)
    ↓
JSON files (layout, visuals, etc)
    ↓
Node.js MCP Server (conecta ao Claude)
    ↓
Claude/Copilot edita via MCP
    ↓
JSON files (atualizados)
    ↓
Python recompactor.py (recompacta)
    ↓
Novo PowerBI PBIX (com mudanças)
```

---

## Componentes Principais

### 1. Python Extractor

**Arquivo:** `scripts/pbix_extractor.py`

**O que faz:**
- Lê arquivo PBIX (que é ZIP)
- Extrai estrutura de pastas
- Copia JSONs de layout para `./extracted/`

**Estrutura extraída:**
```
extracted/
├── report/
│   ├── definition/
│   │   └── pages/
│   │       ├── <page1-hash>/
│   │       │   ├── visual.json
│   │       │   ├── config.json
│   │       │   └── ...
│   │       └── <page2-hash>/
│   │           ├── visual.json
│   │           └── ...
│   └── ...
├── semanticModel/
└── ...
```

**Código simplificado:**
```python
def extract_pbix(pbix_file):
    with zipfile.ZipFile(pbix_file, 'r') as zip:
        zip.extractall('extracted/')
    return True
```

---

### 2. JSON Structure

**Arquivo:** `extracted/report/definition/pages/<hash>/visual.json`

**Exemplo de visual.json:**
```json
{
  "name": "Sales Chart",
  "visualType": "columnChart",
  "config": {
    "x": 100,
    "y": 200,
    "width": 400,
    "height": 300
  },
  "properties": {
    "fill": "#0078D4",
    "fontSize": 14,
    "title": "Monthly Sales"
  },
  "dataBindings": {
    "Category": "Date",
    "Values": ["Sales"]
  }
}
```

---

### 3. Node.js MCP Server

**Arquivo:** `mcp/pbir-visual-editor-mcp.js`

**O que faz:**
- Conecta Claude ao sistema de arquivos
- Lê JSONs de layout
- Permite Claude editar propriedades

**Endpoints MCP:**
```javascript
// Listar páginas
mcp.tool('list_pages', () => {...})

// Listar visuais de uma página
mcp.tool('list_visuals', (page_id) => {...})

// Atualizar propriedade de visual
mcp.tool('update_visual', (page_id, visual_id, props) => {...})

// Obter layout de página
mcp.tool('get_layout', (page_id) => {...})
```

---

### 4. Python Recompactor

**Arquivo:** `scripts/pbix_recompactor.py`

**O que faz:**
- Lê JSONs editados de `./extracted/`
- Recompacta em novo PBIX

**Código simplificado:**
```python
def recompact_pbix(extracted_dir, output_file):
    with zipfile.ZipFile(output_file, 'w') as zip:
        for root, dirs, files in os.walk(extracted_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, extracted_dir)
                zip.write(file_path, arcname)
    return True
```

---

## Fluxo de Edição

### Passo 1: Claude lê layout

```javascript
// Claude solicita:
layout = await mcp.get_layout('page1')

// MCP retorna:
{
  "visuais": [
    { id: "v1", nome: "Sales", tipo: "columnChart" },
    { id: "v2", nome: "KPI", tipo: "card" }
  ]
}
```

### Passo 2: Claude atualiza propriedade

```javascript
// Claude executa:
await mcp.update_visual('page1', 'v1', {
  "fill": "#0078D4"
})

// MCP atualiza arquivo JSON:
// extracted/report/definition/pages/page1/visual.json
```

### Passo 3: Arquivo é salvo

```
visual.json agora contém:
{
  "properties": {
    "fill": "#0078D4"  // ← mudado
  }
}
```

### Passo 4: Recompacta

```bash
python scripts/pbix_recompactor.py extracted/ novo.pbix
```

---

## Formato JSON (Deep Dive)

### Visual.json completo

```json
{
  "id": "abc123...",
  "name": "Sales by Region",
  "visualType": "columnChart",
  
  "config": {
    "x": 100,
    "y": 50,
    "width": 500,
    "height": 300,
    "z": 0
  },
  
  "properties": {
    "fill": "#FFFFFF",
    "stroke": "#CCCCCC",
    "strokeWidth": 1,
    "fontSize": 14,
    "fontFamily": "Arial",
    "fontWeight": "normal",
    "textColor": "#000000"
  },
  
  "chartProperties": {
    "title": "Sales by Region",
    "xAxisLabel": "Region",
    "yAxisLabel": "Sales ($)",
    "legend": true,
    "gridLines": true
  },
  
  "dataBindings": {
    "Category": "Region",
    "Values": ["Sales"],
    "Color": null
  }
}
```

---

## Propriedades Editáveis

### Posicionamento
- `config.x` - Posição horizontal (em pixels)
- `config.y` - Posição vertical (em pixels)
- `config.width` - Largura (em pixels)
- `config.height` - Altura (em pixels)
- `config.z` - Camada (z-index)

### Cores
- `properties.fill` - Cor de fundo (#RRGGBB)
- `properties.stroke` - Cor de borda (#RRGGBB)
- `properties.textColor` - Cor de texto (#RRGGBB)

### Tipografia
- `properties.fontSize` - Tamanho (em pixels)
- `properties.fontFamily` - Fonte (Arial, Segoe UI, etc)
- `properties.fontWeight` - Peso (normal, bold)

### Conteúdo
- `chartProperties.title` - Título do visual
- `chartProperties.xAxisLabel` - Label eixo X
- `chartProperties.yAxisLabel` - Label eixo Y
- `chartProperties.legend` - Mostrar legenda (true/false)

---

## Limitações e Considerações

### ✅ O que funciona bem
- Editar propriedades visuais (cores, tamanhos, fontes)
- Reorganizar layout (posição, largura, altura)
- Renomear títulos e labels
- Mudar visibilidade de elementos

### ❌ O que não funciona
- Alterar dados (requer Power Query)
- Criar novas medidas DAX (requer modelo semântico)
- Mudar tipos de visualização (requer recrear visual)
- Modificar relacionamentos de tabelas

---

## Referência: Visual de Tabela (`tableEx`)

O `tableEx` tem exigências específicas que diferem dos outros visuais. Omitir qualquer campo obrigatório resulta em tabela em branco sem mensagem de erro.

### Campos obrigatórios

| Campo | Onde | Descrição |
|---|---|---|
| `nativeQueryRef` | Cada projeção | Nome legível da coluna/medida. **Sem ele a query não resolve.** |
| `drillFilterOtherVisuals` | `visual` | Deve ser `true` |
| `filterConfig.filters` | Raiz do visual | Uma entrada por campo: `Categorical` para colunas, `Advanced` para medidas |

### Bucket correto

| Visual | Dimensões | Medidas |
|---|---|---|
| `tableEx` (tabela simples) | `Values` | `Values` |
| `pivotTable` (matriz) | `Rows` / `Columns` | `Values` |

**Nunca colocar dimensões em `Rows` num `tableEx`** — são silenciosamente ignoradas.

### Restrição de tabelas de dimensão

Combinar colunas de tabelas diferentes sem a chave de junção causa cross-join vazio:

```
❌ vendas.Vendedor + regioes.Região + produtos.Categoria  → tabela em branco
✅ vendas.Vendedor + vendas.Produto                       → funciona
```

### Estrutura mínima funcional

```json
{
  "visual": {
    "visualType": "tableEx",
    "query": {
      "queryState": {
        "Values": {
          "projections": [
            {
              "field": { "Column": { "Expression": { "SourceRef": { "Entity": "tabela" } }, "Property": "Coluna" } },
              "queryRef": "tabela.Coluna",
              "nativeQueryRef": "Coluna"
            },
            {
              "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "_Medidas" } }, "Property": "Medida" } },
              "queryRef": "_Medidas.Medida",
              "nativeQueryRef": "Medida"
            }
          ]
        }
      }
    },
    "drillFilterOtherVisuals": true
  },
  "filterConfig": {
    "filters": [
      { "name": "<hex-20-chars>", "field": { "Column": { "Expression": { "SourceRef": { "Entity": "tabela" } }, "Property": "Coluna" } }, "type": "Categorical" },
      { "name": "<hex-20-chars>", "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "_Medidas" } }, "Property": "Medida" } }, "type": "Advanced" }
    ]
  }
}
```

---

## Debugging

### Ver arquivo JSON editado
```bash
cat extracted/report/definition/pages/<hash>/visual.json | jq
```

### Validar JSON
```bash
python scripts/pbix_validator.py novo.pbix
```

### Ver diff de mudanças
```bash
git diff extracted/
```

---

## Próximos Passos

- Para usar: **[FLUXO.md](FLUXO.md)**
- Para exemplos: **[EXEMPLOS.md](EXEMPLOS.md)**
- Para API: **[API.md](API.md)**

