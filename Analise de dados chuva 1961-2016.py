import pandas as pd
import matplotlib.pyplot as plt


def carrega_dados():
    # Carrega os dados do arquivo CSV.
    # Usamos parse_dates para converter a coluna de data para datetime.
    # Também usamos dayfirst para que o pandas entenda que o dia vem antes do mês no formato da data.
    df = pd.read_csv('OK_Anexo_Arquivo_Dados_Projeto.csv', sep=';', parse_dates=['data'], dayfirst=True)

    # Filtra os dados removendo linhas com precipitação negativa, que são consideradas inválidas.
    df = df[df['precip'] >= 0]

    return df


def mes_mais_chuvoso(df):
    # Cria uma nova coluna combinando o ano e o mês para cada linha.
    df['ano_mes'] = df['data'].dt.to_period('M')

    # Agrupa os dados por ano/mês e calcula a soma total de precipitação para cada grupo.
    total_precip_por_mes = df.groupby('ano_mes')['precip'].sum()

    # Encontra o mês com a maior precipitação.
    mes, precip = total_precip_por_mes.idxmax(), total_precip_por_mes.max()

    return mes, precip


def temp_media_por_mes(df, mes):
    # Cria um filtro para selecionar apenas as linhas correspondentes ao mês escolhido e entre os anos 2006 e 2016.
    filtro = (df['data'].dt.month == mes) & (df['data'].dt.year.between(2006, 2016))

    # Calcula a temperatura média mínima para as linhas selecionadas.
    media_temperatura = df.loc[filtro, 'minima'].mean()

    return media_temperatura


def gera_grafico(df, mes):
    # Cria um filtro para selecionar apenas as linhas correspondentes ao mês escolhido e entre os anos 2006 e 2016.
    filtro = (df['data'].dt.month == mes) & (df['data'].dt.year.between(2006, 2016))

    # Agrupa os dados por ano e calcula a temperatura mínima média para cada grupo.
    medias_por_ano = df.loc[filtro].groupby(df['data'].dt.year)['minima'].mean()

    # Cria um gráfico de barras com as médias calculadas.
    plt.bar(medias_por_ano.index, medias_por_ano.values)
    plt.xlabel('Ano')
    plt.ylabel('Temperatura Mínima Média')
    plt.title(f'Temperatura Mínima Média no mês {mes} (2006-2016)')
    plt.show()


def main():
    df = carrega_dados()

    mes, precip = mes_mais_chuvoso(df)
    print(f'Mês mais chuvoso: {mes} com precipitação total de {precip}')

    media_temperatura = temp_media_por_mes(df, 8)
    print(f'Média de temperatura mínima em agosto entre 2006 e 2016: {media_temperatura}')

    gera_grafico(df, 8)


if __name__ == '__main__':
    main()
