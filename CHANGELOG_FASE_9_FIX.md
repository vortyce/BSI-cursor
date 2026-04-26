# Changelog - Fase 9 (Fix & Finalization)

## [Backend]
- **Single Profile Mode**: Consolidada a lógica de "perfil único" nos endpoints de API.
- **API**: `get_profile` agora retorna 404 corretamente se não houver perfil salvo, impedindo fluxos fantasmas.
- **PortfolioService**: Adicionada documentação explícita sobre a natureza placeholder da contribuição de `data_quality` no score heurístico.

## [Frontend]
- **Fluxo de Perfil**: Removido o estado de "perfil default" silencioso em memória.
- **UI/UX**: Adicionada tela de "Configuração Necessária" que impede a execução da alocação sem um perfil salvo no banco de dados.
- **Aesthetics**: Refinamento visual do formulário de perfil e mensagens de status.

## [Pacote de Auditoria]
- **Saneamento**: Remoção completa de `.env.demo`, `__pycache__`, arquivos `.pyc` e caches locais.
- **README_REVIEW.md**: Reenquadramento total para a Fase 9 (Alocação).
- **PROJECT_TREE.txt**: Atualizado para refletir o conteúdo real e higienizado do pacote.
