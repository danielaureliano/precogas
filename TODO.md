# TODO: Melhorias no PrecoGas

## 🚀 Roadmap (Planejado)

- [ ] **Funcionalidade:** Adicionar suporte a outros estados (parametrização na URL).
- [ ] **Qualidade:** Criar testes automatizados (Unitários e Integração).
- [ ] **CI/CD:** Configurar execução efetiva dos testes no GitHub Actions (workflow criado, falta implementação dos testes).

## ✅ Concluído

### 📄 Documentação
- [x] Padronizar documentação do projeto (README, LICENSE, SECURITY).
- [x] Adicionar instruções de Contribuição, Licença e CI/CD no README.
- [x] Criar guia de execução local e via Docker.

### ⚙️ Backend & Infra
- [x] **Performance:** Implementar lógica de cache com Redis na aplicação Python para evitar downloads/processamentos repetidos.
- [x] Corrigir extração de dados da planilha (considerando cabeçalho na linha 10).
- [x] Implementar fallback automático: busca semanas anteriores se a atual falhar.
- [x] Adicionar orquestração de containers (Docker Compose) para API e Redis.
- [x] Configurar tratamento de SSL para downloads em ambiente de desenvolvimento.