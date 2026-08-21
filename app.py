import streamlit as st
from streamlit_option_menu import option_menu
from campos import inicio, nova_analise, analise_estatistica, documentacao, historico, sobre

st.set_page_config(
    page_title= "Sistema de Análise de Água",
    page_icon= "💧",
    layout= "wide"
    )

def show():

    with st.sidebar:
        pagina = option_menu(
            "Menu",
            ["Início",
             "Nova Análise",
             "Análise Estatística",
             "Documentação",
             "Histórico",
             "Sobre"],
            default_index = 0
        )
        
    match pagina:
        case "Início":
            inicio.show()

        case "Nova Análise":
            nova_analise.show()

        case "Análise Estatística":
            analise_estatistica.show()

        case "Documentação":
            documentacao.show()

        case "Histórico":
            historico.show()

        case "Sobre":
            sobre.show()

show()