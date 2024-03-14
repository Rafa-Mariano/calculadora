import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def calcular_parcelas(valor_total, numero_parcelas, taxa_juros_anual, datas_vencimento):
    taxa_juros_mensal = taxa_juros_anual / 12 / 100
    valor_parcela = valor_total * (taxa_juros_mensal / (1 - (1 + taxa_juros_mensal)**(-numero_parcelas)))
    juros_total = valor_parcela * numero_parcelas - valor_total

    parcelas = []
    for i in range(numero_parcelas):
        parcelas.append({'Parcela': i+1, 'Data Vencimento': datas_vencimento[i], 'Valor Parcela': valor_parcela, 'Juros': valor_parcela * (i+1) - valor_total, 'Saldo Devedor': valor_total - valor_parcela * (i+1)})
    
    return valor_parcela, juros_total, pd.DataFrame(parcelas)

st.title('Calculadora Confiança Financeira')

valor_total = st.number_input('Valor total:', min_value=0.01, step=0.01)
periodo_pagamento = st.selectbox('Periodicidade de pagamento:', ('Mensal', 'Quinzenal', 'Semanal'))
numero_parcelas = st.number_input('Número de parcelas:', min_value=1, step=1, format='%d')
taxa_juros_anual = st.number_input('Taxa de juros anual (%):', min_value=1, step=1)

if periodo_pagamento == 'Mensal':
    delta = timedelta(days=30)
elif periodo_pagamento == 'Quinzenal':
    delta = timedelta(days=15)
else:  # Semanal
    delta = timedelta(weeks=1)

datas_vencimento = []
data_vencimento = datetime.now()
for i in range(numero_parcelas):
    data_vencimento = st.date_input(f'Data de vencimento da parcela {i+1}:', min_value=datetime.now())
    datas_vencimento.append(data_vencimento.strftime('%Y-%m-%d'))
    data_vencimento += delta

opcao_calculo = st.radio("Opção de cálculo:", ('Número de parcelas', 'Valor da parcela'))

if opcao_calculo == 'Número de parcelas':
    valor_parcela, juros_total, df = calcular_parcelas(valor_total, numero_parcelas, taxa_juros_anual, datas_vencimento)
    st.write(f'Valor de cada parcela: R$ {valor_parcela:.2f}')
    st.write(f'Total de juros pagos: R$ {juros_total:.2f}')
    st.write(df)
else:
    valor_parcela = st.number_input('Valor da parcela:', min_value=1, step=1)
    numero_parcelas = int(valor_total / valor_parcela)
    valor_parcela, juros_total, df = calcular_parcelas(valor_total, numero_parcelas, taxa_juros_anual, datas_vencimento)
    st.write(f'Número de parcelas necessárias: {numero_parcelas}')
    st.write(f'Total de juros pagos: R$ {juros_total:.2f}')
    st.write(df)

if st.button('Baixar Excel'):
    df.to_excel('resultados_financiamento.xlsx', index=False)
    st.success('Arquivo Excel gerado com sucesso!')

