# Configuração MCP - Microsoft Official Integration

Guia completo para conectar o PowerBI IA com o MCP oficial da Microsoft.

---

## 🎯 O que é MCP?

MCP (Model Context Protocol) é um protocolo padrão que permite que modelos de IA (como Claude) acessem ferramentas e dados externos.

No nosso caso, Claude pode usar MCP para:
- Ler arquivos JSON do seu projeto
- Editar propriedades de visuais
- Validar estrutura de PBIX

---

## 📋 Arquitetura

```
Claude Desktop / VSCode + Copilot
    ↓ (via MCP protocol)
pbir-visual-editor-mcp.js (Node.js)
    ↓ (lê/escreve)
extracted/
├── report/
│   ├── definition/
│   │   └── pages/
│   │       ├── [página1]/visual.json
│   │       ├── [página2]/visual.json
│   │       └── ...
│   └── ...
└── semanticModel/
```

---

## 🔧 INSTALAÇÃO COMPLETA

### Passo 1: Verificar Instalação MCP

```bash
# Você já tem isto (do npm install):
cd PowerBI_IA/mcp
npm list @microsoft/mcp-sdk
```

**Resultado esperado:**
```
@microsoft/mcp-sdk@1.0.0 (ou superior)
```

Se não tiver, instale:
```bash
npm install @microsoft/mcp-sdk
npm install stdio-transport
```

### Passo 2: Configurar Claude Desktop

#### Opção A: Windows

1. Abra arquivo de configuração:
```
C:\Users\[SeuUsuario]\AppData\Roaming\Claude\claude_desktop_config.json
```

2. Se não existir, crie com este conteúdo:
```json
{
  "mcpServers": {
    "pbir-visual-editor": {
      "command": "node",
      "args": ["C:\\Users\\[SeuUsuario]\\PowerBI_IA\\mcp\\pbir-visual-editor-mcp.js"]
    }
  }
}
```

**Substituir:**
- `[SeuUsuario]` pelo seu usuário Windows
- Verificar que o caminho existe

3. Salvar e reiniciar Claude Desktop

#### Opção B: Mac

1. Abra arquivo de configuração:
```
~/.claude/claude_desktop_config.json
```

2. Se não existir, crie com este conteúdo:
```json
{
  "mcpServers": {
    "pbir-visual-editor": {
      "command": "node",
      "args": ["/Users/[SeuUsuario]/PowerBI_IA/mcp/pbir-visual-editor-mcp.js"]
    }
  }
}
```

**Substituir:**
- `[SeuUsuario]` pelo seu usuário Mac

3. Salvar e reiniciar Claude Desktop

#### Opção C: Linux

1. Abra arquivo de configuração:
```
~/.claude/claude_desktop_config.json
```

2. Se não existir, crie com este conteúdo:
```json
{
  "mcpServers": {
    "pbir-visual-editor": {
      "command": "node",
      "args": ["/home/[usuario]/PowerBI_IA/mcp/pbir-visual-editor-mcp.js"]
    }
  }
}
```

**Substituir:**
- `[usuario]` pelo seu usuário Linux

3. Salvar e reiniciar Claude Desktop

---

## ✅ VERIFICAR SE ESTÁ FUNCIONANDO

### Método 1: Claude Desktop

1. Abra Claude Desktop
2. Você verá notificação:
```
✓ MCP Server "pbir-visual-editor" connected
```

3. Feche e abra novamente. A notificação deve aparecer automaticamente.

### Método 2: Testar Manualmente

```bash
cd PowerBI_IA/mcp
node pbir-visual-editor-mcp.js
```

Você verá output similar a:
```
[2026-05-19T21:15:00.000Z] MCP Server started
[2026-05-19T21:15:00.100Z] Listening on stdio
Ready to accept requests
```

Se funcionar, pressione `Ctrl+C` para parar.

### Método 3: Verificar Logs

Se tiver erro, procure por:
```
~/.claude/logs/  (Mac/Linux)
C:\Users\[Usuario]\AppData\Local\Claude\logs\  (Windows)
```

---

## 🚀 PRIMEIRO USO

### 1. Preparar Arquivo PBIX

```bash
# Criar pasta de trabalho
cd PowerBI_IA
mkdir -p pbix extracted

# Colocar seu arquivo PBIX em:
# PowerBI_IA/pbix/seu_relatorio.pbix
```

### 2. Descompactar

```bash
python scripts/pbix_extractor.py pbix/seu_relatorio.pbix
```

**Resultado:**
```
✓ PBIX descompactado
✓ Arquivos extraídos para: ./extracted
```

### 3. Abrir VSCode

```bash
code .
```

