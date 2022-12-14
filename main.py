import pandas as pd
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from pprint import pprint


def read_csv(path_militares, path_tipo_tempo, path_militar_tempo, path_cursos, path_militar_curso, path_tipo_curso):
    return pd.read_csv(path_militares), pd.read_csv(path_tipo_tempo), pd.read_csv(path_militar_tempo), pd.read_csv(path_cursos), pd.read_csv(path_militar_curso), pd.read_csv(path_tipo_curso)


def summarize_data(df, df_cursos, df_militar_curso, df_tipo_curso):
    genero = get_gender_data(df)

    posto = get_rank_data(df)

    cidade_lotacao = get_city_data(df)

    media_anos_servico = get_mean_service_time(df)

    media_idade = get_mean_age(df)

    comportamento = get_behavior_data(df)

    formacao = get_fomation_data(
        df, df_cursos, df_militar_curso)

    cursos = get_couses_data(df, df_cursos, df_militar_curso)

    idiomas = get_language_data(df)

    afastados = get_away_data(df)

    restricoes = get_restrictions_data(df)

    data = {
        "genero": genero,
        "posto": posto,
        "cidade_lotacao": cidade_lotacao,
        "media_anos_servico": media_anos_servico,
        "media_idade": media_idade,
        "comportamento": comportamento,
        "formacao": formacao,
        "cursos": cursos,
        "idiomas": idiomas,
        "afastados": afastados,
        "restricoes": restricoes
    }
    return data


def get_restrictions_data(df):
    restricoes = {'total': 0, 'motivo': {}}
    tipo_restricao = df['restrição_tipo'].unique()
    for tipo in tipo_restricao:
        if (str(tipo) == 'nan'):
            continue
        restricoes['motivo'][tipo] = 0
    for tipo in df['restrição_tipo']:
        if (str(tipo) == 'nan'):
            continue
        restricoes['motivo'][tipo] += 1
        restricoes['total'] += 1
    return restricoes


def get_away_data(df):
    afastados = {'total': 0, 'motivo': {}}
    tipo_afastamento = df['afastamento_tipo'].unique()
    for tipo in tipo_afastamento:
        if (str(tipo) == 'nan'):
            continue
        afastados['motivo'][tipo] = 0
    for tipo in df['afastamento_tipo']:
        if (str(tipo) == 'nan'):
            continue
        afastados['motivo'][tipo] += 1
        afastados['total'] += 1
    return afastados


def get_language_data(df):
    idiomas = {}
    languages = df['idioma'].unique()
    for lang in languages:
        if (str(lang) == 'nan'):
            continue
        idiomas[lang] = 0
    for lang in df['idioma']:
        if (str(lang) == 'nan'):
            continue
        idiomas[lang] += 1
    return idiomas


def get_couses_data(df, df_cursos, df_militar_curso):
    cursos = {}
    c_df = df_militar_curso.join(
        df_cursos, on='id_curso', how='left', lsuffix='_militar_curso', rsuffix='_cursos')
    # c_df.to_csv("c_df.csv")
    c_df = c_df.query(
        'id_tipo_curso == 1 or id_tipo_curso == 2 or id_tipo_curso == 3')
    # print(c_df)
    courses = c_df['nm_curso'].unique().tolist()
    # print(formacoes)
    for course in courses:
        cursos[course] = 0

    for course in c_df['nm_curso']:
        cursos[course] += 1
    return cursos


def get_fomation_data(df, df_cursos, df_militar_curso):
    formacao = {}
    c_df = df_militar_curso.join(
        df_cursos, on='id_curso', how='left', lsuffix='_militar_curso', rsuffix='_cursos')
    # c_df.to_csv("c_df.csv")
    c_df = c_df[c_df['id_tipo_curso'] == 0]
    # print(c_df)
    formacoes = c_df['nm_curso'].unique().tolist()
    # print(formacoes)
    for form in formacoes:
        formacao[form] = 0
    for form in c_df['nm_curso']:
        formacao[form] += 1
    return formacao


def get_behavior_data(df):
    comportamento = {}
    txt_none = "Sem Informação"
    comportamentos = df['comportamento'].unique()
    for comp in comportamentos:
        if (str(comp) == 'nan'):
            comp = txt_none
        comportamento[comp] = 0
    for comp in df['comportamento']:
        if (str(comp) == 'nan'):
            comp = txt_none
        comportamento[comp] += 1
    return comportamento


def get_mean_age(df):
    mean_idade = 0
    for dt in df["data de nascimento"]:
        year, month, day = dt.split("-")
        diff = datetime.now().year - int(year)
        mean_idade += diff
        #print(dt,year, diff)
    return mean_idade/len(df["data de nascimento"])


def get_mean_service_time(df):
    media_anos_servico = 0
    for dt in df["data de ingresso"]:
        year, month, day = dt.split("-")
        diff = datetime.now().year - int(year)
        media_anos_servico += diff
        #print(dt,year, diff)
    return media_anos_servico/len(df["data de ingresso"])


