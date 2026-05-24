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
