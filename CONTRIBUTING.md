# Guia de Contribuição

## Estratégia de Branches

Este projeto segue um fluxo simplificado baseado em **Feature Branches** e **Trunk-Based Development**:

*   **`main`**: Branch estável de produção. O código nesta branch deve estar sempre pronto para deploy.
    *   **Proteção:** Não deve receber commits diretos (exceto admins em correções emergenciais). Alterações entram via Pull Request.
    *   **Deploy:** Commits na `main` disparam o deploy automático no Render.com.

*   **Branches de Desenvolvimento:**
    *   `feat/nome-da-feature`: Para novas funcionalidades.
    *   `fix/nome-do-bug`: Para correções de erros.
    *   `docs/nome-da-doc`: Para alterações em documentação.
    *   `chore/nome-da-tarefa`: Para manutenção, dependências e configurações.
    *   `refactor/nome-da-refatoracao`: Para melhorias de código sem mudança de comportamento.

## Fluxo de Trabalho

1.  **Sincronize:** `git checkout main && git pull origin main`
2.  **Crie uma Branch:** `git checkout -b feat/nova-funcionalidade`
3.  **Desenvolva:** Faça suas alterações.
4.  **Verifique Localmente:** O `pre-commit` rodará automaticamente no commit. Você também pode rodar `pytest` manualmente.
5.  **Commite:** Use **Conventional Commits** (ex: `feat: adiciona endpoint de health check`).
6.  **Push:** `git push origin feat/nova-funcionalidade`
7.  **Pull Request:** Abra um PR no GitHub para a `main`.
8.  **CI/CD:** Aguarde os testes automatizados (GitHub Actions) passarem.
9.  **Merge:** Após aprovação, faça o merge (Squash and Merge é recomendado).

## Padrões de Código

*   **Python:** Seguir PEP 8.
*   **Linting:** `ruff` é usado para garantir estilo.
*   **Tipagem:** Use Type Hints sempre que possível.
