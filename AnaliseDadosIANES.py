#2° Trabalho apps
#Você foi contratado por uma empresa de manufatura para desenvolver um aplicativo interno
# que registre e analise os dados de produção das máquinas da linha de montagem
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title('Análise e Atualização de dados')
st.subheader('Empresa IANES ')


Aba1,Aba2 = st.tabs(['Registro','Gráfico'])
#Identificação funcionario 
with Aba1:
    dados = st.file_uploader('Carregar ultimos dados lançados', type = ['csv'])
    if dados is not None:
        df = pd.read_csv(dados)
        #Para corrigir nomes e remover as colunas que estão ficando duplicadas 
        df.columns = df.columns.str.strip().str.replace(':', ' ', regex = False)
        #Para remover as colunas duplicadas 
        df = df.loc[:, ~df.columns.duplicated()]
        st.success('Dados carregados')
        st.dataframe(df)
    else:
          df = pd.DataFrame(columns = [
              'Nome Completo', 'Máquina', 'Peças produzidas',
            'Turno', 'Data de registro', 'Peças Inteiras', 'Peças com defeitos'
            ])

     #Registrar novos dados no arquivo     
    st.sidebar.header('Registre aqui os novos dados de produção')
    st.sidebar.subheader('Registre nos campos abaixo: ')
    with st.sidebar.form('Formulário', clear_on_submit = True):
        novo_nome = st.text_input('Nome completo:')
        maquina = st.selectbox('Maquina:', ['Maquina 1', 'Maquina 2', 'Maquina 3'])
        novas_peças_produzidas = st.number_input('Peças produzidas: ', min_value = 0)
        novo_turno = st.text_input('Turno:')
        novo_dia = st.date_input('Data do registro:')
        nova_Pecas_Inteiras = st.number_input('Peças Inteiras:', min_value = 1)
        nova_Pecas_com_defeitos = st.number_input('Peças com defeitos:', min_value = 0)
        
        bt1 = st.form_submit_button('Registrar')
        if bt1:
            novo = {'Nome Completo':[novo_nome],
                    'Maquina':[maquina],
                    'Peças produzidas':[novas_peças_produzidas],
                    'Turno':[novo_turno],
                    'Data de registro':[novo_dia],
                    'Peças Inteiras':[nova_Pecas_Inteiras],
                    'Peças com defeitos':[nova_Pecas_com_defeitos]
                    }
            x = pd.DataFrame(novo)
            DF = pd.concat([df, x], ignore_index=True)
            st.success('Novo registro adicionado!')
            st.dataframe(DF)
            DF.to_csv('C:/Users/dayse/Desktop/Tec. Desenvolvimento de Sistemas/WPy64-31241/Programação de apps/Analise_de_dados.csv', index=False)
            st.sidebar.success("Arquivo salvo como Analise_de_dados.csv")

#Gráfico
with Aba2:
    st.title('Gráficos de produção por Máquina')

    if df.empty:
        st.info('carregue ou registre dados na aba anterior para visualizar os gráficos')
    else:
        try:
            # Garantir limpeza
            df.columns = df.columns.str.strip().str.replace(':', '', regex=False)
            df = df.loc[:, ~df.columns.duplicated()]
            
            #Converter a data 
            df['Data de registro: '] = pd.to_datetime(df['Data de registro'], errors = 'coerce')

            #Gráficos por maquinas
            maquinas = df['Maquina'].unique()
            
            for maq in maquinas:
                dados_maq = df[df['Maquina'] == maq]
                if dados_maq.empty:
                    st.warning(f'Sem dados para {maq}')
                    #Gráficos produção diaria
                
                    fig1, ax1 = plt.subplots()
                    ax1.plot(dados_maq['Data de registro'], dados_maq['Peças produzidas'], marker = 'o',
                            linestyle = '-', label = 'Peças produzidas')
                    ax1.set_title(f'Produção - {maq}')
                    ax1.set_xlabel('Data de registro')
                    ax1.set_ylabel('Peças produzidas')
                    ax1.grid(True)
                    ax1.legend()
                    st.pyplot(fig1)

        except Exception as e:
            st.error(f'Ocorreu um erro ao tentar gerar os gráficos: {e}')
       


