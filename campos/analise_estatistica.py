import streamlit as st
from utils.database import listar_analises
from utils.calculos import media, desvio_padrao, variancia, amplitude, dpr

def show():
    st.title("Análise Estatística")
    
    analises = listar_analises()
    
    if not analises:
        st.warning("Nenhuma análise cadastrada.")
        
    if len(analises) < 3:
        st.warning("Deve conter pelo menos 3 analises")
        
    else:
            
            numero_analises = st.number_input("Selecione a quadidade analises que serão análisadas",
                max_value= len(analises),
                min_value= 2,
                value= 3,
                step = 1,
                key = "quantidade_analises"
            )
            
            opcoes = {analise['id']: analise['nome'] 
                      for analise in analises}
            
            selecionadas = st.multiselect(
                "selecione as análises",
                options = list(opcoes.keys()),
                format_func=lambda x:opcoes[x],
                max_selections= numero_analises 
            )
            
            if st.button("Analisar", use_container_width=True):
                analises_escolhidas = [
                    analise
                    for analise in analises
                    if analise['id'] in selecionadas
                ]
                
                if len(selecionadas) != numero_analises:
                    st.warning(f"Selecione extamente {numero_analises} análises")
                    return
                    
                medias = {}
                variancias = {}
                desvio_padroes = {}
                dprs = {}
                amplitudes = {}
                
                parametros = [
                    "ph",
                    "oxigenio_dissolvido",
                    "nitrato",
                    "nitrito",
                    "amonia",
                    "resultado_dureza",
                    "resultado_turbidez",
                    "resultado_std",
                    "resultado_salinidade",
                    ]
                for parametro in parametros:
                    
                    lista = [
                        analise[parametro]
                        for analise in analises_escolhidas
                        if analise[parametro] is not None]
                    
                    medias[parametro] = media(lista)
                    variancias[parametro] = variancia(lista)
                    desvio_padroes[parametro] = desvio_padrao(lista)
                    dprs[parametro] = dpr(lista)
                    amplitudes[parametro] = amplitude(lista)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"""## Médias:
    pH: {medias["ph"]:.2f}
    Oxigênio Dissolvido: {medias["oxigenio_dissolvido"]:.2f}
    Nitráto: {medias["nitrato"]:.2f}
    Nitríto: {medias["nitrito"]:.2f}
    Amônia: {medias["amonia"]:.2f}
    Dureza: {medias["resultado_dureza"]:.2f}
    Turbidez: {medias["resultado_turbidez"]:.2f}
    Sólidos Totais Dissolvidos: {medias["resultado_std"]:.2f}
    Salinidade:{medias["resultado_salinidade"]:.2f}""")
                    
                    st.info(f"""## Desvio Padrões:
    pH: {desvio_padroes["ph"]:.2f}
    Oxigênio Dissolvido: {desvio_padroes["oxigenio_dissolvido"]:.2f}
    Nitráto: {desvio_padroes["nitrato"]:.2f}
    Nitríto: {desvio_padroes["nitrito"]:.2f}
    Amônia: {desvio_padroes["amonia"]:.2f}
    Dureza: {desvio_padroes["resultado_dureza"]:.2f}
    Turbidez: {desvio_padroes["resultado_turbidez"]:.2f}
    Sólidos Totais Dissolvidos: {desvio_padroes["resultado_std"]:.2f}
    Salinidade:{desvio_padroes["resultado_salinidade"]:.2f}""")
                        
                    st.info(f"""## Amplitudes:
    pH: {amplitudes["ph"]:.2f}
    Oxigênio Dissolvido: {amplitudes["oxigenio_dissolvido"]:.2f}
    Nitráto: {amplitudes["nitrato"]:.2f}
    Nitríto: {amplitudes["nitrito"]:.2f}
    Amônia: {amplitudes["amonia"]:.2f}
    Dureza: {amplitudes["resultado_dureza"]:.2f}
    Turbidez: {amplitudes["resultado_turbidez"]:.2f}
    Sólidos Totais Dissolvidos: {amplitudes["resultado_std"]:.2f}
    Salinidade:{amplitudes["resultado_salinidade"]:.2f}""")
                    
                    #coluna 2
                with col2:
                    
                    st.info(f"""## Variâncias:
    pH: {variancias["ph"]:.2f}
    Oxigênio Dissolvido: {variancias["oxigenio_dissolvido"]:.2f}
    Nitráto: {variancias["nitrato"]:.2f}
    Nitríto: {variancias["nitrito"]:.2f}
    Amônia: {variancias["amonia"]:.2f}
    Dureza: {variancias["resultado_dureza"]:.2f}
    Turbidez: {variancias["resultado_turbidez"]:.2f}
    Sólidos Totais Dissolvidos: {variancias["resultado_std"]:.2f}
    Salinidade:{variancias["resultado_salinidade"]:.2f}""")
                    
                    st.info(f"""## Coeficientes de Variação:
    pH: {dprs["ph"]:.2f}
    Oxigênio Dissolvido: {dprs["oxigenio_dissolvido"]:.2f}
    Nitráto: {dprs["nitrato"]:.2f}
    Nitríto: {dprs["nitrito"]:.2f}
    Amônia: {dprs["amonia"]:.2f}
    resultado_dureza: {dprs["resultado_dureza"]:.2f}
    Turbidez: {dprs["resultado_turbidez"]:.2f}
    Sólidos Totais Dissolvidos: {dprs["resultado_std"]:.2f}
    Salinidade:{dprs["resultado_salinidade"]:.2f}""")
                    
                    
                    
                    
                    
                    
                    