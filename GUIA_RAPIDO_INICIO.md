# Guia Rápido de Início - PowerBI IA

Instruções passo a passo para começar a usar o assistente agora.

---

## 🎯 Visão Geral do Fluxo

```
1. Baixar PBIX do Workspace
   ↓
2. Descompactar com Python
   ↓
3. Abrir VSCode + MCP conectado
   ↓
4. Pedir mudanças ao Claude/Copilot
   ↓
5. Recompactar PBIX
   ↓
6. Publicar no Workspace
```

---

## 📋 Pré-requisitos

- ✅ Python 3.8+ instalado
- ✅ Node.js 16+ instalado
- ✅ VSCode instalado
- ✅ Claude Desktop instalado (ou GitHub Copilot no VSCode)
- ✅ Projeto clonado: `git clone https://github.com/marcelodcorrea/PowerBI_IA.git`

---

## 🚀 PASSO 1: Preparar Ambiente

### 1.1 Instalar Dependências Python

```bash
cd PowerBI_IA
pip install -r requirements.txt
```

**O que instala:** Nenhuma dependência externa (Python puro!)

### 1.2 Instalar MCP Server Node.js

```bash
cd mcp
npm install
cd ..
```

**O que instala:** Dependências do MCP Server

### 1.3 Criar Pastas de Trabalho

```bash
mkdir -p pbix extracted
```

- `pbix/` → Coloque seu arquivo PBIX aqui
- `extracted/` → JSONs descompactados (criado automaticamente)

---

## 📥 PASSO 2: Conseguir um Arquivo PBIX

### Opção A: Do Power BI Service

1. Abra https://app.powerbi.com
2. Vá para seu workspace
3. Clique no relatório → ⋯ (três pontos) → Baixar
4. Salve em: `pbix/seu_relatorio.pbix`

### Opção B: Do Power BI Desktop

1. Abra seu relatório no Power BI Desktop
2. Arquivo → Salvar como → Escolha pasta `pbix/`
3. Nomeie como: `seu_relatorio.pbix`

### Opção C: Usar Arquivo de Teste

```bash
# Criar arquivo PBIX de teste (estrutura mínima)
python scripts/pbix_extractor.py pbix/relatorio.pbix 2>/dev/null || \
cp pbix/relatorio.pbix pbix/teste.pbix
```

---

## 🔧 PASSO 3: Descompactar o PBIX

```bash
python scripts/pbix_extractor.py pbix/seu_relatorio.pbix
```

**Resultado esperado:**

```
✓ PBIX descompactado
✓ Arquivos extraídos para: ./extracted
✓ Estrutura:
  ├── report/
  │   ├── definition/
  │   │   └── pages/
  │   │       └── (JSONs dos visuais)
  │   └── ...
  ├── semanticModel/
  └── ...

✅ Sucesso! Pronto para editar com VSCode.
```

---

## 🎨 PASSO 4: Conectar MCP no Claude Desktop

### 4.1 Localizar arquivo de configuração

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Mac/Linux:**
```
~/.claude/claude_desktop_config.json
```

### 4.2 Editar Configuração

Abra o arquivo e adicione o MCP Server:

```json
{
  "mcpServers": {
    "pbir-visual-editor": {
      "command": "node",
      "args": ["C:\\Users\\SeuUsuario\\PowerBI_IA\\mcp\\pbir-visual-editor-mcp.js"]
    }
  }
}
```

**Ajuste o caminho para seu computador!**

### 4.3 Reiniciar Claude Desktop

1. Feche Claude Desktop completamente
2. Abra novamente
3. Você verá notificação: "MCP Server connected"

---

## 🗂️ PASSO 5: Abrir no VSCode

```bash
code .
```

### O que você verá:

```
PowerBI_IA/
├── extracted/               ← Seus JSONs aqui
│   ├── report/
│   │   └── definition/
│   │       └── pages/
│   │           ├── [página1]/
│   │           │   ├── visual.json    ← Edite visuais aqui
│   │           │   └── ...
│   │           └── [página2]/
│   └── semanticModel/      ← Modelo de dados
├── pbix/                    ← Seu PBIX original
├── scripts/                 ← Scripts Python
├── mcp/                     ← MCP Server
└── (outros arquivos)
```

---

## 💬 PASSO 6: Pedir Mudanças ao Claude

### No Claude Desktop, escreva:

```
Claude, no relatório que preparei:

1. Mude o título do gráfico 'Sales' para 'Revenue'
2. Altere a cor de fundo do card KPI para azul (#0078D4)
3. Aumente o tamanho da fonte dos títulos para 18px

Você pode acessar os arquivos via MCP. Faça as mudanças.
```

### O que Claude faz:

1. Conecta via MCP ao seu projeto
2. Lê os JSONs de layout
3. Encontra os elementos
4. Edita as propriedades
5. Salva os arquivos atualizados
6. Avisa quando termina

---

## ✅ PASSO 7: Verificar Mudanças

### No VSCode:

