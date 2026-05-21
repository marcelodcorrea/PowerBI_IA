# PowerBI IA — Assistente para Editar Arquivos Power BI

Edite arquivos Power BI (`.pbix`) via VSCode com auxilio de IA, sem abrir o Power BI Desktop.
O fluxo: extrair o PBIX, editar os `visual.json` com Claude, recompactar o PBIX.

---

## Pre-requisitos

- Python 3.8 ou superior
- Node.js 16 ou superior
- VSCode com extensao Claude Code (MCP)
- Git

---

## Instalacao

```bash
git clone https://github.com/marcelodcorrea/PowerBI_IA.git
cd PowerBI_IA
pip install -r requirements.txt
cd mcp && npm install && cd ..
cp .env.example .env.local
```

Nao ha dependencias Python externas. Os scripts usam apenas bibliotecas da biblioteca padrao.

---

## Como usar

### 1. Coloque o arquivo .pbix na pasta `pbix/`

```
PowerBI_IA/
└── pbix/
    └── MeuRelatorio.pbix   <- cole aqui
```

### 2. Extraia o PBIX

```bash
python scripts/pbix_extractor.py pbix/MeuRelatorio.pbix
```

Os arquivos JSON serao extraidos para `extracted/`.

### 3. Edite com Claude no VSCode

Abra o VSCode na pasta do projeto. Solicite mudancas ao Claude:

```
"Mude a cor dos cards KPI para #FF6600"
"Mova o grafico de barras 50 pixels para baixo"
"Altere o titulo da pagina para 'Resumo Executivo'"
```

Claude usa as ferramentas MCP para ler e editar os `visual.json` em `extracted/`.

### 4. Recompacte o PBIX

```bash
python scripts/pbix_recompactor.py extracted/ pbix/MeuRelatorio_editado.pbix --original pbix/MeuRelatorio.pbix
```

O arquivo gerado pode ser aberto diretamente no Power BI Desktop.

---

## Scripts disponiveis

| Script | Descricao | Uso |
|--------|-----------|-----|
| `pbix_extractor.py` | Descompacta PBIX em arquivos JSON | `python scripts/pbix_extractor.py pbix/arquivo.pbix` |
| `pbix_recompactor.py` | Recompacta JSONs editados em PBIX valido | `python scripts/pbix_recompactor.py extracted/ saida.pbix --original original.pbix` |
| `pbix_info.py` | Inspeciona PBIX sem extrair (paginas, visuais, status) | `python scripts/pbix_info.py pbix/arquivo.pbix` |
| `pbix_validator.py` | Valida integridade basica de um PBIX | `python scripts/pbix_validator.py pbix/arquivo.pbix` |

---

## Estrutura de pastas

```
PowerBI_IA/
├── pbix/                          # Cole os .pbix aqui (ignorados pelo Git)
│   └── .gitkeep
├── extracted/                     # Arquivos extraidos (ignorados pelo Git)
│   └── .gitkeep
├── scripts/
│   ├── pbix_extractor.py
│   ├── pbix_recompactor.py
│   ├── pbix_info.py
│   └── pbix_validator.py
├── mcp/
│   ├── pbir-visual-editor-mcp.js
│   └── package.json
├── requirements.txt
├── .env.example
└── README.md
```

---

## Nota sobre SecurityBindings

O arquivo `SecurityBindings` dentro do PBIX contem uma assinatura criptografica DPAPI
(Data Protection API do Windows) gerada pelo Power BI Desktop no momento do salvamento.
Essa assinatura e um hash do conteudo dos arquivos do relatorio.

Ao modificar qualquer `visual.json` externamente, o hash original deixa de ser valido.
Se o `SecurityBindings` nao for zerado, o Power BI Desktop exibe:

> "Nao foi possivel abrir o documento — Esse arquivo esta corrompido ou foi criado por
> uma versao nao reconhecida de Power BI Desktop."

O script `pbix_recompactor.py` zera automaticamente o `SecurityBindings` (`b''`).
O Power BI Desktop abre o arquivo normalmente sem essa assinatura — ela e opcional
para leitura, obrigatoria apenas para validacao DRM.

---

## Troubleshooting

| Erro | Causa | Solucao |
|------|-------|---------|
| `UnicodeEncodeError: 'charmap' codec can't encode character` | Windows com terminal em encoding nao-UTF8, versao antiga dos scripts com emojis | Atualize para a versao atual dos scripts (sem emojis). Alternativa: `set PYTHONUTF8=1` antes de executar |
| `"Arquivo corrompido"` no Power BI Desktop | `SecurityBindings` nao foi zerado | Use sempre `--original` no `pbix_recompactor.py`; o script zera automaticamente |
| `DataModel` parece corrompido | Compressao errada ao recompactar | O script ja corrige: `DataModel` e salvo como `ZIP_STORED` (sem compressao) |
| `[ERRO] Arquivo nao encontrado` | Caminho errado ou arquivo nao copiado para `pbix/` | Verifique se o `.pbix` esta em `pbix/` e o caminho esta correto |
| `[ERRO] nao e um arquivo PBIX valido` | Arquivo corrompido ou nao e um PBIX | Verifique se o arquivo abre normalmente no Power BI Desktop |
| Modificacoes nao aparecem no PBIX gerado | Arquivos editados em diretorio diferente do informado | Confirme que `extracted_dir` aponta para o mesmo diretorio onde os JSONs foram editados |

---

## Como funciona (resumo tecnico)

1. Um arquivo `.pbix` e um ZIP renomeado com estrutura proprietaria do Power BI
2. Os visuais de cada pagina ficam em `Report/definition/pages/<guid>/visuals/<guid>/visual.json`
3. Python extrai o ZIP, preservando todos os metadados dos entries
4. Claude edita os `visual.json` via MCP (Model Context Protocol)
5. Python recompacta usando os `ZipInfo` originais (`writestr(item, data)`) para preservar
   `create_version`, `flag_bits` e demais campos que o Power BI valida
6. `SecurityBindings` e zerado para invalidar a assinatura DPAPI que nao refletiria mais o conteudo
7. `DataModel` e adicionado por ultimo com `ZIP_STORED` (comportamento do Power BI Desktop)
