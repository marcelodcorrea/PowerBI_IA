# Guia de Instalação e Uso — PowerBI IA

Tudo que você precisa para instalar e começar a usar o assistente.

---

## Visão Geral do Fluxo

```
1. Instalar dependências
   ↓
2. Configurar MCP no Claude Desktop
   ↓
3. Baixar PBIX do Workspace
   ↓
4. Descompactar com Python
   ↓
5. Pedir mudanças ao Claude
   ↓
6. Recompactar PBIX
   ↓
7. Publicar no Workspace
```

---

## Pré-requisitos

Instale antes de começar:

| Ferramenta | Versão mínima | Download |
|---|---|---|
| Python | 3.8+ | https://python.org |
| Node.js | 16+ | https://nodejs.org |
| VSCode | qualquer | https://code.visualstudio.com |
| Claude Desktop | qualquer | https://claude.ai/download |
| Git | qualquer | https://git-scm.com |

---

## PARTE 1 — Instalação (primeira vez)

### Passo 1: Clonar o repositório

```bash
git clone https://github.com/marcelodcorrea/PowerBI_IA.git
cd PowerBI_IA
```

### Passo 2: Instalar dependências Python

```bash
pip install -r requirements.txt
```

> Os scripts usam apenas bibliotecas padrão do Python (`zipfile`, `json`, `os`) — nenhuma dependência externa obrigatória.

### Passo 3: Instalar dependências Node.js do MCP

```bash
cd mcp
npm install
cd ..
```

### Passo 4: Criar pastas de trabalho

```bash
mkdir pbix
mkdir extracted
mkdir template
mkdir template_extracted
```

- `pbix/` → coloque seus arquivos PBIX aqui
- `extracted/` → JSONs extraídos (criado automaticamente pelo extrator)
- `template/` → coloque aqui um PBIX de template para ser usado como modelo de estilo (opcional)
- `template_extracted/` → conteúdo extraído do template (criado automaticamente)

### Passo 5: Configurar MCP no Claude Desktop

**Windows:** abra `%APPDATA%\Claude\claude_desktop_config.json`
**Mac/Linux:** abra `~/.claude/claude_desktop_config.json`

Adicione o bloco abaixo, ajustando o caminho para o seu computador:

```json
{
  "mcpServers": {
    "pbir-visual-editor": {
      "command": "node",
      "args": ["C:\\caminho\\para\\PowerBI_IA\\mcp\\pbir-visual-editor-mcp.js"]
    }
  }
}
```

Salve o arquivo e **reinicie o Claude Desktop**. Você verá a notificação "MCP Server connected".

> **GitHub Copilot:** siga a documentação do Copilot para conectar MCP Servers externos.

### Passo 6: Verificar instalação

```bash
python --version   # deve retornar 3.8+
node --version     # deve retornar 16+
npm --version      # deve estar instalado

# Teste o MCP Server
cd mcp
node pbir-visual-editor-mcp.js
# Pressione Ctrl+C para sair
cd ..

# Teste o script Python
python scripts/pbix_validator.py --help
```

Se todos os comandos retornarem sem erro, a instalação está completa.

---

## PARTE 2 — Uso no dia a dia

### Passo 7: Obter um arquivo PBIX

**Opção A — Do Power BI Service:**
1. Abra https://app.powerbi.com
2. Vá para seu workspace → clique no relatório → ⋯ → Baixar
3. Salve em `pbix/seu_relatorio.pbix`

**Opção B — Do Power BI Desktop:**
1. Arquivo → Salvar como → pasta `pbix/`

> **Regra do projeto:** sempre use o arquivo `.pbix` com a data de modificação mais recente da pasta `pbix/` como base para qualquer operação.

### Passo 8: Descompactar o PBIX

```bash
python scripts/pbix_extractor.py pbix/seu_relatorio.pbix
```

Resultado esperado:
```
[OK] Arquivos extraídos: XX
[OK] Páginas encontradas: X
[OK] Visuais encontrados: XX
[OK] Extração concluída.
```

### Passo 9: Abrir no VSCode

```bash
code .
```

Estrutura gerada em `extracted/`:
```
extracted/
└── Report/
    └── definition/
        └── pages/
            └── [id-da-pagina]/
                ├── page.json
                └── visuals/
                    └── [id-do-visual]/
                        └── visual.json   ← edite aqui
```

### Passo 10: Pedir mudanças ao Claude

No Claude Desktop (com MCP conectado), descreva o que quer mudar:

```
Claude, no relatório que preparei:
1. Mude a cor de fundo dos cards para azul (#0078D4)
2. Altere o título do gráfico de barras para "Vendas por Região"
3. Aumente a fonte dos títulos para 18pt

Use o MCP para acessar os arquivos e fazer as mudanças.
```

### Passo 11: Recompactar o PBIX

Após aprovar as mudanças nos JSONs:

```bash
python scripts/pbix_recompactor.py ./extracted pbix/seu_relatorio_novo.pbix --original pbix/seu_relatorio.pbix
```

Resultado esperado:
```
[OK] PBIX gerado: pbix/seu_relatorio_novo.pbix (XX KB)
[OK] Concluído. Arquivo pode ser aberto no Power BI Desktop.
```

### Passo 12: Publicar no Workspace

**Opção A — Via Power BI Desktop:**
1. Abra `pbix/seu_relatorio_novo.pbix` no Power BI Desktop
2. Arquivo → Publicar → escolha seu workspace

**Opção B — Via Power BI Service:**
1. Seu workspace → Upload → Trocar arquivo existente
2. Selecione `pbix/seu_relatorio_novo.pbix`

---

## Exemplo Completo

