# Exemplo: mascote Tomatinho

- `tomatinho.json`: ficha do personagem
- `tomatinho-cenas.json`: cenas em que ele aparece, na ordem do roteiro
- `tomatinho-prompts.md`: todos os prompts numerados na ordem de execução, gerado com:

```bash
python3 plugins/scroll-master/skills/character-model/scripts/montar_prompt.py exemplos/tomatinho/tomatinho.json --modo sequencia
```