### 4. Abrir Claude Desktop

1. Clique no ícone do Claude no dock/taskbar
2. Ou execute: `open /Applications/Claude.app` (Mac)
3. Você verá: ✓ MCP Server "pbir-visual-editor" connected

### 5. Usar MCP para Editar

No Claude Desktop, escreva:

```
Vou editar um relatório Power BI através do MCP.

Primeiro, mostre-me a estrutura das páginas disponíveis.
```

Claude vai:
1. Conectar via MCP
2. Ler pasta `extracted/`
3. Listar páginas disponíveis
4. Mostrar estrutura

---

## 💡 EXEMPLOS DE COMANDOS PARA CLAUDE

### Exemplo 1: Listar Páginas

```
Claude, me mostre todas as páginas disponíveis neste relatório.
Use o MCP para acessar os arquivos.
```

**Claude responde:**
```
Conectei via MCP ao seu projeto.

Páginas encontradas:
1. Dashboard (página principal)
2. Vendas por Região
3. KPIs
4. Detalhes
```

### Exemplo 2: Editar Cores

```
Claude, edite o arquivo:
extracted/report/definition/pages/[página1]/visual.json

Encontre o visual com nome "SalesChart" e mude a propriedade:
"fill": de "#ADD8E6" para "#0078D4"

Use o MCP para salvar as mudanças.
```

**Claude executa via MCP:**
```
✓ Acessei o arquivo via MCP
✓ Encontrei o visual "SalesChart"
✓ Mudei a cor para #0078D4
✓ Arquivo salvo com sucesso
```

### Exemplo 3: Editar Múltiplos Elementos

```
Claude, neste relatório:

1. Página "Dashboard":
   - Gráfico "Sales": mude cor para azul #0078D4
   - Card "Total": aumente fontSize para 20px

2. Página "Vendas por Região":
   - Mapa: mude cor de fundo para branco

Use o MCP para acessar e editar os JSONs.
```

---

## 📁 ESTRUTURA DE ARQUIVOS

### Onde colocar PBIX

```
PowerBI_IA/
├── pbix/                    ← COLOQUE AQUI
│   ├── seu_relatorio.pbix
│   ├── outro_relatorio.pbix
│   └── ...
└── ...
```

### Onde Claude edita

```
PowerBI_IA/
├── extracted/               ← Claude edita aqui (via MCP)
│   ├── report/
│   │   ├── definition/
│   │   │   └── pages/
│   │   │       ├── [página1]/
│   │   │       │   ├── visual.json      ← Edita cores, fontes, etc
│   │   │       │   ├── config.json
│   │   │       │   └── ...
│   │   │       └── [página2]/
│   │   │           ├── visual.json
│   │   │           └── ...
│   │   └── ...
│   ├── semanticModel/       ← Modelo de dados
│   └── ...
└── ...
```

---

## 🔄 FLUXO COMPLETO

```
1. PREPARAR
   ├─ mkdir -p pbix extracted
   ├─ Colocar PBIX em pbix/seu_relatorio.pbix
   └─ Claude Desktop reiniciado

2. DESCOMPACTAR
   └─ python scripts/pbix_extractor.py pbix/seu_relatorio.pbix

3. EDITAR (via MCP)
   ├─ code . (abrir VSCode)
   ├─ Claude Desktop (open no seu MCP)
   ├─ Você: "Claude, mude as cores para azul"
   └─ Claude: (edita via MCP) "✓ Mudado"

4. VERIFICAR
   └─ VSCode mostra JSONs editados

5. RECOMPACTAR
   └─ python scripts/pbix_recompactor.py extracted/ pbix/novo.pbix

6. PUBLICAR
   └─ Abrir pbix/novo.pbix no Power BI Desktop → Publicar
```

---

## 🆘 TROUBLESHOOTING

### Problema: MCP não conecta

**Solução 1: Verificar arquivo de config**
```bash
# Mac/Linux
cat ~/.claude/claude_desktop_config.json

# Windows
type %APPDATA%\Claude\claude_desktop_config.json
```

Procure por:
```json
"mcpServers": {
  "pbir-visual-editor": {
    "command": "node",
    "args": ["/caminho/correto/pbir-visual-editor-mcp.js"]
  }
}
```

**Solução 2: Verificar se Node.js existe**
```bash
which node
node --version  # deve ser v16+
```

**Solução 3: Reiniciar tudo**
```bash
# 1. Feche Claude Desktop completamente
# 2. Abra terminal
# 3. Teste manualmente:
cd PowerBI_IA/mcp
node pbir-visual-editor-mcp.js

# Deve aparecer: "Ready to accept requests"
# Se sim, Ctrl+C e abra Claude Desktop novamente
```