```bash
# 1. Identificar o PBIX mais recente
# Windows:
Get-ChildItem pbix/*.pbix | Sort-Object LastWriteTime -Descending | Select-Object -First 1

# 2. Descompactar
python scripts/pbix_extractor.py pbix/vendas.pbix

# 3. Abrir VSCode
code .

# 4. Pedir mudanças ao Claude Desktop via MCP
# Ex: "Mude todas as cores para o azul corporativo #0078D4"

# 5. Recompactar
python scripts/pbix_recompactor.py ./extracted pbix/vendas_v2.pbix --original pbix/vendas.pbix

# 6. Publicar no Power BI Desktop ou Service
```

---

## Dicas de Uso

### Tempo por operação

| Operação | Tempo estimado |
|---|---|
| Descompactar PBIX | ~5 segundos |
| Solicitar mudança ao Claude | ~1 minuto |
| Claude editar via MCP | ~30 segundos |
| Recompactar PBIX | ~5 segundos |
| **Total por mudança** | **~2–3 minutos** (vs ~30 min no Power BI Desktop) |

### Iteração rápida: várias mudanças, um só recompact

Não é necessário recompactar após cada mudança. Extraia uma vez, peça quantas mudanças quiser ao Claude, recompacte apenas ao final:

```bash
python scripts/pbix_extractor.py pbix/relatorio.pbix
code .

# Mudança 1 → Claude edita via MCP → aprove
# Mudança 2 → Claude edita via MCP → aprove
# Mudança 3 → Claude edita via MCP → aprove

python scripts/pbix_recompactor.py ./extracted pbix/relatorio_v2.pbix --original pbix/relatorio.pbix
# Todas as mudanças consolidadas em um único PBIX
```

## Usando um Template de Estilo

O projeto suporta um arquivo PBIX de template que define a identidade visual dos relatórios — paleta de cores, fontes, bordas, temas.

### Como funciona

1. Coloque um arquivo `.pbix` com o visual desejado na pasta `template/`
2. Nas próximas solicitações, o Claude verificará automaticamente se há um template disponível
3. Se existir, o template será extraído para `template_extracted/` e seu estilo será usado como modelo ao criar ou modificar visuais no arquivo `pbix/`
4. Se não existir, o fluxo normal continua sem restrições de estilo

### Comportamento com template ativo

| O que vem do template | O que vem do arquivo `pbix/` |
|---|---|
| Cores, fontes, bordas | Dados e medidas |
| Tema (paleta de cores) | Bindings de colunas/tabelas |
| Padding, sombra, opacidade | Layout e posicionamento |
| Estilo dos títulos | Filtros e interações |

### Fluxo com template

```
1. Coloque template em template/
   ↓
2. Claude extrai template → template_extracted/
   ↓
3. Claude analisa: cores, fontes, tema
   ↓
4. Extraia o PBIX de trabalho → extracted/
   ↓
5. Peça as mudanças ao Claude
   ↓
6. Claude aplica: estilo do template + dados do pbix/
   ↓
7. Recompacte → novo PBIX em pbix/
```

> **Dica:** o template não precisa ser reextraído a cada sessão. Se `template_extracted/` já estiver preenchido, o Claude usará diretamente os JSONs existentes.

---

## Quando Usar Este Projeto

### Funciona bem para
- Mudar cores de gráficos, cards e fundos de página
- Ajustar tamanhos e posições de visuais
- Renomear títulos e labels
- Alterar fontes (tamanho, peso, família)
- Reorganizar layout de páginas

### Não substitui o Power BI Desktop para
- Alterar dados (requer Power Query)
- Criar ou editar medidas DAX
- Mudar relacionamentos entre tabelas
- Criar novos tipos de visual do zero
- Modificar o modelo semântico

---

## Checklist de Início

- [ ] Python 3.8+ instalado (`python --version`)
- [ ] Node.js 16+ instalado (`node --version`)
- [ ] Repositório clonado (`git clone ...`)
- [ ] `pip install -r requirements.txt` executado
- [ ] `cd mcp && npm install && cd ..` executado
- [ ] Pastas `pbix/` e `extracted/` criadas
- [ ] `claude_desktop_config.json` configurado com caminho do MCP
- [ ] Claude Desktop reiniciado
- [ ] Arquivo PBIX colocado em `pbix/`
- [ ] (Opcional) Arquivo PBIX de template colocado em `template/`
- [ ] Pronto para usar!

---

## Troubleshooting

**"MCP Server não conecta"**
```bash
# Verifique o caminho absoluto em claude_desktop_config.json
# Reinicie o Claude Desktop completamente
cd mcp && node pbir-visual-editor-mcp.js  # deve iniciar sem erro

# Se o erro persistir, verifique os logs do Claude Desktop:
# Windows:    C:\Users\[Usuario]\AppData\Local\Claude\logs\
# Mac/Linux:  ~/.claude/logs/
```

**"Python não encontrado"**
```bash
# Instale Python 3.8+ em https://python.org
# Marque "Add Python to PATH" durante a instalação (Windows)
```

**"Node.js não encontrado"**
```bash
# Instale Node.js 16+ em https://nodejs.org
```

**"PBIX não descompacta"**
```bash
python scripts/pbix_validator.py pbix/seu_relatorio.pbix
# Se falhar, o arquivo pode estar corrompido — baixe novamente do Power BI Service
```

**"JSONs não encontrados após extração"**
```bash
# Confirme que a extração foi concluída:
ls extracted/Report/definition/pages/
# Se vazio, re-execute o extrator
```

---

Para erros que ocorrem **durante o uso** (visual não encontrado, propriedade inválida, PBIX corrompido após recompactar), consulte [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

Para mais detalhes: [EXEMPLOS.md](EXEMPLOS.md) | [ARQUITETURA.md](ARQUITETURA.md) | [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
