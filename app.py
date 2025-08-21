import streamlit as st
import requests

st.title("Consultor da Tabela FIPE 🚗")

# --- PASSO 1: MARCAS ---
# Faz a primeira chamada à API para buscar a lista de marcas de veículos.
URL_MARCAS = "https://parallelum.com.br/fipe/api/v1/carros/marcas"
response_marcas = requests.get(URL_MARCAS)

if response_marcas.status_code == 200:
    dados_marcas = response_marcas.json()
    # Extrai apenas os nomes das marcas para exibir no seletor.
    nomes_das_marcas = [marca['nome'] for marca in dados_marcas]
    marca_selecionada_nome = st.selectbox("Selecione a Marca:", nomes_das_marcas)

    # Procura o código correspondente à marca que o usuário selecionou.
    codigo_da_marca = None
    for marca in dados_marcas:
        if marca['nome'] == marca_selecionada_nome:
            codigo_da_marca = marca['codigo']
            break

    # --- PASSO 2: MODELOS ---
    # Se um código de marca foi encontrado, busca os modelos.
    if codigo_da_marca:
        URL_MODELOS = f"https://parallelum.com.br/fipe/api/v1/carros/marcas/{codigo_da_marca}/modelos"
        response_modelos = requests.get(URL_MODELOS)

        if response_modelos.status_code == 200:
            dados_completos_modelos = response_modelos.json()
            lista_de_modelos = dados_completos_modelos['modelos']
            lista_de_anos = dados_completos_modelos['anos']

            nomes_dos_modelos = [modelo['nome'] for modelo in lista_de_modelos]
            modelo_selecionado_nome = st.selectbox("Selecione o Modelo:", nomes_dos_modelos)

            # Procura o código do modelo selecionado.
            codigo_do_modelo = None
            for modelo in lista_de_modelos:
                if modelo['nome'] == modelo_selecionado_nome:
                    codigo_do_modelo = modelo['codigo']
                    break

            # --- PASSO 3: ANOS ---
            # Se um código de modelo foi encontrado, mostra os anos.
            if codigo_do_modelo:
                nomes_dos_anos = [ano['nome'] for ano in lista_de_anos]
                ano_selecionado_nome = st.selectbox("Selecione o Ano:", nomes_dos_anos)

                # Adiciona o botão para o usuário confirmar a consulta.
                if st.button("Consultar Preço"):

                    # Procura o código do ano selecionado.
                    codigo_do_ano = None
                    for ano in lista_de_anos:
                        if ano['nome'] == ano_selecionado_nome:
                            codigo_do_ano = ano['codigo']
                            break

                    # --- PASSO 4: RESULTADO FINAL! ---
                    # Com todos os códigos, faz a consulta final.
                    if codigo_do_ano:
                        URL_FINAL = f"https://parallelum.com.br/fipe/api/v1/carros/marcas/{codigo_da_marca}/modelos/{codigo_do_modelo}/anos/{codigo_do_ano}"
                        response_final = requests.get(URL_FINAL)

                        if response_final.status_code == 200:
                            dados_finais = response_final.json()

                            # Exibe o resultado de forma destacada.
                            st.header(f"O valor do veículo é: **{dados_finais['Valor']}**")
                            st.markdown(f"Dados referentes ao mês de **{dados_finais['MesReferencia']}**.")
                        else:
                            st.error("Não foi possível buscar o valor do veículo.")

else:
    st.error("Falha ao buscar a lista de marcas. Tente recarregar a página.")