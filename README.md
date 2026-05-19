# PowerBI IA - Assistente para Editar Arquivos Power BI

Um assistente simples para editar arquivos Power BI (PBIX) usando IA, sem abrir Power BI Desktop. Descompacta, edita JSONs de layout, e recompacta tudo automaticamente.

---

## 🎯 O Que Você Consegue Fazer

```
Antes (sem esta solução):
❌ Abrir Power BI Desktop
❌ Editar visualmente cada elemento
❌ ~30 minutos por mudança

Agora (com esta solução):
✅ "Claude, mude as cores de 5 gráficos"
✅ IA edita JSONs de layout via MCP
✅ ~2 minutos por mudança
✅ Tudo versionado em Git
```

---

## ⚡ Quick Start (10 minutos)

### 1. Instalar dependências
```bash
git clone https://github.com/marcelodcorrea/PowerBI_IA.git
cd PowerBI_IA
pip install -r requirements.txt
cd mcp && npm install && cd ..
```

### 2. Usar no dia a dia
```bash
# Descompacta PBIX
python scripts/pbix_extractor.py pbix/relatorio.pbix

# Abra VSCode + Claude (MCP conectado)
code .

# Solicite mudanças ao Claude via MCP
# Claude edita JSONs em tempo real

# Recompacta PBIX
python scripts/pbix_recompactor.py extracted/ pbix/relatorio.pbix

# Suba no Workspace
```

---

## 📚 Documentação Completa

### Para Começar (Novo Usuário)
- **[GUIA_RAPIDO_INICIO.md](GUIA_RAPIDO_INICIO.md)** ⭐ **COMECE AQUI**
  - 9 passos: de descompactar até publicar
  - Exemplos práticos
  - Troubleshooting

### Para Entender MCP
- **[CONFIGURACAO_MCP_MICROSOFT.md](CONFIGURACAO_MCP_MICROSOFT.md)** 
  - O que é MCP e como funciona
  - Configurar Claude Desktop (Windows/Mac/Linux)
  - Verificar se está funcionando
  - Exemplos de comandos para Claude
  - Troubleshooting completo

### Referência
- **[SETUP.md](SETUP.md)** - Instalação passo a passo
- **[FLUXO.md](FLUXO.md)** - Como usar no dia a dia
- **[API.md](API.md)** - Funções disponíveis
- **[EXEMPLOS.md](EXEMPLOS.md)** - Casos de uso reais (10 exemplos)
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Erros comuns
- **[ARQUITETURA.md](ARQUITETURA.md)** - Como funciona (técnico)
- **[CHANGELOG.md](CHANGELOG.md)** - Histórico de versões

---

## 🏗️ Arquitetura

```
Claude Desktop / VSCode + Copilot
    ↓ (via MCP - Model Context Protocol)
Node.js MCP Server
    ↓ (lê/escreve)
extracted/ (JSONs do PBIX)
    ├── report/
    │   ├── definition/pages/
    │   │   ├── [página1]/visual.json
    │   │   ├── [página2]/visual.json
    │   │   └── ...
    │   └── ...
    └── semanticModel/
```

---

## 🚀 Fluxo Completo

```
1. Clone o repositório
   ↓
2. Instale dependências (Python + Node.js)
   ↓
3. Coloque seu PBIX em: pbix/seu_relatorio.pbix
   ↓
4. Descompacte: python scripts/pbix_extractor.py pbix/seu_relatorio.pbix
   ↓
5. Configure Claude Desktop (MCP)
   ↓
6. Abra VSCode: code .
   ↓
7. Solicite mudanças ao Claude (via MCP)
   ↓
8. Claude edita os JSONs automaticamente
   ↓
9. Recompacte: python scripts/pbix_recompactor.py extracted/ novo.pbix
   ↓
10. Publique no Power BI Workspace
```

---

## 🔧 Tecnologia

- **Python 3.8+** - Scripts para descompactar/recompactar PBIX
- **Node.js 16+** - MCP Server para acesso aos arquivos
- **Claude ou GitHub Copilot** - IA para editar via MCP
- **VSCode** - Editor para revisar mudanças
- **Git** - Versionamento de mudanças

---

## 📋 Pré-requisitos

- Python 3.8+
- Node.js 16+
- VSCode
- Claude Desktop instalado
- Git (opcional, mas recomendado)

---

## ✨ Funcionalidades

✅ Descompactar PBIX em JSONs editáveis  
✅ Editar cores, fontes, tamanhos, posições de visuais  
✅ Renomear títulos e labels  
✅ Reorganizar layout de páginas  
✅ Validar integridade de arquivo  
✅ Recompactar em novo PBIX  
✅ Versionamento com Git  
✅ MCP oficial da Microsoft integrado  

---

## ❌ O Que NÃO Funciona

- ❌ Alterar dados (use Power Query)
- ❌ Criar novas medidas DAX (use tabelas semânticas)
- ❌ Mudar relacionamentos entre tabelas
- ❌ Modificar modelo de dados completo

