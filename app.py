import streamlit as st
import requests

# --- CONFIGURAÇÃO DA PÁGINA E ESTILOS ---
st.set_page_config(page_title="Consultor FIPE", page_icon="🚗")

st.title("Consultor da Tabela FIPE 🚗")

# Esconde o spinner "Running..." do cache e o ícone de "Running..." do canto superior
st.markdown("""
<style>
    [data-testid="stStatusWidget"] {
        visibility: hidden;
        height: 0 !important;
        position: absolute;
    }
</style>
""", unsafe_allow_html=True)


# --- ÁREA DE FUNÇÕES COM CACHE ---

@st.cache_data(show_spinner=False)
def buscar_marcas():
    """Busca a lista de todas as marcas de carros na API e guarda em cache."""
    URL = "https://parallelum.com.br/fipe/api/v1/carros/marcas"
    try:
        response = requests.get(URL, timeout=10)
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException:
        return None
    return None


@st.cache_data(show_spinner=False)
def buscar_modelos(codigo_da_marca):
    """Busca os modelos e anos de uma marca específica e guarda em cache."""
    URL = f"https://parallelum.com.br/fipe/api/v1/carros/marcas/{codigo_da_marca}/modelos"
    try:
        response = requests.get(URL, timeout=10)
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException:
        return None
    return None


@st.cache_data(show_spinner=False)
def buscar_valor(codigo_da_marca, codigo_do_modelo, codigo_do_ano):
    """Busca o valor final do veículo e guarda em cache."""
    URL = f"https://parallelum.com.br/fipe/api/v1/carros/marcas/{codigo_da_marca}/modelos/{codigo_do_modelo}/anos/{codigo_do_ano}"
    try:
        response = requests.get(URL, timeout=10)
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException:
        return None
    return None


# --- LÓGICA PRINCIPAL DO APP ---

dados_marcas = buscar_marcas()

if dados_marcas:
    nomes_das_marcas = [marca['nome'] for marca in dados_marcas]
    marca_selecionada_nome = st.selectbox("Selecione a Marca:", nomes_das_marcas)

    codigo_da_marca = None
    for marca in dados_marcas:
        if marca['nome'] == marca_selecionada_nome:
            codigo_da_marca = marca['codigo']
            break

    if codigo_da_marca:
        with st.spinner("Buscando modelos..."):
            dados_completos_modelos = buscar_modelos(codigo_da_marca)

        if dados_completos_modelos:
            lista_de_modelos = dados_completos_modelos.get('modelos', [])
            lista_de_anos = dados_completos_modelos.get('anos', [])

            nomes_dos_modelos = [modelo['nome'] for modelo in lista_de_modelos]
            modelo_selecionado_nome = st.selectbox("Selecione o Modelo:", nomes_dos_modelos)

            codigo_do_modelo = None
            for modelo in lista_de_modelos:
                if modelo['nome'] == modelo_selecionado_nome:
                    codigo_do_modelo = modelo['codigo']
                    break

            if codigo_do_modelo:
                nomes_dos_anos = [ano['nome'] for ano in lista_de_anos]
                ano_selecionado_nome = st.selectbox("Selecione o Ano:", nomes_dos_anos)

                if st.button("Consultar Preço"):
                    codigo_do_ano = None
                    for ano in lista_de_anos:
                        if ano['nome'] == ano_selecionado_nome:
                            codigo_do_ano = ano['codigo']
                            break

                    if codigo_do_ano:
                        with st.spinner("Consultando valor..."):
                            dados_finais = buscar_valor(codigo_da_marca, codigo_do_modelo, codigo_do_ano)

                        if dados_finais:
                            st.header(f"O valor do veículo é: **{dados_finais['Valor']}**")
                            st.markdown(f"Dados referentes ao mês de **{dados_finais['MesReferencia']}**.")
                        else:
                            st.error("Não foi possível buscar o valor do veículo.")
        else:
            st.warning("Não foi possível carregar os modelos para esta marca.")
else:
    st.error("Falha ao buscar a lista de marcas. A API pode estar fora do ar. Tente recarregar a página.")

