import streamlit as st
from datetime import datetime
from utils.calculos import dureza, std, salinidade, turbidez
from utils.database import salvar_analise, nome_existe
from dotenv import load_dotenv
import os
from groq import Groq

load_dotenv()  
#relacionando chave API Groq
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def show():
    
    st.title ("💧Sistema de Análise de Qualidade da Água")
    st.write("Preencha as informaçõe abaixo:")
    
#campos de preenchimento de dados

    st.header("Nome da Análise:")
    nome_analise = st.text_input(
        "Digite um nome para a análise",
        key = "nome_analise")
    
    st.divider()
   
    temperatura = st.number_input(
        "Temperatura (°C)",
        min_value=1.0,
        max_value=100.0,
        value=25.0,
        key = "temperatura"
        )
    ph = st.number_input(
        "pH",
        min_value=0.0,
        max_value=14.0,
        value=7.0,
        key = "pH"
        )
    oxigenio_dissolvido = st.selectbox(
        "Oxigênio Dissolvido mg/L",
        [5, 6, 7, 8, 9],
        key = "oxigenio"
        )
    st.header("Indice de Nitrogênio")
    nitrato = st.selectbox(
        "Nitrato mg/L",
        [0.5, 1.0, 0.05, 2.0, 2.5],
        key = "nitrato"
        )
    nitrito = st.selectbox(
        "Nitríto mg/L",
        [0.5, 1.0, 0.05, 2.0, 2.5],
         key = "nitrito"
        )
    amonia = st.selectbox(
        "Amônia mg/L",
        [0.5, 1.0, 0.05, 2.0, 2.5],
        key = "amonia"
        )

    st.header("Dureza")
    c_edta = st.number_input(
        "Concentração de EDTA (mL)",
        min_value = 0.0,
        max_value = 1.0,
        value = 0.0,
        key = "c_edta"
        )
    v_edta = st.number_input(
        "Volume de EDTA (mL)",
        min_value = 0.0,
        max_value = 10.0,
        value = 0.0,
        key = "v_edta"
        )
    v_amostra = st.number_input(
        "Volume da amostra (mL)",
        min_value = 0.0,
        max_value = 100.0,
        value = 0.0,
        key = "volume_dureza"
        )
    
    st.header("Turbidez")
    turbidez = st.number_input(
        "Turbidez (NTU)",
        min_value = 0.0,
        max_value = 100.0,
        value = 0.0,
        key = "turbidez"
        )

    st.header("Sólidos Totais Dissolvidos")
    massa_in = st.number_input(
        "Massa Inicial (g)",
        min_value = 0.0,
        max_value = 500.0,
        value = 0.0,
        key = "massa_inicial"
        )
    massa_fi = st.number_input(
        "Massa Final (g)",
        min_value = 0.0,
        max_value = 10000.0,
        value = 0.0,
        key = "massa_final"
        )
    volume = st.number_input(
        "Volume da amostra (mL)",
        min_value = 0.0,
        max_value = 100.0,
        value = 0.0,
        key = "volume_STD"
        )
    
    st.header("Salinidade")
    condutividade = st.number_input(
        "Condutividade Elétrica (µS/cm)",
        min_value = 0.0,
        max_value = 100000.0,
        value = 0.0,
        key = "condutividade"
        )
#botão de análise

    if "analise" not in st.session_state:
         st.session_state["analise"] = None
         
    if st.button ("Analisar", use_container_width=True):
        st.write("Analisando os dados...")
        
#relacionado os resultado de dureza, std, salinidade
        resultado_dureza = dureza(c_edta, v_edta, v_amostra)
        resultado_std = std(massa_in, massa_fi, volume)
        resultado_salinidade = salinidade(condutividade)
        tem_erro = False
        
#telas de erro
        if not nome_analise.strip():
            st.error("Análise não esta nomeada.")
            tem_erro = True
            
        elif nome_existe(nome_analise):
            st.error("já há uma análise com esse nome")
            tem_erro = True
            
        if resultado_dureza is None:
            st.error("O volume da amostra para dureza não pode ser zero.")
            tem_erro = True  
            
        if resultado_std is None:
            st.error("O volume da amostra para sólidos sottais dissolvidos não pode ser zero.")   
            tem_erro = True