1. Abra `extracted/report/definition/pages/[página]/visual.json`
2. Procure pelas mudanças feitas
3. Os JSONs estarão alterados
4. Você pode ver um preview com HTML (veja abaixo)

### Validar Mudanças:

```bash
python scripts/pbix_validator.py pbix/seu_relatorio.pbix
```

---

## 🔨 PASSO 8: Recompactar PBIX

Após aprovar as mudanças:

```bash
python scripts/pbix_recompactor.py extracted/ pbix/seu_relatorio_novo.pbix
```

**Resultado esperado:**

```
⏳ Recompactando PBIX...
✓ PBIX recompactado
✓ Arquivo: pbix/seu_relatorio_novo.pbix
✓ Tamanho: 512.3 KB

✅ Sucesso! Pronto para publicar.
```

---

## 📤 PASSO 9: Publicar no Workspace

### Opção A: Via Power BI Desktop

1. Power BI Desktop → Abrir
2. Abra `pbix/seu_relatorio_novo.pbix`
3. Power BI Desktop carrega as mudanças
4. Arquivo → Publicar
5. Escolha seu workspace
6. Pronto!

### Opção B: Via Power BI Service

1. Power BI Service → Seu Workspace
2. Upload → Trocar arquivo existente
3. Selecione `pbix/seu_relatorio_novo.pbix`
4. Pronto!

---

## 🔄 CICLO COMPLETO (Exemplo)

```bash
# 1. Descompactar
python scripts/pbix_extractor.py pbix/vendas.pbix

# 2. VSCode
code .

# 3. Claude edita via MCP (vire para Claude Desktop)
# Claude: "Mude as cores para azul corporativo"

# 4. Você aprova as mudanças (revise em VSCode)

# 5. Recompactar
python scripts/pbix_recompactor.py extracted/ pbix/vendas_novo.pbix

# 6. Publicar (abra no Power BI Desktop ou Service)
# Resultado: Relatório com cores atualizadas!
```

---

## 📊 Exemplo Prático: Mudar Cores

### Seu comando para Claude:

```
Claude, neste relatório de vendas:

1. Gráfico 'Monthly Sales': 
   - Mude cor de azul (#ADD8E6) para azul corporativo (#0078D4)
   
2. Card KPI 'Total Revenue':
   - Mude cor de fundo para verde claro (#E8F5E9)
   - Aumentar tamanho fonte para 20px

Use o MCP para acessar os JSONs e fazer as mudanças.
```

### O que Claude retorna:

```
✓ Conectei ao MCP
✓ Encontrei o gráfico 'Monthly Sales' na página 1
✓ Alterei a cor para #0078D4
✓ Encontrei o card 'Total Revenue' na página 1
✓ Mudei cor de fundo para #E8F5E9
✓ Aumentei fontSize para 20px

✅ 3 elementos atualizados com sucesso!
Os arquivos foram salvos.
```

### Então você:

```bash
# Recompacta
python scripts/pbix_recompactor.py extracted/ pbix/vendas_novo.pbix

# Publica
# (Abre no Power BI Desktop e publica)

# Resultado: Cores atualizadas no workspace!
```

---

## 🆘 Troubleshooting

### Erro: "MCP Server não conecta"

```bash
# 1. Verifique o caminho em claude_desktop_config.json
# 2. Reinicie Claude Desktop
# 3. No VSCode, abra terminal e teste:
cd mcp
node pbir-visual-editor-mcp.js
```

### Erro: "PBIX não descompacta"

```bash
# 1. Verifique se é arquivo .pbix válido
# 2. Tente validar:
python scripts/pbix_validator.py pbix/seu_relatorio.pbix

# 3. Se falhar, baixe de novo do Power BI Service
```

### Erro: "JSONs não são encontrados"

```bash
# 1. Confirme que descompactou:
ls -la extracted/report/definition/pages/

# 2. Se não tiver nada, execute novamente:
python scripts/pbix_extractor.py pbix/seu_relatorio.pbix
```

---

## 📚 Próximos Passos

- **Mais exemplos?** Veja [EXEMPLOS.md](EXEMPLOS.md)
- **Entender internals?** Veja [ARQUITETURA.md](ARQUITETURA.md)
- **Erros?** Veja [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Referência de funções?** Veja [API.md](API.md)

---

## ✅ Checklist para Começar

- [ ] Python 3.8+ instalado
- [ ] Node.js 16+ instalado
- [ ] `pip install -r requirements.txt` executado
- [ ] `cd mcp && npm install && cd ..` executado
- [ ] `mkdir -p pbix extracted` executado
- [ ] Arquivo PBIX colocado em `pbix/`
- [ ] claude_desktop_config.json editado com MCP
- [ ] Claude Desktop reiniciado
- [ ] VSCode aberto (`code .`)
- [ ] Pronto para solicitar mudanças ao Claude!

---

**Quando tiver dúvida, releia este guia. Ele cobre 95% dos casos!** 🚀

