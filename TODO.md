# Roadmap e Tarefas (TODO)

## Em Andamento
  Relatório de Análise e Adoção de Boas Práticas
  De: projeto_rpg_analise_postural | Para: precogas

  Este relatório identifica diretrizes avançadas e fluxos de trabalho rigorosos presentes no projeto de análise postural (RPG) que são recomendados para serem integrados ao precogas para aumentar a maturidade do
  software, a rastreabilidade e a eficiência do desenvolvimento.

  1. Diretrizes de Engenharia de Software

  Princípios e Robustez
   * Verificação Explícita de Recursos (Hardware Check):
       * Prática RPG: O projeto RPG realiza verificações explícitas de hardware (GPU/CUDA) no início da execução.
       * Aplicação no PrecoGas: Implementar um "Startup Check" robusto no main.py ou downloader.py. Antes de iniciar a API ou o worker, o sistema deve verificar explicitamente:
           1. A conectividade com a internet (para baixar dados da ANP).
           2. A disponibilidade do servidor Redis.
           3. A existência e permissões de escrita nos diretórios temporários.
       * Benefício: Falhar rápido ("Fail Fast") com mensagens de erro claras ao invés de estourar exceções em tempo de execução.

  Manipulação de Arquivos
   * Uso de `pathlib`:
       * Prática RPG: Exige o uso da biblioteca pathlib para toda manipulação de caminhos, garantindo compatibilidade entre SOs.
       * Aplicação no PrecoGas: Refatorar o extractor.py e downloader.py para substituir manipulações de string (os.path.join) por objetos Path do pathlib.

  2. Padrões de Código e Linguagem

  Otimização e Performance
   * Vetorização (NumPy/Pandas):
       * Prática RPG: Proíbe loops Python para cálculos em séries temporais, exigindo vetorização.
       * Aplicação no PrecoGas: No módulo extractor.py, garantir que a limpeza e transformação dos dados da planilha da ANP (ETL) utilizem estritamente funções vetorizadas do Pandas, evitando iterações (iterrows
         ou loops for) para performance máxima, especialmente se o volume de dados históricos crescer.

  Estilo de Interação do Agente
   * Abordagem "Code-First":
       * Prática RPG: O agente deve fornecer o código funcional antes da explicação teórica.
       * Aplicação no PrecoGas: Adotar essa diretriz no GEMINI.md do PrecoGas. Isso torna as interações de manutenção mais eficientes e diretas.

  3. Controle de Versão (Git) e Fluxo de Trabalho

  Sincronização de Dependências (Crítico)
   * Prática RPG: Exige verificação e atualização do requirements.txt antes de qualquer commit que altere scripts.
   * Aplicação no PrecoGas: Integrar essa regra rígida. Atualmente, dependências desatualizadas são uma causa comum de falhas em CI/CD. O agente deve proativamente verificar se novos imports exigem atualização
     do arquivo de dependências antes de sugerir o commit.

  Documentação Contínua
   * Prática RPG: Exige atualização do README.md, CHANGELOG.md e RESUMO_PROGRESSO.md antes do commit, e não apenas em releases.
   * Aplicação no PrecoGas: Adotar a atualização atômica da documentação. Se uma feature mudou a forma como o endpoint /precos funciona, o README deve ser atualizado no mesmo commit ou PR da mudança de código,
     garantindo que a documentação nunca fique obsoleta.

  Estratégia de Branches
   * Prática RPG: Define explicitamente main (estável), develop (integração) e feature/*.
   * Aplicação no PrecoGas: Formalizar o fluxo. Sair do modelo genérico para um modelo onde main é intocável diretamente e reflete o código em produção, enquanto desenvolvimento ocorre em branches específicas.

  4. CI/CD e Observabilidade

  Logging Estruturado e Métricas
   * Prática RPG: Sistema de log personalizado (log_utils.py) que registra tempos de execução e timestamps para cada etapa do pipeline.
   * Aplicação no PrecoGas:
       * Implementar logs estruturados (JSON logs) no app/services/.
       * Registrar métricas chave nos logs: "Tempo de download da planilha ANP", "Tempo de processamento ETL", "Tamanho do arquivo processado". Isso facilitará a depuração futura e monitoramento de performance.

  5. Estrutura e Configuração do Projeto

  Configuração Externa (YAML vs .Env)
   * Prática RPG: Uso de arquivos YAML para configurações complexas de dataset e treino.
   * Aplicação no PrecoGas: Se a lógica de extração da ANP se tornar complexa (muitas regras de colunas, mapeamentos de nomes de cidades), mover essas regras "hardcoded" do código Python para um arquivo de
     configuração config/etl_rules.yaml. Isso permite alterar regras de negócio sem alterar o código fonte.

  6. Recomendações Específicas (Ações Imediatas)

  Para elevar o nível do precogas baseando-se nesta análise, recomendo as seguintes ações imediatas pelo agente:

   1. Refatoração de Logs: Criar um módulo utilitário de log (inspirado no log_utils do RPG) para padronizar a saída dos serviços downloader e extractor.
   2. Atualização do GEMINI.md do PrecoGas:
       * Adicionar a regra de "Atualização de Documentação e Dependências Pré-Commit".
       * Adicionar a diretriz de "Code-First" para as respostas do agente.
       * Especificar o uso de pathlib.
   3. Implementação de Health Check: Criar uma rota /health na API que verifica a conexão com o Redis e a internet (simulando um request leve), seguindo o princípio de verificação explícita de recursos.

## 🚀 Planejado
- [ ] **Segurança:** Monitorar e corrigir vulnerabilidades apontadas pelo Dependabot.
- [ ] **Funcionalidade:** Adicionar suporte a outros estados na API (parâmetro via URL, hoje fixo em DF).

## ✅ Concluído
- [x] **Logs:** Refatoração para padronizar as saídas dos serviços de download e extração usando um módulo de log dedicado.
- [x] **Testes:** Suíte completa (Unitários, Integração) com cobertura de **89%**.
- [x] **CI/CD:** Workflow do GitHub Actions configurado para testes automatizados (`pytest`) e linting (`ruff`).
- [x] **Qualidade:** Cobertura de código > 80% garantida via `pytest-cov`.
- [x] **Cache:** Implementação de sistema de cache (Redis).
- [x] **Deploy:** Configuração para deploy automatizado no Render.com.
- [x] **Correção:** Ajuste na extração de dados e URLs da ANP.
- [x] **Infra:** Configuração de Docker Compose.