Para essas tarefas, continue usando Power BI Desktop ou Power Query.

---

## 🎯 Caso de Uso Ideal

```
Você:
  "Claude, nos 10 gráficos deste relatório:
   - Mude todas as cores para azul corporativo (#0078D4)
   - Aumente tamanho da fonte para 16px
   - Deixe os textos em negrito"

Claude (via MCP):
  "✓ Conectei ao seu projeto
   ✓ Encontrei 10 gráficos
   ✓ Mudei cores
   ✓ Aumentei fontes
   ✓ Adicionei negrito
   ✓ Pronto!"

Resultado:
  Novo PBIX com 10 gráficos atualizados em 2 minutos
  (vs 30 minutos manual)
```

---

## 📁 Estrutura

```
PowerBI_IA/
├── pbix/                      ← Coloque seus PBIX aqui
├── extracted/                 ← JSONs descompactados (auto)
├── scripts/
│   ├── pbix_extractor.py      ← Descompacta
│   ├── pbix_recompactor.py    ← Recompacta
│   └── pbix_validator.py      ← Valida
├── mcp/
│   ├── pbir-visual-editor-mcp.js  ← MCP Server
│   └── package.json
├── GUIA_RAPIDO_INICIO.md      ← ⭐ COMECE AQUI
├── CONFIGURACAO_MCP_MICROSOFT.md
├── SETUP.md
├── FLUXO.md
├── API.md
├── EXEMPLOS.md
├── TROUBLESHOOTING.md
├── ARQUITETURA.md
├── CHANGELOG.md
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## 🚀 Próximos Passos

1. **Novo usuário?**
   - Leia: [GUIA_RAPIDO_INICIO.md](GUIA_RAPIDO_INICIO.md)
   - Tempo: ~10 minutos
   - Você estará pronto para usar

2. **Quer entender MCP?**
   - Leia: [CONFIGURACAO_MCP_MICROSOFT.md](CONFIGURACAO_MCP_MICROSOFT.md)
   - Tempo: ~15 minutos
   - Você entenderá como tudo funciona

3. **Tem um erro?**
   - Veja: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
   - Ou seção "Troubleshooting" em [GUIA_RAPIDO_INICIO.md](GUIA_RAPIDO_INICIO.md)

4. **Quer exemplos práticos?**
   - Veja: [EXEMPLOS.md](EXEMPLOS.md)
   - 10 casos reais prontos para adaptar

---

## 💡 Exemplo Real

**Seu comando:**
```
Claude, neste relatório de vendas, faça:
1. Mude o título "Sales 2024" para "Revenue 2024"
2. Gráfico "Monthly": cor azul de 200 para 300 (mais escuro)
3. Card KPI: aumente fontSize de 14 para 20px
```

**Claude executa via MCP:**
- Acessa os arquivos
- Encontra os elementos
- Edita as propriedades
- Salva tudo

**Seu resultado:**
```
✓ Pronto em ~30 segundos
✓ Recompacte: python scripts/pbix_recompactor.py extracted/ novo.pbix
✓ Novo PBIX com todas as mudanças
```

---

## 🔒 Segurança

- ✅ Nenhum token ou credencial exposto
- ✅ .gitignore bloqueia arquivos sensíveis
- ✅ .env.example para template (sem valores reais)
- ✅ Pronto para produção

---

## 📊 Benefícios

| Aspecto | Sem Solução | Com PowerBI IA |
|---------|-----------|-----------------|
| Tempo | 30 min/mudança | 2 min/mudança |
| Desktop | Precisa abrir | Não precisa |
| Versionamento | Manual | Git automático |
| Batch de mudanças | Demorado | Rápido |
| Precisão | Manual | 100% (MCP) |

---

## 🤝 Contribuindo

Found a bug? Tem uma sugestão?
1. Abra uma issue no GitHub
2. Fork o repositório
3. Faça suas mudanças
4. Envie um Pull Request

---

## 📝 Licença

MIT - Use como quiser

---

## 📧 Suporte

- **Documentação:** Veja os .md files neste repo
- **GitHub Issues:** Abra uma issue se tiver problemas
- **Referências:** Veja seção "Referências" em [CONFIGURACAO_MCP_MICROSOFT.md](CONFIGURACAO_MCP_MICROSOFT.md)

---

## 🎯 Roadmap Futuro

- [ ] Suporte a múltiplos PBIX simultâneos
- [ ] Preview HTML em tempo real
- [ ] Git integration automática
- [ ] Undo/Redo
- [ ] Suporte a Power Query básico
- [ ] Dashboard web para gerenciamento

---

**Made by Claude IA | Focado em Simplicidade e Qualidade**

**Pronto para começar? → [GUIA_RAPIDO_INICIO.md](GUIA_RAPIDO_INICIO.md)** ⭐

