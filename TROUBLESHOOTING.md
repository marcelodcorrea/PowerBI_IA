# Troubleshooting - Erros Comuns

Soluções para problemas comuns.

---

## Erro: "No module named 'zipfile'"

**Causa:** Dependências Python não instaladas.

**Solução:**
```bash
pip install -r requirements.txt
```

---

## Erro: "PBIX não descompacta"

**Causa:** Arquivo não é PBIX válido.

**Solução:**
1. Verifique se é arquivo `.pbix` correto
2. Tente com outro arquivo PBIX
3. Valide o arquivo:
```bash
python scripts/pbix_validator.py seu_arquivo.pbix
```

---

## Erro: "MCP Server não conecta"

**Causa:** Configuração incorreta do MCP no Claude Desktop.

**Solução:**
1. Verifique path em `~/.claude/claude_desktop_config.json`
2. Reinicie Claude Desktop
3. Teste manualmente:
```bash
cd mcp && node pbir-visual-editor-mcp.js
```

---

## Erro: "Node.js não encontrado"

**Causa:** Node.js não instalado.

**Solução:**
```bash
# Instale Node.js 16+ em https://nodejs.org
node --version  # deve ser v16+
```

---

## Erro: "Visual não encontrado"

**Causa:** Nome do visual está incorreto.

**Solução:**
1. Liste todos os visuais via Claude:
```
Claude, liste todos os visuais da página 'Dashboard'
```

2. Use o nome exato que Claude retornar

---

## Erro: "Propriedade inválida"

**Causa:** Tentou mudar propriedade que não existe.

**Solução:**
1. Consult API.md para propriedades válidas
2. Use propriedades suportadas:
   - `fill` (cor de fundo)
   - `fontSize` (tamanho fonte)
   - `stroke` (cor borda)
   - etc.

---

## Erro: "Arquivo PBIX corrompido após recompactar"

**Causa:** JSONs malformados durante edição.

**Solução:**
1. Restaure do backup em `docs_backup/`
2. Comece novamente
3. Use git para versionar:
```bash
git add extracted/
git commit -m "edições de layout"
```

---

## Erro: "Claude não consegue conectar ao MCP"

**Causa:** MCP Server não está respondendo.

**Solução:**
1. Reinicie Claude Desktop
2. Verifique se Node.js está rodando:
```bash
ps aux | grep node
```

3. Se não estiver, teste manualmente:
```bash
cd mcp && npm test
```

---

## Dica: Usar Git para Recuperação

Se algo deu errado, use Git:

```bash
# Ver mudanças
git diff extracted/

# Descartar mudanças ruins
git checkout extracted/

# Restaurar versão anterior
git log --oneline extracted/
git checkout <commit-hash> -- extracted/
```

---

## Dica: Testar Antes de Recompactar

Sempre revise os JSONs antes de recompactar:

```bash
# Verifique os arquivos alterados
git status extracted/

# Veja o diff
git diff extracted/

# Se tiver erro, desfaça:
git checkout extracted/
```

---

## Próximos Passos

- Releia **[FLUXO.md](FLUXO.md)** para começar de novo
- Consulte **[API.md](API.md)** para propriedades válidas
- Veja **[ARQUITETURA.md](ARQUITETURA.md)** para entender internals

