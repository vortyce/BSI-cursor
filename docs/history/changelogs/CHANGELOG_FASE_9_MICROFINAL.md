# Changelog - Fase 9 (Microfinal & Consolidação)

## [Backend]
- **Single Profile Mode Centralizado**: A lógica de "perfil único" foi movida integralmente para o `PortfolioService.save_profile()`, garantindo que tanto a API quanto scripts internos (como seeders) respeitem a regra de MVP de perfil único global.
- **Refatoração Cirúrgica**: Simplificação dos endpoints de portfólio para delegar a responsabilidade de persistência e busca ao serviço especializado.

## [Documentação]
- **README_REVIEW.md**: Atualizado para reforçar a arquitetura de "Single Profile" na Fase 9.
- **Microfinal**: Esta entrega representa o fechamento definitivo da Fase 9 com higienização completa e consistência técnica.

## [Pacote de Auditoria]
- **PROJECT_TREE.txt**: Regenerado para refletir com precisão cirúrgica o conteúdo do pacote final, sem caches ou arquivos de ambiente sensíveis.
- **Higiene**: Removidos resquícios de `.env.demo`, `__pycache__` e arquivos temporários.