---

### Problema: "pbir-visual-editor-mcp.js não encontrado"

**Solução:**
```bash
# Verifique se arquivo existe
ls -la PowerBI_IA/mcp/pbir-visual-editor-mcp.js

# Se não existir, re-clone o repositório
git clone https://github.com/marcelodcorrea/PowerBI_IA.git
```

---

### Problema: Arquivo PBIX não descompacta

**Solução:**
```bash
# 1. Verifique se é PBIX válido
python scripts/pbix_validator.py pbix/seu_relatorio.pbix

# 2. Tente baixar de novo do Power BI Service
# 3. Se continuar, tente:
unzip -l pbix/seu_relatorio.pbix | head

# Deve mostrar estrutura interna
```

---

## 📊 EXEMPLO COMPLETO (passo a passo)

### Seu objetivo
Mudar as cores de um relatório de azul para verde

### Passo 1: Preparar

```bash
# Terminal
cd PowerBI_IA
mkdir -p pbix extracted

# Colocar arquivo em: pbix/vendas.pbix
# (Baixe do Power BI Service)
```

### Passo 2: Descompactar

```bash
python scripts/pbix_extractor.py pbix/vendas.pbix
```

Resultado:
```
✓ PBIX descompactado
✓ Arquivos extraídos para: ./extracted
```

### Passo 3: Abrir VSCode

```bash
code .
```

### Passo 4: Abrir Claude Desktop

- Clique no ícone Claude
- Aguarde: ✓ MCP Server "pbir-visual-editor" connected

### Passo 5: Solicitar Mudança

**Você escreve no Claude:**
```
Claude, no relatório de vendas que descompactei:

Mude todos os gráficos de azul (#ADD8E6) para verde (#00B050).

Use o MCP para:
1. Acessar os arquivos em extracted/
2. Encontrar todos os elementos azuis
3. Mudar para verde
4. Salvar os arquivos

Comece!
```

### Passo 6: Claude Executa via MCP

Claude:
```
✓ Conectei ao MCP
✓ Acessei extracted/report/definition/pages/
✓ Encontrei 5 gráficos com cor #ADD8E6
✓ Mudei todos para #00B050
✓ Arquivos salvos

Pronto! Agora recompacte o PBIX.
```

### Passo 7: Verificar no VSCode

- VSCode mostra arquivos modificados
- Você vê as mudanças de cor nos JSONs

### Passo 8: Recompactar

```bash
python scripts/pbix_recompactor.py extracted/ pbix/vendas_novo.pbix
```

Resultado:
```
✓ PBIX recompactado
✓ Arquivo: pbix/vendas_novo.pbix
```

### Passo 9: Publicar

```bash
# Abrir no Power BI Desktop
# Ou fazer upload direto no Power BI Service
# Resultado: Relatório com cores verdes!
```

---

## 🎓 ENTENDER MCP

### O que MCP faz no nosso caso

```
Claude (sem MCP):
"Desculpa, não posso acessar seus arquivos"

Claude (com MCP):
"Deixa eu acessar via MCP..."
├─ Abre extracted/report/definition/pages/
├─ Lê todos os visual.json
├─ Encontra elementos
├─ Edita propriedades
├─ Salva arquivos
└─ "✓ Pronto!"
```

### Como Claude acessa via MCP

1. Claude envia: "Leia o arquivo visual.json da página 1"
2. MCP Server (Node.js) recebe
3. MCP Server lê arquivo do disco
4. MCP Server retorna conteúdo a Claude
5. Claude analisa e edita
6. Claude envia: "Salve este conteúdo"
7. MCP Server salva no disco
8. Arquivo atualizado!

---

## ✅ CHECKLIST FINAL

- [ ] Node.js 16+ instalado (`node --version`)
- [ ] `npm install` executado em `mcp/`
- [ ] `claude_desktop_config.json` editado corretamente
- [ ] Caminho no config está correto (sem espaços especiais)
- [ ] Claude Desktop reiniciado
- [ ] Mensagem "MCP Server connected" aparece
- [ ] Arquivo PBIX em `pbix/seu_relatorio.pbix`
- [ ] `python scripts/pbix_extractor.py` executado
- [ ] VSCode aberto (`code .`)
- [ ] Pronto para solicitar mudanças ao Claude!

---

## 📚 Referências

- [MCP Protocol Official](https://modelcontextprotocol.io/)
- [Microsoft MCP SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- Documentação local: [GUIA_RAPIDO_INICIO.md](GUIA_RAPIDO_INICIO.md)

---

**Quando tiver dúvida, releia este guia ou consulte GUIA_RAPIDO_INICIO.md!** 🚀

