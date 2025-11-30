import streamlit as st
from analysis import basic_metrics, highlight_issues
from model import call_llm_analysis
import time
from dotenv import load_dotenv
from model import OPENAI_KEY
load_dotenv()

st.set_page_config(page_title="Tutor IA - Linguistic Analyzer", layout="wide")

st.title("Tutor Inteligente: Análise Linguística com IA")
st.markdown("Cole um texto (aluno) abaixo e gere análise linguística, sugestões e reescrita usando LLM.")

with st.sidebar:
    st.write("Instruções rápidas")
    st.write("- Cole um parágrafo ou redação curta (50–800 palavras).")
    st.write("- Se não tiver OPENAI_API_KEY, o app usa fallback heurístico.")

text = st.text_area("Texto do aluno (input)", height=240)

col1, col2 = st.columns([1,1])
with col1:
    if st.button("Analisar (LLM)"):
        if not text.strip():
            st.error("Cole um texto primeiro.")
        else:
            with st.spinner("Executando métricas e chamando LLM..."):
                metrics = basic_metrics(text)
                heur = highlight_issues(text)
                st.subheader("Métricas Básicas")
                st.write(metrics)
                if heur:
                    st.info("Heuristics / quick hints:")
                    for h in heur:
                        st.write("- " + h)
                # LLM analysis
                llm_result = call_llm_analysis(text)
                time.sleep(0.2)
                st.subheader("Resultado do LLM")
                if "error" in llm_result:
                    st.error("LLM error: " + str(llm_result.get("error")))
                    st.write(llm_result.get("raw", llm_result.get("detail", "")))
                else:
                    st.markdown("**Assessment**")
                    st.write(llm_result.get("assessment", ""))
                    st.markdown("**Detected grammar issues**")
                    for g in llm_result.get("grammar_issues", []):
                        st.write("- " + (g.get("issue") + ": " + g.get("explain") if isinstance(g, dict) else str(g)))
                    st.markdown("**Estimated level**")
                    st.write(llm_result.get("level", ""))
                    st.markdown("**Suggestions (didactic)**")
                    for s in llm_result.get("suggestions", []):
                        st.write("- " + s)
                    st.markdown("**Rewritten (improved) text**")
                    st.write(llm_result.get("rewrite", ""))

with col2:
    st.write("Prompt used for LLM (editable):")
    st.code(call_llm_analysis.__doc__ if call_llm_analysis.__doc__ else "See model.SYSTEM_PROMPT in model.py")

print("API KEY:", OPENAI_KEY[:8], "...carregada!")
