# Changelog - Fase 5: Pacote Final de Auditoria

## [v5.0.0-audit-clean] - 2026-04-23

### Saneamento e Higiene
- Remoção de arquivos `.env` reais, mantendo apenas `.env.example`.
- Exclusão de diretórios `__pycache__`, arquivos `.pyc` e caches de ambiente local.
- Limpeza de diretórios `node_modules` e artefatos de build temporários.
- Remoção do banco de dados local `bsi_demo.db` para garantir que o auditor execute o seed manualmente conforme instruído.

### Documentação
- Revisão do `README_REVIEW.md` para uma linguagem tecnicamente honesta e sóbria.
- Criação de `OPEN_ISSUES.md` listando limitações conhecidas do MVP.
- Criação de `NEXT_STEPS.md` detalhando o roadmap técnico pós-Fase 5.
- Atualização do `PROJECT_TREE.txt` para refletir exatamente a estrutura do pacote de auditoria.
