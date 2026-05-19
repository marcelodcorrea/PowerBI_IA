# Instalação e Configuração

Guia passo a passo para começar a usar o PowerBI IA.

---

## Pré-requisitos

- **Python 3.8+** instalado
- **Node.js 16+** instalado
- **VSCode** instalado
- **Claude Desktop** ou **GitHub Copilot** no VSCode
- **Git** para versionamento

---

## Instalação (10 minutos)

### Passo 1: Clonar o repositório

```bash
git clone https://github.com/marcelodcorrea/PowerBI_IA.git
cd PowerBI_IA
```

### Passo 2: Instalar dependências Python

```bash
pip install -r requirements.txt
```

**O que instala:**
- `zipfile` - para descompactar PBIX
- `json` - para editar JSONs
- Outras dependências necessárias

### Passo 3: Instalar dependências Node.js

```bash
cd mcp
npm install
cd ..
```

**O que instala:**
- `@microsoft/mcp-sdk` - para MCP Server
- `stdio-transport` - para comunicação

### Passo 4: Configurar VSCode + MCP

**Se usa Claude Desktop:**

1. Abra: `~/.claude/claude_desktop_config.json` (Mac/Linux)
   ou `%APPDATA%/Claude/claude_desktop_config.json` (Windows)

2. Adicione (substitua `seu_caminho` pelo caminho real):

```json
{
  "mcpServers": {
    "pbir-visual-editor": {
      "command": "node",
      "args": ["seu_caminho/PowerBI_IA/mcp/pbir-visual-editor-mcp.js"]
    }
  }
}
```

3. Salve e reinicie Claude Desktop

**Se usa GitHub Copilot:**

Siga a documentação do Copilot para conectar MCP Servers.

### Passo 5: Copiar arquivo de exemplo de variáveis

```bash
cp .env.example .env.local
```

**Edite `.env.local` com seus valores:**
```
PBIX_INPUT_DIR=./pbix/
PBIX_EXTRACT_DIR=./extracted/
PBIX_OUTPUT_DIR=./pbix/
```

---

## Teste de Instalação

Verifique se tudo está funcionando:

```bash
# Teste Python
python --version  # deve ser 3.8+

# Teste Node.js
node --version    # deve ser 16+

# Teste npm
npm --version     # deve estar instalado

# Teste MCP Server
cd mcp && npm test && cd ..

# Teste script Python
python scripts/pbix_validator.py
```

---

## Próximos Passos

Depois de instalar:

1. Leia **[FLUXO.md](FLUXO.md)** para entender o dia a dia
2. Veja **[EXEMPLOS.md](EXEMPLOS.md)** para casos reais
3. Comece a usar!

---

## Troubleshooting

### Erro: "Python não encontrado"
```bash
# Instale Python 3.8+ em https://python.org
```

### Erro: "Node.js não encontrado"
```bash
# Instale Node.js 16+ em https://nodejs.org
```

### Erro: "MCP Server não conecta"
```bash
# Reinicie Claude Desktop
# Verifique o caminho em claude_desktop_config.json
```

### Erro: "PBIX não descompacta"
```bash
# Verifique se o arquivo é PBIX válido
# Tente novamente com arquivo diferente
```

---

**Pronto! Agora você pode usar o PowerBI IA.**

Leia [FLUXO.md](FLUXO.md) para começar.
