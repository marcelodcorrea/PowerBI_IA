# Exemplos Práticos

5-10 casos reais prontos para copiar/colar.

---

## Exemplo 1: Mudar Cores de Gráficos

**Cenário:** Você recebeu feedback que os gráficos estão com cores de prototipagem. Precisa mudar para azul corporativo.

**Comando:**
```
Claude, neste relatório, mude todos os gráficos de azul claro para azul corporativo:
- Cor: #0078D4
- Manter o mesmo contraste
```

**Resultado:** Todos os gráficos com cor corporativa.

---

## Exemplo 2: Aumentar Tamanho de Fonte

**Cenário:** Gerente quer que os KPIs fiquem mais visíveis. Precisa aumentar tamanho da fonte.

**Comando:**
```
Claude, aumente os títulos dos cards KPI:
- Tamanho atual: 14px
- Novo tamanho: 24px
- Mantenha a cor
```

**Resultado:** Títulos maiores e mais legíveis.

---

## Exemplo 3: Reorganizar Layout

**Cenário:** Precisa mover elementos para deixar espaço para novo visual.

**Comando:**
```
Claude, reorganize a página 'Dashboard':
1. Mova o gráfico 'Sales' para a esquerda
2. Mude o tamanho para 300x200px
3. Deixe espaço para novo elemento à direita
```

**Resultado:** Layout reorganizado com espaço livre.

---

## Exemplo 4: Renomear Elementos

**Cenário:** Nomes dos elementos estão em inglês, precisa traduzir.

**Comando:**
```
Claude, traduza os seguintes elementos:
- 'Sales by Region' → 'Vendas por Região'
- 'Year to Date' → 'No Ano'
- 'Monthly Trend' → 'Tendência Mensal'
```

**Resultado:** Todos os nomes em português.

---

## Exemplo 5: Adicionar Formatação

**Cenário:** Precisa destacar números importantes com formatação especial.

**Comando:**
```
Claude, no card 'Total Revenue':
1. Número em negrito
2. Aumente tamanho para 36px
3. Adicione formatação de moeda ($)
```

**Resultado:** Número destacado e formatado corretamente.

---

## Exemplo 6: Mudar Transparência/Opacidade

**Cenário:** Fundo de alguns elementos está muito opaco, reduzir visibilidade.

**Comando:**
```
Claude, reduza a opacidade dos backgrounds:
- Card KPI: de 100% para 80%
- Gráfico: de 100% para 90%
```

**Resultado:** Backgrounds com transparência ajustada.

---

## Exemplo 7: Alinhar Elementos

**Cenário:** Elementos estão desalinhados visualmente, precisa arrumar.

**Comando:**
```
Claude, alinhe os elements horizontalmente:
- Cards KPI: todos na mesma altura (y=100)
- Espaçamento igual entre eles: 20px
```

**Resultado:** Elementos alinhados perfeitamente.

---

## Exemplo 8: Mudar Estilos de Borda

**Cenário:** Adicionar bordas para melhor separação visual.

**Comando:**
```
Claude, adicione bordas aos elementos:
- Cor: #CCCCCC
- Espessura: 2px
- Raio: 4px (cantos arredondados)
```

**Resultado:** Elementos com bordas elegantes.

---

## Exemplo 9: Mudar Tipos de Visualização (Layout)

**Cenário:** Algumas visualizações podem mudar de tipo (coluna → linha).

**Comando:**
```
Claude, neste layout, onde há espaço para mudar:
1. Gráfico 'Trend': de coluna para linha
2. Mantenha as cores
3. Mesma altura
```

**Resultado:** Gráfico com novo tipo de visual.

---

## Exemplo 10: Batch de Mudanças

**Cenário:** Múltiplas mudanças no mesmo relatório.

**Comando:**
```
Claude, faça o seguinte no relatório:

CORES:
- Mude azul claro (#ADD8E6) para azul corporativo (#0078D4)
- Mude vermelho (#FF0000) para laranja (#FF8C00)

FONTES:
- Títulos: aumente para 20px (de 16px)
- Subtítulos: mantenha em 12px

LAYOUT:
- Card KPI: mova para topo
- Gráfico Sales: mude tamanho para 400x300px
```

**Resultado:** Todas as mudanças aplicadas de uma vez.

---

## Dicas para Escrever Bons Comandos

### ✅ Bom: Específico
```
Mude o gráfico 'Monthly Sales' da página 'Dashboard':
- Cor de fundo: de cinza para branco
- Borda: adicione #CCCCCC 2px
- Tamanho fonte: 14px
```

### ❌ Ruim: Genérico
```
Mude as cores (muito vago, Claude não sabe exatamente o quê)
```

### ✅ Bom: Com contexto
```
No relatório de vendas, página 'Performance':
- Gráfico 'Target vs Actual': mude cor série 'Target' para vermelho
- Mantenha série 'Actual' em verde
```

### ❌ Ruim: Sem contexto
```
Mude aquele gráfico (qual gráfico? qual página?)
```

### ✅ Bom: Valores explícitos
```
- Tamanho fonte: 18px (de 14px)
- Cor: #0078D4 (azul corporativo)
- Opacidade: 80% (de 100%)
```

### ❌ Ruim: Termos vagos
```
- Aumente um pouco a fonte
- Mude para uma cor melhor
- Deixe mais transparente
```

---

## Próximos Passos

Comece com um dos exemplos acima e adapte para seu relatório!

- **[FLUXO.md](FLUXO.md)** - Como executar
- **[API.md](API.md)** - Funções disponíveis
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Se houver erros

