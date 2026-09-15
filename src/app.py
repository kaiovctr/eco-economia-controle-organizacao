#carregar bibliotecas
import pandas as pd
import json
import requests
import streamlit as st
import re

#config ollama
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODELO = "gpt-oss"

#abrindo os dados
perfil = json.load(open('./data/perfil_usuario.json'))
transacoes = pd.read_csv('./data/transacoes.csv')
historico = pd.read_csv('./data/historico_interacoes.csv')

#contexto
contexto = f"""
CLIENTE: {perfil['nome']}, {perfil['idade']} anos
OBJETIVO: {perfil['objetivo_principal']}

RENDA:
Salário bruto: R$ {perfil['renda']['salario_bruto']:.2f}
Renda extra mínima: R$ {perfil['renda']['renda_extra_minima']:.2f}
Renda extra máxima: R$ {perfil['renda']['renda_extra_maxima']:.2f}
Descrição da renda extra: {perfil['renda']['descricao_renda_extra']}

MORADIA:
Tipo: {perfil['moradia']['tipo']}
Valor mensal: R$ {perfil['moradia']['valor_mensal']:.2f}

OBJETIVO PRINCIPAL:
{perfil['objetivo_principal']}

METAS:
{perfil['metas']}

PREFERÊNCIAS FINANCEIRAS:
Valor desejado para economizar por mês: R$ {perfil['preferencias_financeiras']['valor_desejado_para_economizar_por_mes']:.2f}
Prioridade: {perfil['preferencias_financeiras']['prioridade']}

TRANSAÇÕES RECENTES:
{transacoes.to_string(index=False)}

ATENDIMENTOS ANTERIORES:
{historico.to_string(index=False)}
"""

# ler system prompt do 03-prompts
def carregar_system_prompt(caminho_md='./docs/03-prompts.md'):
    with open(caminho_md, 'r', encoding='utf-8') as f:
        conteudo = f.read()

    match = re.search(
        r'## System Prompt\s*```(?:\w*\n)?(.*?)```',
        conteudo,
        re.DOTALL
    )

    if not match:
        raise ValueError("Não foi possível encontrar o System Prompt no arquivo markdown.")

    return match.group(1).strip()

SYSTEM_PROMPT = carregar_system_prompt()

#chamar ollama
def perguntar(msg):
    prompt = f"""
    {SYSTEM_PROMPT}

    CONTEXTO DO CLIENTE:
    {contexto}

    Perguntas: {msg}"""

    r = requests.post(OLLAMA_URL, json={"model": MODELO, "prompt": prompt, "stream": False})
    return r.json()['response']

#interface com streamlit
st.title("💵 ECO - Economia, Controle e Organização")
st.subheader("Seu organizador financeiro!")

if pergunta := st.chat_input("Qual sua dúvida sobre suas finanças?"):
    st.chat_message("user").write(pergunta)
    with st.spinner("..."):
        st.chat_message("assistant").write(perguntar(pergunta))