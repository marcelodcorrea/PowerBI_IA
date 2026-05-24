# Regras do Projeto PowerBI IA

## Arquivo PBIX de Trabalho

**Sempre use o arquivo PBIX mais recente da pasta `pbix/`.**

Antes de qualquer solicitação que envolva extração, modificação ou recompactação de um relatório, identifique o arquivo `.pbix` com a data de modificação mais recente na pasta `pbix/`. Use esse arquivo como base para a operação.

```powershell
# Como identificar o arquivo mais recente
Get-ChildItem "pbix/*.pbix" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
```

Isso vale para:
- Extrações (`pbix_extractor.py`)
- Modificações nos JSONs extraídos
- Recompactações (`pbix_recompactor.py`)

O arquivo de saída ao recompactar deve ser salvo na mesma pasta `pbix/` com um nome descritivo da mudança feita (ex: `Relatorio_amarelo.pbix`, `Relatorio_v2.pbix`).

---

## Template de Visuais e Temas

O projeto suporta um arquivo de template PBIX na pasta `template/`. Quando presente, ele serve como modelo de estilo — paleta de cores, fontes, bordas, temas — para todas as criações e modificações de visuais.

### Passo 1 — Verificar se existe template

**Antes de criar ou modificar qualquer visual**, verifique se há um `.pbix` na pasta `template/`:

```powershell
Get-ChildItem "template/*.pbix" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
```

### Passo 2 — Se o template existir: extrair e analisar

Extraia o template mais recente para `template_extracted/`:

```powershell
python scripts/pbix_extractor.py template/<NomeDoTemplate>.pbix --output-dir ./template_extracted
```

Em seguida, analise o conteúdo extraído para entender o padrão de estilo:

- **Visuais:** leia os `visual.json` em `template_extracted/Report/definition/pages/*/visuals/*/visual.json`
  - Identifique: cores de fundo (`backgroundColor`), cores de borda (`border`), fontes (`fontFamily`, `fontSize`, `fontWeight`), padding, sombra
- **Tema:** leia o arquivo `.json` em `template_extracted/Report/StaticResources/SharedResources/BaseThemes/`
  - Identifique: paleta de cores principal, cores de dados, estilos padrão de texto

### Passo 3 — Aplicar o template como modelo

Ao realizar as alterações solicitadas pelo usuário **no arquivo `pbix/`** (o mais recente):

- **Visuais novos ou modificados:** use as propriedades de estilo do visual equivalente no template (cores, fontes, bordas, padding) como ponto de partida
- **Temas:** replique a paleta e as configurações do tema do template
- **Dados e bindings:** preserve os dados originais do arquivo `pbix/` — o template define apenas o estilo, nunca os dados
- **Layout e posicionamento:** respeite as solicitações do usuário; use o template apenas para estilo visual, não para posição/tamanho

### Passo 4 — Se o template não existir

Se a pasta `template/` estiver vazia ou sem arquivos `.pbix`, siga o fluxo normal de edição sem restrições de estilo de template. Informe o usuário que nenhum template foi detectado e que as mudanças serão aplicadas com base nas solicitações diretas.
