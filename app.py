import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt

# Carregue o modelo de previsão
model = joblib.load('modelo/melhor_modelo.joblib')

# Carregue o histórico de preços
historico = pd.read_csv('https://raw.githubusercontent.com/LeticiaMoliveira/FIAP/main/Fase%204/petroleo.csv',
                        parse_dates=['Date'], dayfirst=True,
                        thousands='.', decimal=',')

# Crie um formulário para solicitar quantos dias o cliente quer prever
st.title('Previsão do Preço do Petróleo Brent')
st.write('Este aplicativo usa um modelo de aprendizado de máquina para prever o preço do petróleo Brent com base no histórico de preços anteriores.')
st.write('Insira o número de dias que você deseja prever:')
num_days = st.number_input('Número de dias', min_value=1, max_value=400)

if st.button('Prever'):
    # Selecione os últimos n registros do histórico
    dados_previsao = historico.tail(num_days)

    # Preveja o preço do petróleo Brent
    previsao = model.predict(dados_previsao[['Price']])  # Use apenas a coluna 'Price' como entrada

    # Crie um DataFrame com as previsões
    data_inicial = dados_previsao['Date'].iloc[-1] + pd.DateOffset(days=1)  # Adicione um dia para obter a próxima data
    datas = pd.date_range(start=data_inicial, periods=num_days, freq='D')
    df_previsao = pd.DataFrame({'Data': datas, 'Preço': previsao/10})

    # Crie um gráfico com as previsões
    plt.figure(figsize=(10, 6))
    plt.plot(historico['Date'], historico['Price'], label='Preço Histórico')
    plt.plot(df_previsao['Data'], df_previsao['Preço'], label='Previsão')
    plt.xlabel('Data')
    plt.ylabel('Preço')
    plt.title('Previsão do Preço do Petróleo Brent')
    plt.legend()
    st.pyplot(plt)

    # Exiba a tabela com as previsões
    st.write(f'Previsão do preço do petróleo Brent para os próximos {num_days} dias:')
    st.table(df_previsao)