def get_gender_data(df):
    genero = {}
    genders = df['sexo'].unique()
    for gen in genders:
        genero[gen] = 0
    for gen in df['sexo']:
        genero[gen] += 1
    return genero


def get_rank_data(df):
    posto = {}
    ranks = df['posto/graduação'].unique()
    for rank in ranks:
        posto[rank] = 0
    for rank in df['posto/graduação']:
        posto[rank] += 1
    return posto


def get_city_data(df):
    cidade_lotacao = {}
    cities = df['lotação_cidade'].unique()
    for city in cities:
        cidade_lotacao[city] = 0
    for city in df['lotação_cidade']:
        cidade_lotacao[city] += 1
    return cidade_lotacao

def calc_theoretical_retirement(dt_theoretical_retirement,dt_entry,min_mili_time_years,max_civil_time_years,tmp_civil,tmp_military):
    #print("dt_theoretical_retirement",dt_theoretical_retirement, "tmp_civil",tmp_civil,"tmp_military",tmp_military)
    if(max_civil_time_years):
        if(tmp_civil>365,25*max_civil_time_years):
            tmp_civil=365,25*max_civil_time_years
    time_spent_on_military = (dt_theoretical_retirement - dt_entry - timedelta(days=tmp_military)).days
    if(min_mili_time_years):
        if(time_spent_on_military<365,25*min_mili_time_years):
            time_4_month_years = int((min_mili_time_years-time_spent_on_military)/365.25)
    else:
        time_4_month_years = 0
    dt_theoretical_retirement = dt_theoretical_retirement - timedelta(days=tmp_civil) - timedelta(days=tmp_military)
    
    #print("dt_theoretical_retirement",dt_theoretical_retirement)
    return dt_theoretical_retirement,time_4_month_years

def calc_retirement(gender, dt_entry, ids_tipo, qtds_dias, df_tipo_tempo):
    '''
    Homens
        - Se sua data de ingresso é até 19/12/2013: deve ter 35 anos de serviço, não tem exigência de tempo militar, pode somar todo o tempo que tiver fora.
        - Se sua data de ingresso é posterior a 19/12/2013: deve ter 35 anos de serviço, sendo, no mínimo, 30 anos de serviço militar, podendo usar 5 anos anteriores de tempo que não seja militar.
    Mulheres
        - Se sua data de ingresso é até 31/08/2006: deve ter 35 anos de serviço, não tem exigência de tempo militar, pode somar todo o tempo que tiver fora
        - Se sua data de ingresso é entre 01/09/2006 e até 19/12/2013: deve ter 35 anos de serviço, sendo, no mínimo, 15 anos de serviço militar, podendo usar 20 anos anteriores de tempo que não seja militar.
        - Se sua data de ingresso é posterior a 19/12/2013: deve ter 35 anos de serviço, sendo, no mínimo, 30 anos de serviço militar, podendo usar 5 anos anteriores de tempo que não seja militar.
    “Pedágios”
        - “17%”
            Se até 31/12/2021 tiver fechado as regras anteriores, não há pedágio. Caso contrário, do tempo total que restar para fechar a regra em 01/01/2022 deve ser acrescentado 17%.
        - “4 meses”
            Se até 31/12/2021 tiver fechado as regras anteriores, não há pedágio. Caso contrário, do tempo que restar para fechar o tempo militar em 01/01/2022 deve ser acrescentado 4 meses para cada ano faltante.
    '''
    # print(str(dt_entry))

    # A conta do pedágio de 17% é sobre a diff de tempo entre a aposentadoria teorica e a data de mudança da regra 01/01/2022

    dt_entry = datetime.strptime(str(dt_entry), "%Y-%m-%d")
    dt_theoretical_retirement = dt_entry + relativedelta(years=+35)
    dt_ret = datetime.now()

    time_4_month_years = 0
    toll_17_pc = 0

    tmp_military = 0
    tmp_civil = 0
    #print(qtds_dias)
    for i, tipo in enumerate(ids_tipo):
        if (df_tipo_tempo[df_tipo_tempo['id_tipo'] == tipo]['is_militar'].values[0] == 1):
            tmp_military += int(qtds_dias[i])
        else:
            tmp_civil += int(qtds_dias[i])
    

    if (gender == "Masculino"):
        if (dt_entry <= datetime.strptime("2013-12-19", "%Y-%m-%d")):
           dt_theoretical_retirement,time_4_month_years = calc_theoretical_retirement(dt_theoretical_retirement =dt_theoretical_retirement ,dt_entry =dt_entry ,min_mili_time_years =None ,max_civil_time_years =None ,tmp_civil =tmp_civil ,tmp_military = tmp_military)
        if (dt_entry > datetime.strptime("2013-12-19", "%Y-%m-%d")):
            dt_theoretical_retirement,time_4_month_years = calc_theoretical_retirement(dt_theoretical_retirement =dt_theoretical_retirement ,dt_entry =dt_entry ,min_mili_time_years =30 ,max_civil_time_years =5 ,tmp_civil =tmp_civil ,tmp_military = tmp_military)
    else:
        if (dt_entry <= datetime.strptime("2006-08-31", "%Y-%m-%d")):
            dt_theoretical_retirement,time_4_month_years = calc_theoretical_retirement(dt_theoretical_retirement =dt_theoretical_retirement ,dt_entry =dt_entry ,min_mili_time_years =None ,max_civil_time_years =None ,tmp_civil =tmp_civil ,tmp_military = tmp_military)
        if (dt_entry >= datetime.strptime("2006-09-01", "%Y-%m-%d") and dt_entry <= datetime.strptime("2013-12-19", "%Y-%m-%d")):
            dt_theoretical_retirement,time_4_month_years = calc_theoretical_retirement(dt_theoretical_retirement =dt_theoretical_retirement ,dt_entry =dt_entry ,min_mili_time_years =20 ,max_civil_time_years =15 ,tmp_civil =tmp_civil ,tmp_military = tmp_military)
        if (dt_entry > datetime.strptime("2013-12-19", "%Y-%m-%d")):
            dt_theoretical_retirement,time_4_month_years = calc_theoretical_retirement(dt_theoretical_retirement =dt_theoretical_retirement ,dt_entry =dt_entry ,min_mili_time_years =30 ,max_civil_time_years =5 ,tmp_civil =tmp_civil ,tmp_military = tmp_military)

    if(dt_theoretical_retirement > datetime.strptime("2021-12-31", "%Y-%m-%d")):
        #print("diff 17%: ",(dt_theoretical_retirement - datetime.strptime("2022-01-01", "%Y-%m-%d")).days)
        toll_17_pc = int(0.17*(dt_theoretical_retirement - datetime.strptime("2022-01-01", "%Y-%m-%d")).days)
    else:
        toll_17_pc = 0
    #print("toll_17_pc",toll_17_pc)
    if(time_4_month_years > 0):
        toll_4_month = int(4*(time_4_month_years/365.25))
    else:
        toll_4_month = 0
    dt_ret = dt_theoretical_retirement + timedelta(days=toll_17_pc) + timedelta(days=toll_4_month)
    if(dt_ret < datetime.now()):
        dt_ret = datetime.now()
    return dt_ret,{"toll_17_pc (days)":toll_17_pc,"toll_4_month (months)":toll_4_month,"tmp_military (days)":tmp_military,"tmp_civil (days)":tmp_civil}


