# API de Funções

Documentação das funções Python e Node.js disponíveis.

---

## Python Scripts

### `pbix_extractor.py`

Descompacta um arquivo PBIX e extrai JSONs de layout.

**Uso:**
```bash
python scripts/pbix_extractor.py <arquivo.pbix> [--output-dir ./extracted/]
```

**Parâmetros:**
- `arquivo.pbix` - Caminho do arquivo PBIX a descompactar
- `--output-dir` - (opcional) Diretório de saída (padrão: ./extracted/)

**Retorno:**
```
✓ PBIX descompactado
✓ JSONs extraídos para ./extracted/
✓ Estrutura:
  extracted/
  ├── report/
  │   ├── definition/
  │   │   └── pages/
  │   │       ├── <page-hash>/
  │   │       │   ├── visual.json
  │   │       │   └── ...
  │   │       └── ...
  │   └── ...
  └── ...
```

**Exemplo:**
```bash
python scripts/pbix_extractor.py vendas.pbix
```

---

### `pbix_recompactor.py`

Recompacta JSONs editados em arquivo PBIX.

**Uso:**
```bash
python scripts/pbix_recompactor.py <pasta-extraida> <arquivo-saida.pbix>
```

**Parâmetros:**
- `pasta-extraida` - Diretório com JSONs descompactados (ex: ./extracted/)
- `arquivo-saida.pbix` - Arquivo PBIX de saída

**Retorno:**
```
✓ JSONs verificados
✓ PBIX recompactado
✓ Arquivo: arquivo-saida.pbix pronto
```

**Exemplo:**
```bash
python scripts/pbix_recompactor.py extracted/ vendas.pbix
```

---

### `pbix_validator.py`

Valida integridade de arquivo PBIX.

**Uso:**
```bash
python scripts/pbix_validator.py <arquivo.pbix>
```

**Parâmetros:**
- `arquivo.pbix` - Arquivo a validar

**Retorno:**
```
✓ PBIX válido
✓ JSONs verificados
✓ Estrutura OK
```

**Exemplo:**
```bash
python scripts/pbix_validator.py vendas.pbix
```

---

## Node.js MCP Server

### `pbir-visual-editor-mcp.js`

MCP Server para editar layouts via Claude/Copilot.

**Funções disponíveis:**

#### `get_layout(page_id)`
Retorna JSON de layout de uma página.

```
Entrada: page_id = "abc123..."
Saída: { visuais: [...], propriedades: {...} }
```

#### `update_visual(page_id, visual_id, props)`
Atualiza propriedades de um visual.

```
Entrada:
  page_id = "abc123..."
  visual_id = "xyz789..."
  props = { "fill": "#FF0000", "fontSize": 24 }

Saída: { sucesso: true, alterado: true }
```

#### `list_pages()`
Lista todas as páginas do relatório.

```
Saída: [
  { id: "page1", nome: "Vendas" },
  { id: "page2", nome: "KPIs" }
]
```

#### `list_visuals(page_id)`
Lista todos os visuais de uma página.

```
Entrada: page_id = "page1"
Saída: [
  { id: "visual1", tipo: "columnChart", nome: "Sales" },
  { id: "visual2", tipo: "card", nome: "Total" }
]
```

---

## Exemplo Completo de Uso

### Scenario: Mudar cor de gráfico

**Comando para Claude:**
```
Mude o gráfico 'Sales 2024' para azul (#0078D4)
```

**O que Claude faz via MCP:**
```javascript
// 1. Encontra a página
pages = await mcp.list_pages()
page = pages.find(p => p.nome === "Vendas")

// 2. Encontra o visual
visuals = await mcp.list_visuals(page.id)
visual = visuals.find(v => v.nome === "Sales 2024")

// 3. Atualiza cor
await mcp.update_visual(page.id, visual.id, {
  "fill": "#0078D4",
  "stroke": "#0078D4"
})

// 4. Retorna sucesso
return { sucesso: true, visual: "Sales 2024", alterado: true }
```

---

## Erros Comuns

### Erro: "Arquivo PBIX inválido"
```
Causa: Arquivo não é PBIX válido
Solução: Verifique se é arquivo .pbix correto
```

### Erro: "Visual não encontrado"
```
Causa: Nome de visual incorreto
Solução: Use list_visuals() para ver nomes exatos
```

### Erro: "Propriedade inválida"
```
Causa: Tentou mudar propriedade que não existe
Solução: Consulte documentação de JSON do Power BI
```

---

## Próximos Passos

- Veja **[EXEMPLOS.md](EXEMPLOS.md)** para casos práticos
- Consulte **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** para erros
- Leia **[ARQUITETURA.md](ARQUITETURA.md)** para internals

