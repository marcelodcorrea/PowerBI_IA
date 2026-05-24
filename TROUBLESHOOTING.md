# Troubleshooting — Erros durante o Uso

Erros que podem ocorrer **depois que o projeto já está instalado**, durante o uso diário.

> Para erros de instalação (Python, Node.js, MCP não conecta), consulte [GUIA_RAPIDO_INICIO.md](GUIA_RAPIDO_INICIO.md).

---

## "Visual não encontrado"

**Causa:** O nome do visual passado ao Claude não corresponde a nenhum elemento no JSON.

**Solução:**
1. Peça ao Claude que liste os visuais disponíveis:
   ```
   Claude, liste todos os visuais da página 'Dashboard'
   ```
2. Use exatamente o nome retornado por ele na próxima solicitação.

---

## "Propriedade inválida"

**Causa:** Tentativa de modificar uma propriedade que não existe ou não é suportada para aquele tipo de visual.

**Solução:**
1. Consulte [API.md](API.md) para ver as propriedades válidas por tipo de visual.
2. Propriedades mais comuns:
   - `fill` — cor de fundo
   - `fontSize` — tamanho da fonte
   - `stroke` — cor da borda
   - `color` — cor do texto ou dado

---

## "Arquivo PBIX corrompido após recompactar"

**Causa:** Um ou mais JSONs ficaram malformados durante a edição.

**Solução:**
1. Se estiver usando Git, restaure os JSONs:
   ```bash
   git diff extracted/          # veja o que mudou
   git checkout extracted/      # descarta todas as mudanças
   ```
2. Se não estiver usando Git, re-extraia a partir do PBIX original:
   ```bash
   python scripts/pbix_extractor.py pbix/seu_relatorio.pbix
   ```
3. Recomece as edições com mais cuidado.

---

## Tabela (`tableEx`) aparece em branco sem dados

**Causa 1 — `nativeQueryRef` ausente:**
O campo `nativeQueryRef` é obrigatório em cada projeção do `tableEx`. Sem ele, o Power BI não consegue resolver a query e exibe a tabela completamente vazia, mesmo que as colunas apareçam configuradas no painel lateral.

**Causa 2 — Bucket errado para dimensões:**
No `tableEx` (tabela simples), todas as colunas — dimensões e medidas — devem estar no bucket `Values` do `queryState`. O bucket `Rows` é exclusivo do visual de **matriz** (`pivotTable`). Dimensões em `Rows` são silenciosamente ignoradas.

**Causa 3 — Colunas de tabelas de dimensão sem chave de junção:**
Combinar colunas de tabelas diferentes (ex: `vendas.Vendedor` + `regioes.Região` + `produtos.Categoria`) sem incluir a chave de relacionamento resulta em cross-join vazio. Use apenas colunas da mesma tabela de granularidade, ou inclua a coluna-chave que une as tabelas.

**Estrutura correta de um `tableEx` funcional:**

```json
{
  "visual": {
    "visualType": "tableEx",
    "query": {
      "queryState": {
        "Values": {
          "projections": [
            {
              "field": {
                "Column": {
                  "Expression": { "SourceRef": { "Entity": "vendas" } },
                  "Property": "Vendedor"
                }
              },
              "queryRef": "vendas.Vendedor",
              "nativeQueryRef": "Vendedor"
            },
            {
              "field": {
                "Measure": {
                  "Expression": { "SourceRef": { "Entity": "_Medidas" } },
                  "Property": "Total Vendas"
                }
              },
              "queryRef": "_Medidas.Total Vendas",
              "nativeQueryRef": "Total Vendas"
            }
          ]
        }
      }
    },
    "drillFilterOtherVisuals": true
  },
  "filterConfig": {
    "filters": [
      {
        "name": "hex20chars_unico",
        "field": {
          "Column": {
            "Expression": { "SourceRef": { "Entity": "vendas" } },
            "Property": "Vendedor"
          }
        },
        "type": "Categorical"
      },
      {
        "name": "hex20chars_unico2",
        "field": {
          "Measure": {
            "Expression": { "SourceRef": { "Entity": "_Medidas" } },
            "Property": "Total Vendas"
          }
        },
        "type": "Advanced"
      }
    ]
  }
}
```

**Regras resumidas para `tableEx`:**
- `nativeQueryRef` obrigatório em toda projeção (valor = nome da coluna/medida)
- Tudo em `Values` — nunca usar `Rows`
- `drillFilterOtherVisuals: true` no nível do `visual`
- `filterConfig` com uma entrada por campo: colunas → `"type": "Categorical"`, medidas → `"type": "Advanced"`
- Colunas de dimensão: usar apenas campos da mesma tabela de granularidade

---

## Dicas de Uso Seguro

### Versionar com Git antes de editar

```bash
git add extracted/
git commit -m "antes das edições de layout"
```

Isso permite desfazer qualquer mudança rapidamente:

```bash
git log --oneline extracted/          # veja o histórico
git checkout <hash> -- extracted/     # restaura versão específica
```

### Revisar JSONs antes de recompactar

```bash
git diff extracted/    # veja exatamente o que foi alterado
```

Se algo parecer errado, descarte antes de recompactar:

```bash
git checkout extracted/
```

---

Mais informações: [API.md](API.md) | [ARQUITETURA.md](ARQUITETURA.md) | [GUIA_RAPIDO_INICIO.md](GUIA_RAPIDO_INICIO.md)