def analyse_retirement(df_militares, df_tipo_tempo, df_tempo_militares):
    nomes, matriculas = df_militares['nome'], df_militares['matrícula']. astype(
        int)
    rets_remaining_time = []
    ret_data = []
    for mat in matriculas:
        line = df_militares[df_militares['matrícula'] == mat]
        sx = line['sexo'].values[0]
        #print(mat)
        ids_tipo, qtds_dias = [], []
        tipo_tempo = df_tempo_militares[df_tempo_militares['matricula_militar'] == mat]
        if (len(tipo_tempo) > 0):
            for (_, row) in tipo_tempo.iterrows():
                ids_tipo.append(row['id_tipo'])
                qtds_dias.append(row['tempo_dias'])
            #print(ids_tipo, qtds_dias)
        dt_entry = line['data de ingresso'].values[0]
        days_before = line['tempo anterior_tempo em dias'].values[0]
        ret_prev, ped = calc_retirement(
            sx, dt_entry, ids_tipo, qtds_dias, df_tipo_tempo)
        #print()
        data = {
            "Nome": line['nome'].values[0],
            "Matricula": mat,
            "Data Prevista para aposentadoria (com pedágio)": f'{ret_prev.day}/{ret_prev.month}/{ret_prev.year}',
            "Pedágios aplicados": ped}
        ret_data.append(data)
    return ret_data


def main():
    df_militares, df_tipo_tempo, df_tempo_militares, df_cursos, df_militar_curso, df_tipo_curso = read_csv(
        "banco_de_pessoal.csv", "tipo_tempo.csv", "militar_tipo_tempo.csv", "cursos.csv", "militar_curso.csv", "cursos_tipo.csv")
    print("1 - Ver dados sumarizados")
    print("2 - Ver dados de aposentadoria")
    choice = int(input("Escolha uma opção: "))
    if (choice == 1):
        print("Aguarde, processando...")
        summarized_dt = summarize_data(
            df_militares, df_cursos, df_militar_curso, df_tipo_curso)
        pprint(summarized_dt)
    if (choice == 2):
        print("Aguarde, processando...")
        ret_data = analyse_retirement(
            df_militares, df_tipo_tempo, df_tempo_militares)
        print("1 - ver todos os dados")
        print("2 - ver dados de um militar específico")
        choice = int(input("Escolha uma opção: "))
        if (choice == 1):
            pprint(ret_data)
        if (choice == 2):
            print("Digite a matrícula do militar: ")
            mat = int(input())
            for data in ret_data:
                if (data["Matricula"] == mat):
                    pprint(data)
                    break
    rets_dt = analyse_retirement(
        df_militares, df_tipo_tempo, df_tempo_militares)


if __name__ == "__main__":
    main()
