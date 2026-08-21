import streamlit as st
import os
from utils.database  import salvar_documentacao, listar_documentacao, deletar_documentacao, documento_existe

PASTA_DOCS = "docs"
def show():
    
    st.title("Documentação")
    st.write("insira a documentação de referencia para a análise da água aqui:")
    
    PASTA_DOCS = "docs"
    os.makedirs(PASTA_DOCS, exist_ok=True)
    
    arquivo = st.file_uploader("Upload de arquivo", type=["pdf","docx"], accept_multiple_files=False, key = "file_upload")

    if arquivo is not None:
        if st.button("Salvar documento", use_container_width=True):
            
            
            if documento_existe(arquivo.name):
                st.warning("Documento já foi cadastrado")
                
            else:    
                caminho = os.path.join(PASTA_DOCS, arquivo.name)
                with open(caminho, "wb") as f:
                    f.write(arquivo.getbuffer())
                    
                salvar_documentacao(
                    nome = arquivo.name,
                    caminho= caminho,
                    tipo= arquivo.type  
                )
                st.success("Documento salvo com sucesso")
                
    st.divider()
    st.subheader("Documentos cadastrados")
    
    documentos = listar_documentacao()
    
    if not documentos:
        st.warning("Nenhum documento cadastrado")
    
    else:
        for documento in documentos:
            
                with st.expander(f"{documento['nome']}"):
                    if os.path.exists(documento["caminho"]):
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            
                                with open(documento["caminho"], "rb") as f:
                                    st.download_button(
                                        label="Download",
                                        data= f.read(),
                                        file_name=documento["nome"],
                                        mime=documento["tipo"],
                                        key=f"download_{documento['id']}", use_container_width=True)
                        with col2:    
                            if st.button("Deletar",key=f"deletar_{documento['id']}", use_container_width=True):
                                deletar_documentacao(documento["id"])
                        
                        
                                if os.path.exists(documento["caminho"]):
                                        os.remove(documento["caminho"])
                                        
                                        st.success("Arquivo deletado com sucesso")
                                        st.rerun()
                                            
                    else:
                        st.error("Arquivo não encontrado.")     
                        
                        if st.button("Remover do banco de dados", key=f"remover_{documento['id']}"):
                            deletar_documentacao(documento["id"])
                            st.rerun()
       