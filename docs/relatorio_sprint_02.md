# Entropia Lab — Relatório do Sprint 2

**Data:** 17 de outubro de 2026  
**Projeto:** Entropia Lab MVP  
**Status:** MVP funcional em desenvolvimento

## 1. Objetivo do sprint

Desenvolver uma aplicação local para experimentar modelos de
linguagem executados pelo Ollama, comparar seu desempenho e
estabelecer a base de um agente tutor de programação.

## 2. Funcionalidades implementadas

### Integração com o Ollama
- Comunicação com a API local.
- Identificação dinâmica dos modelos instalados.
- Seleção de modelos pela interface.
- Configuração do endereço da API.

### Interface e interação
- Interface web desenvolvida com Streamlit.
- Envio de perguntas a um modelo selecionado.
- Campo editável para as instruções do tutor.
- Exibição das respostas completas.

### Comparação de modelos
- Seleção de dois ou mais modelos.
- Execução sequencial com a mesma pergunta.
- Exibição comparativa dos resultados.
- Indicadores de progresso durante a execução.

### Métricas
- Tempo total da requisição.
- Tempo de carregamento do modelo.
- Tempo de avaliação do prompt.
- Tempo de geração.
- Quantidade de tokens de entrada e saída.
- Velocidade de geração em tokens por segundo.

### Tratamento de erros
- Verificação da disponibilidade da API.
- Tratamento de falhas nas requisições HTTP.
- Configuração do tempo limite das consultas.

## 3. Tecnologias utilizadas

- Python
- Streamlit
- Requests
- Ollama
- Ubuntu Linux
- Git

## 4. Modelos disponíveis no ambiente

- deepseek-coder:1.3b
- qwen2.5-coder:1.5b
- qwen2.5-coder:3b
- qwen3.5:4b
- qwen2.5-coder:7B

## 5. Observações dos testes

O modelo deepseek-coder:1.3b foi utilizado em um teste funcional
da interface.

O modelo qwen3.5:4b apresentou erro de tempo excedido em um teste.
A causa ainda precisa ser investigada.

A qualidade das respostas dos modelos deve ser avaliada
separadamente das métricas de velocidade.

## 6. Limitações atuais

- Não há histórico permanente de conversas.
- O código gerado não é executado automaticamente.
- Não existe verificação automática da correção das respostas.
- Não há integração com modelos em nuvem.
- As instruções personalizadas não são persistidas entre sessões.

## 7. Próximas atividades

1. Investigar os erros de tempo excedido.
2. Implementar histórico de conversas e manutenção de contexto.
3. Aprimorar as instruções pedagógicas do tutor.
4. Criar testes para a comunicação com o Ollama.
5. Avaliar mecanismos de persistência local.

## 8. Resultado do sprint

O projeto possui uma interface funcional para consultar modelos
locais e comparar suas métricas de execução.

A próxima etapa será evoluir o MVP para um tutor de programação
capaz de manter o contexto das conversas e apoiar o aprendizado
de forma progressiva.
