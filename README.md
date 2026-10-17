# Entropia Lab — MVP

Aplicação local em Python e Streamlit para conversar com modelos do Ollama, alternar entre eles e comparar desempenho.

## Requisitos
- Ubuntu/Linux
- Python 3.10+
- Ollama em execução e pelo menos um modelo instalado

## Instalação
No terminal, dentro do diretório do projeto:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Se `venv` não estiver disponível: `sudo apt install python3-venv`.

Confira os modelos: `ollama list`. Se necessário: `ollama pull qwen2.5-coder:1.5b`.

## Executar
```bash
source .venv/bin/activate
streamlit run app.py
```

A aplicação usa a API local `http://127.0.0.1:11434`.

## O que inclui
- Lista dinâmica de modelos via `/api/tags`
- Seletor para testar um modelo
- Prompt de sistema editável
- Comparação sequencial de modelos com a mesma pergunta
- Métricas de tempo total, carregamento, geração, tokens e tokens por segundo

## Limitações deliberadas
- Não guarda histórico permanente.
- Não executa código gerado.
- Não integra ainda APIs de modelos na nuvem.
- A primeira execução pode incluir carregamento do modelo.
- Velocidade não é uma medida da qualidade técnica.

## Privacidade
Por padrão, os prompts são enviados ao Ollama local em `127.0.0.1`. Não exponha a API do Ollama à rede sem avaliar a segurança.