#tela de resultados
        if not tem_erro:
            
            st.success("Análise concluída!")
            resultado_geral = st.info(f"""
                ### Resultados da Análise:
                
                Temperatura: {temperatura} °C\n
                pH: {ph}\n
                Oxigênio Dissolvido: {oxigenio_dissolvido} mg/L\n
                Nitrato: {nitrato} mg/L\n
                Nitríto: {nitrito} mg/L\n
                Amônia: {amonia} mg/L\n
                Dureza: {resultado_dureza:.2f} mg/L\n
                Sólidos Totais Dissolvidos: {resultado_std:.2f} mg/L\n
                Salinidade: {resultado_salinidade:.2f} g/L\n
                Turbidez: {turbidez} NTU

            """)
            
            #relatório técnico IA

            prompt = f"""Você é um engenheiro ambiental e químico especializado em análise de qualidade da água.

                Sua função é interpretar resultados laboratoriais de forma técnica, objetiva e clara.

                Utilize como referência, sempre que aplicável:
                - Resolução CONAMA 357/2005;
                - Portaria GM/MS nº 888/2021.

                Dados da amostra:


                Analise os seguintes parâmetros:
                Temperatura: {temperatura} °C\n
                pH: {ph}\n
                Oxigênio Dissolvido: {oxigenio_dissolvido} mg/L\n
                Nitrato: {nitrato} mg/L\n
                Nitríto: {nitrito} mg/L\n
                Amônia: {amonia} mg/L\n
                Dureza: {resultado_dureza:.2f} mg/L\n
                Turbidez: {turbidez:.2f} NTU\n
                Sólidos Totais Dissolvidos: {resultado_std:.2f} mg/L\n
                Salinidade: {resultado_salinidade:.2f} g/L
                

                Produza um relatório contendo exatamente as seguintes seções:

                ## Diagnóstico Geral
                Faça um resumo da qualidade da água.

                ## Avaliação dos Parâmetros
                Explique o significado de cada parâmetro informado.

                ## Possíveis Problemas
                Indique quais parâmetros sugerem alterações na qualidade da água.

                ## Possíveis Causas
                Descreva possíveis fontes naturais ou antrópicas que expliquem os resultados.

                ## Recomendações
                Sugira medidas para melhorar ou monitorar a qualidade da água.

                ## Conclusão
                Apresente uma conclusão objetiva em no máximo 5 linhas.

                """

            responses = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {
                    "role": "user",
                    "content": prompt
                }
                    ]
            )

            st.info(responses.choices[0].message.content)
            
            relatorio = responses.choices[0].message.content
            
            #armazenamento de dados
            
            st.session_state["analise"] = {
                "nome": nome_analise,
                "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "temperatura": temperatura,
                "ph": ph,
                "oxigenio_dissolvido": oxigenio_dissolvido,
                "nitrato": nitrato,
                "nitrito": nitrito,
                "amonia": amonia,
                "dureza": resultado_dureza,
                "turbidez": turbidez,
                "std": resultado_std,
                "salinidade": resultado_salinidade,
                "relatorio": relatorio
            }
        
    if st.session_state["analise"] is not None:          
        if st.button("Guardar dados", use_container_width=True):
            dados = st.session_state["analise"]
            
            try:
                salvar_analise(
                    dados["nome"],
                    dados["data"],
                    dados["temperatura"],
                    dados["ph"],
                    dados["oxigenio_dissolvido"],
                    dados["nitrato"],
                    dados["nitrito"],
                    dados["amonia"],
                    dados["dureza"],
                    dados["turbidez"],
                    dados["std"],
                    dados["salinidade"],
                    dados["relatorio"]
                )
                
                #salva dados
                st.success("Dados salvos com sucesso!")
                
                #limpa das temporarios ápos salvos no banco de dados
                st.session_state["analise"] = None
                
                #recarrega página
                st.rerun()
                
            except Exception as e:
                st.error(f"Erro ao salvar dados: {e}")