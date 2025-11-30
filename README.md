# Tutor Inteligente de Leitura e Escrita (Protótipo)

Objetivo: protótipo rápido que analisa texto escrito e produz:
- avaliação geral
- detecção de problemas gramaticais
- estimativa de nível
- sugestões didáticas
- reescrita melhorada

Stack: Python, Streamlit, OpenAI (ou outro LLM).

## Como rodar (local)
1. Crie uma virtualenv (opcional) e instale:
   pip install -r requirements.txt

2. Se tiver API Key (OpenAI), exporte:
   export OPENAI_API_KEY="sua_chave_aqui"   (Linux/Mac)
   setx OPENAI_API_KEY "sua_chave_aqui"    (Windows - reinicie terminal)

3. Rode:
   streamlit run app.py

4. Cole um texto, clique em "Analisar (LLM)". Se não houver chave, o app usa fallback heurístico.

## O que entregar ao professor
- link para gravação curta (30s) mostrando o antes/depois.
- PDF com: texto original, métricas, análise, sugestões e reescrita.
- Link para o repositório GitHub com código + README.

## Prompt (usar em produção)
(veja model.py → SYSTEM_PROMPT)

