# Seu Dia a Dia com PowerBI IA

Como usar o assistente no dia a dia. Fluxo simples em 7 passos.

---

## 7 Passos (Ciclo Completo)

### 1️⃣ Baixar PBIX do Workspace

```bash
# No Power BI Service → Baixar arquivo
# Salve em: ./pbix/relatorio.pbix
```

### 2️⃣ Descompactar com Python

```bash
python scripts/pbix_extractor.py relatorio.pbix
```

**O que acontece:**
- PBIX é descompactado
- JSONs de layout extraídos para `./extracted/`
- Pronto para editar

### 3️⃣ Abrir VSCode + MCP

```bash
code .
```

Node.js MCP conecta automaticamente aos JSONs extraídos.

### 4️⃣ Solicitar Mudança à IA

No Claude ou Copilot, escreva:

```
Claude, mude os seguintes elementos no layout:
1. Gráfico 'Vendas': mude cor para azul
2. Card 'KPI': aumente tamanho fonte para 24px
3. Título da página: mude para maiúsculas
```

**Claude executa via MCP:**
- Lê JSONs de layout
- Encontra elementos
- Edita propriedades
- Arquivos são atualizados

### 5️⃣ Revisar Mudanças

No VSCode:
- Veja os JSONs alterados
- HTML preview atualiza em tempo real
- Aprove ou desfaça (`git checkout`)

### 6️⃣ Recompactar PBIX

```bash
python scripts/pbix_recompactor.py extracted/ relatorio.pbix
```

**O que acontece:**
- JSONs são recompactados
- Novo PBIX gerado com mudanças
- Pronto para publicar

### 7️⃣ Publicar no Workspace

```bash
# No Power BI Service
# Suba o arquivo novo
# Ou abra no Power BI Desktop e publique
```

---

## Exemplo Prático Completo

### Cenário
Você precisa mudar as cores de um relatório de vendas para verde (corporate).

### Comando
```
Claude, neste relatório de vendas:
1. Mude todos os gráficos de azul para verde (#00B050)
2. Mude o card KPI de vermelho para verde
3. Deixe os textos mais escuros para contrastar
```

### O que Claude faz
```
Entendido! Vou:
1. Ler o arquivo layout_pages.json
2. Encontrar todos os elementos com cor azul
3. Mudar para verde #00B050
4. Aumentar contraste dos textos
5. Salvar JSONs atualizados

✓ Concluído! 5 elementos atualizados.
```

### Seu workflow
```bash
# 1. Baixou PBIX
# 2. Descompactou
python scripts/pbix_extractor.py vendas.pbix

# 3. Abriu VSCode
code .

# 4. Solicitou mudança ao Claude (passo acima)

# 5. Revisou no preview (HTML mostra cores novas)

# 6. Recompactou
python scripts/pbix_recompactor.py extracted/ vendas.pbix

# 7. Publicou no Workspace
# Pronto! Relatório com cores novas
```

---

## Dicas de Uso

### ✅ Boas práticas

**Use comandos específicos:**
```
Mude o título do gráfico chamado 'Sales 2024' para 'Revenue 2024'
```

**Não use genéricos:**
```
❌ Mude as cores (muito vago)
```

**Mencione nomes de elementos:**
```
✅ No gráfico 'Monthly Trend', mude a cor da série 'Target' para vermelho
```

**Agrupe mudanças relacionadas:**
```
✅ Atualize o card KPI:
  - Título para 24px
  - Cor de fundo para azul claro
  - Valor em negrito
```

### ⏱️ Tempo por tarefa

- Descompactar PBIX: ~5 segundos
- Solicitar mudança: ~1 minuto
- IA editar: ~30 segundos
- Recompactar: ~5 segundos
- **Total: ~2-3 minutos por mudança** (vs 30 min no Desktop)

### 🔄 Iteração rápida

```bash
# Fluxo otimizado para múltiplas mudanças:

python scripts/pbix_extractor.py relatorio.pbix
code .  # Deixe VSCode aberto

# Solicite mudança 1 ao Claude → aprove
# Solicite mudança 2 ao Claude → aprove
# Solicite mudança 3 ao Claude → aprove

python scripts/pbix_recompactor.py extracted/ relatorio.pbix
# Pronto! Todas as mudanças em um PBIX
```

---

## Quando Usar

### ✅ Bom para:
- Mudar cores de múltiplos gráficos
- Ajustar tamanhos e posições
- Renomear títulos e labels
- Mover elementos de página
- Alterar formatação (fontes, números)

### ❌ Não é para:
- Alterar dados (use Power Query para isso)
- Criar novas medidas DAX (use tabelas semânticas)
- Mudar relacionamentos entre tabelas
- Modificar modelo de dados

---

## Próximos Passos

- Leia **[API.md](API.md)** para saber todas as funções
- Veja **[EXEMPLOS.md](EXEMPLOS.md)** para mais casos reais
- Consulte **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** se tiver erros

---

**Pronto para começar? Vá para [EXEMPLOS.md](EXEMPLOS.md) para ver casos práticos!**
