import time
import requests
import streamlit as st

st.set_page_config(page_title="Entropia Lab", page_icon="🧪", layout="wide")
st.title("Entropia Lab")
st.caption("MVP local · tutor de programação e bancada de testes de LLMs")

def base_url(url):
    return url.strip().rstrip("/")

def get_models(url):
    r = requests.get(f"{base_url(url)}/api/tags", timeout=8)
    r.raise_for_status()
    return sorted(m["name"] for m in r.json().get("models", []) if m.get("name"))

def ask_model(url, model, system_prompt, prompt, timeout):
    messages = []
    if system_prompt.strip():
        messages.append({"role": "system", "content": system_prompt.strip()})
    messages.append({"role": "user", "content": prompt.strip()})
    start = time.perf_counter()
    r = requests.post(
        f"{base_url(url)}/api/chat",
        json={"model": model, "messages": messages, "stream": False},
        timeout=timeout,
    )
    elapsed = time.perf_counter() - start
    r.raise_for_status()
    data = r.json()
    eval_count = data.get("eval_count")
    eval_duration = data.get("eval_duration")
    seconds = eval_duration / 1e9 if eval_duration else None
    return {
        "model": model,
        "text": data.get("message", {}).get("content", ""),
        "elapsed": elapsed,
        "total": data.get("total_duration", 0) / 1e9,
        "load": data.get("load_duration", 0) / 1e9,
        "prompt_eval": data.get("prompt_eval_duration", 0) / 1e9,
        "generation": seconds,
        "prompt_tokens": data.get("prompt_eval_count"),
        "tokens": eval_count,
        "tps": eval_count / seconds if eval_count and seconds and seconds > 0 else None,
    }

def show_metrics(r):
    cols = st.columns(4)
    cols[0].metric("Tempo total", f"{r['elapsed']:.2f} s")
    cols[1].metric("Tempo de geração", f"{r['generation']:.2f} s" if r["generation"] is not None else "N/D")
    cols[2].metric("Tokens gerados", str(r["tokens"]) if r["tokens"] is not None else "N/D")
    cols[3].metric("Tokens/s", f"{r['tps']:.2f}" if r["tps"] is not None else "N/D")
    with st.expander("Métricas detalhadas"):
        st.json({
            "Modelo": r["model"],
            "Tempo total reportado pelo Ollama (s)": round(r["total"], 3),
            "Carregamento (s)": round(r["load"], 3),
            "Avaliação do prompt (s)": round(r["prompt_eval"], 3),
            "Geração (s)": round(r["generation"], 3) if r["generation"] is not None else None,
            "Tokens de entrada": r["prompt_tokens"],
            "Tokens gerados": r["tokens"],
        })

with st.sidebar:
    st.header("Conexão")
    url = st.text_input("URL do Ollama", "http://127.0.0.1:11434")
    timeout = st.number_input("Tempo limite (segundos)", 30, 900, 300, 30)
    if st.button("Atualizar modelos"):
        st.session_state.pop("models", None)
        st.rerun()
    try:
        if "models" not in st.session_state:
            st.session_state.models = get_models(url)
        models = st.session_state.models
        st.success(f"Ollama conectado · {len(models)} modelo(s)")
    except requests.RequestException as e:
        models = []
        st.error("Não foi possível acessar o Ollama.")
        st.caption(str(e))

if not models:
    st.warning("Nenhum modelo encontrado. Confira o serviço e execute `ollama list` no terminal.")
    st.stop()

system_prompt = st.text_area(
    "Instruções do tutor",
    "Você é um tutor de programação para uma pessoa iniciante em ADS. Explique passo a passo, "
    "use português brasileiro, seja tecnicamente preciso e não invente APIs ou funções. "
    "Declare incertezas e explique o código em vez de apenas fornecê-lo.",
    height=100,
)
prompt = st.text_area(
    "Pergunta ou tarefa de teste",
    "Explique a diferença entre uma requisição HTTP POST e o JSON enviado no corpo. "
    "Dê um exemplo curto em Node.js usando o módulo nativo http.",
    height=120,
)

tab_one, tab_compare = st.tabs(["Testar um modelo", "Comparar modelos"])

with tab_one:
    model = st.selectbox("Modelo", models, key="one_model")
    if st.button("Enviar pergunta", type="primary"):
        if not prompt.strip():
            st.warning("Escreva uma pergunta.")
        else:
            try:
                with st.spinner(f"Consultando {model}..."):
                    st.session_state.one_result = ask_model(url, model, system_prompt, prompt, int(timeout))
            except requests.RequestException as e:
                st.error(f"Erro na consulta: {e}")
    result = st.session_state.get("one_result")
    if result:
        st.markdown(f"### Resposta · `{result['model']}`")
        st.markdown(result["text"])
        show_metrics(result)

with tab_compare:
    selected = st.multiselect(
        "Selecione pelo menos dois modelos",
        models,
        default=models[:2] if len(models) >= 2 else models,
        key="compare_models",
    )
    st.caption("Os modelos são testados sequencialmente. A primeira execução pode incluir o tempo de carregamento.")
    if st.button("Executar comparação", type="primary"):
        if not prompt.strip():
            st.warning("Escreva uma pergunta.")
        elif len(selected) < 2:
            st.warning("Selecione pelo menos dois modelos.")
        else:
            results = []
            progress = st.progress(0)
            status = st.empty()
            for i, name in enumerate(selected):
                status.write(f"Consultando {name} ({i+1}/{len(selected)})…")
                try:
                    results.append(ask_model(url, name, system_prompt, prompt, int(timeout)))
                except requests.RequestException as e:
                    results.append({"model": name, "text": f"Erro: {e}", "elapsed": None,
                                    "generation": None, "tokens": None, "tps": None})
                progress.progress((i + 1) / len(selected))
            status.empty()
            st.session_state.compare_results = results
    results = st.session_state.get("compare_results", [])
    if results:
        rows = []
        for r in results:
            rows.append({
                "Modelo": r["model"],
                "Tempo total (s)": round(r["elapsed"], 2) if r.get("elapsed") is not None else "Erro",
                "Geração (s)": round(r["generation"], 2) if r.get("generation") is not None else "N/D",
                "Tokens": r.get("tokens") or "N/D",
                "Tokens/s": round(r["tps"], 2) if r.get("tps") is not None else "N/D",
            })
        st.dataframe(rows, use_container_width=True, hide_index=True)
        for r in results:
            with st.expander(f"Resposta completa · {r['model']}"):
                st.markdown(r["text"])
                if r.get("elapsed") is not None:
                    show_metrics(r)

st.divider()
st.caption("Use a mesma pergunta e as mesmas instruções para comparar modelos. Métricas de velocidade não medem, sozinhas, a qualidade.")
