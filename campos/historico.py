import streamlit as st
from utils.database import listar_analises, deletar_analise

def show():
    st.title("Histórico")
    analises = listar_analises()
    
    if not analises:
        st.warning("Nenhuma análise cadastrada.")
        
    else:
        for analise in analises:
            with st.expander(f"Análise: {analise['nome']} - {analise['data']}"):
                st.write(f"Temperatura: {analise['temperatura']} °C")
                st.write(f"pH: {analise['ph']}")
                st.write(f"Oxigênio Dissolvido: {analise['oxigenio_dissolvido']} mg/L")
                st.write(f"Nitrato: {analise['nitrato']} mg/L")
                st.write(f"Nitrito: {analise['nitrito']} mg/L")
                st.write(f"Amônia: {analise['amonia']} mg/L")
                st.write(f"Dureza: {analise['resultado_dureza']}")
                st.write(f"Turbidez: {analise['resultado_turbidez']}")
                st.write(f"STD: {analise['resultado_std']}")
                st.write(f"Salinidade: {analise['resultado_salinidade']}")
                st.subheader(f"Relatório:")
                st.markdown(f"{analise['relatorio']}")
    
                if st.button("Deletar análise", use_container_width=True, key=f"deletar_analise{analise['id']}"):
                    deletar_analise(analise['id'])
                    st.success("análise excluida com sucesso")
                    st.rerun()
            
        
    
    