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
✅ IA edita JSONs de layout
✅ ~2 minutos por mudança
✅ Tudo versionado em Git
```

---

## ⚡ Quick Start (5 minutos)

### 1. Instalar dependências
```bash
pip install -r requirements.txt
npm install  # na pasta mcp/
```

### 2. Usar no dia a dia
```bash
# Descompacta PBIX
python scripts/pbix_extractor.py relatorio.pbix

# VSCode abre, você edita com IA
# (Node.js MCP conecta aos JSONs)

# Recompacta PBIX
python scripts/pbix_recompactor.py extracted/ relatorio.pbix

# Sobe no Workspace
```

---

## 📋 Documentação

- **[SETUP.md](SETUP.md)** - Instalação passo a passo
- **[FLUXO.md](FLUXO.md)** - Como usar no dia a dia
- **[API.md](API.md)** - Funções disponíveis
- **[EXEMPLOS.md](EXEMPLOS.md)** - Casos de uso reais
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Erros comuns
- **[ARQUITETURA.md](ARQUITETURA.md)** - Como funciona (técnico)
- **[CHANGELOG.md](CHANGELOG.md)** - Histórico de versões

---

## 🏗️ Estrutura do Projeto

```
PowerBI_IA/
├── scripts/
│   ├── pbix_extractor.py       # Descompacta PBIX
│   ├── pbix_recompactor.py     # Recompacta PBIX
│   └── pbix_validator.py       # Valida integridade
├── mcp/
│   ├── pbir-visual-editor-mcp.js  # Node.js MCP Server
│   └── package.json
├── README.md                    # Este arquivo
├── SETUP.md                     # Instalação
├── FLUXO.md                     # Como usar
├── API.md                       # Funções
├── EXEMPLOS.md                  # Casos reais
├── TROUBLESHOOTING.md           # Erros
├── ARQUITETURA.md               # Internals
├── CHANGELOG.md                 # Histórico
├── requirements.txt             # Dependências Python
└── .env.example                 # Variáveis de ambiente
```

---

## 🔧 Tecnologia

- **Python 3.8+** - Descompacta/recompacta PBIX
- **Node.js 16+** - MCP Server para edição de layout
- **Claude ou GitHub Copilot** - IA para editar
- **VSCode** - Editor principal

---

## 🚀 Próximos Passos

1. Leia **[SETUP.md](SETUP.md)** para instalar
2. Siga **[FLUXO.md](FLUXO.md)** para usar
3. Veja **[EXEMPLOS.md](EXEMPLOS.md)** para inspiração

---

## 💡 Exemplo Real

```
Você: "Claude, mude o título do gráfico de 'Vendas' para 'Receita'"

Claude executa via MCP:
├─ Lê arquivos JSON de layout
├─ Encontra o gráfico chamado 'Vendas'
├─ Muda o título para 'Receita'
└─ Arquivo JSON atualizado em tempo real

Você: "Aprova" via VSCode

Resultado: Novo PBIX com mudança, pronto para subir
```

---

## 📝 Licença

Use como quiser. Sem restrições.

---

## 🤝 Suporte

Dúvidas? Consulte:
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** para erros comuns
- **[ARQUITETURA.md](ARQUITETURA.md)** para entender o internals

---

**Made for Data Analysts | Powered by Claude AI**
