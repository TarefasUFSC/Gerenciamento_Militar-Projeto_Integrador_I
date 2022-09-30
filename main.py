import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from pprint import pprint


def read_csv(path_militares,path_tipo_tempo,path_militar_tempo):
    return pd.read_csv(path_militares),pd.read_csv(path_tipo_tempo),pd.read_csv(path_militar_tempo)


def summarize_data(df):
    genero = get_gender_data(df)

    posto = get_rank_data(df)

    cidade_lotacao = get_city_data(df)

    media_anos_servico = get_mean_service_time(df)

    media_idade = get_mean_age(df)

    comportamento = get_behavior_data(df)

    # Técnico em enfermagem repetiu 3x ??
    formacao = get_fomation_data(df)

    cursos = get_couses_data(df)

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


def get_couses_data(df):
    cursos = {}
    courses_types = ['cursos de formação', 'cursos pm', 'outros cursos civis']
    courses = []
    for course_type in courses_types:
        courses.extend(df[course_type].unique())
    for course in courses:
        if (str(course) == 'nan' or str(course) == '-'):
            continue
        cursos[course] = 0

    for course_type in courses_types:
        for course in df[course_type]:
            if (str(course) == 'nan' or str(course) == '-'):
                continue
            cursos[course] += 1
    return cursos


def get_fomation_data(df):
    formacao = {}
    txt_none = "Sem Informação"
    formacoes = df['formação'].unique()
    for form in formacoes:
        if (str(form) == 'nan'):
            form = txt_none
        formacao[form] = 0
    for form in df['formação']:
        if (str(form) == 'nan'):
            form = txt_none
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


def calc_retirement(gender, dt_entry,ids_tipo, qtds_dias,df_tipo_tempo):
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
    #print(str(dt_entry))
    ped_flag17,ped_flag4m = False,False
    dt_entry_datetime = datetime.strptime(str(dt_entry), "%Y-%m-%d")
    remaing_time = timedelta(days=0)
    if (gender == "Masculino"):
        if (dt_entry_datetime <= datetime.strptime("2013-12-19", "%Y-%m-%d")):
            d_t_ant = timedelta(days=0)
            for i,tipo in enumerate(ids_tipo):
                d_t_ant = d_t_ant - timedelta(days=int(qtds_dias[i]))
            
            remaing_time = timedelta(days=(35*365)) - ((datetime.now() - dt_entry_datetime) - d_t_ant) 
            if(datetime.now() + remaing_time>datetime.strptime("2021-12-31", "%Y-%m-%d")):
                ped_flag17 = True
                remaing_time += timedelta(days=(remaing_time.days*0.17))
        if (dt_entry_datetime > datetime.strptime("2013-12-19", "%Y-%m-%d")):
            mili_time = 0
            n_mili_time = 0
            for i,tipo in enumerate(ids_tipo):
                if(df_tipo_tempo[df_tipo_tempo['id_tipo'] == tipo]['is_militar'].values[0] == 1):
                    mili_time += qtd_dias[i]
                else:
                    n_mili_time += qtd_dias[i]
            if (n_mili_time/365 > 5):
                n_mili_time = 5*365
            
            remaing_time =timedelta(days=(35*365)) - ( (datetime.now() - dt_entry_datetime) - timedelta(days=mili_time[i]) - timedelta(days=n_mili_time[i]))
            if(datetime.now() + remaing_time>datetime.strptime("2021-12-31", "%Y-%m-%d")):
                ped_flag17 = True
                remaing_time += timedelta(days=(remaing_time.days*0.17))
                if(mili_time<30*365):
                    ped_flag4m = True
                    remaing_time += relativedelta(months=4)
    
    else:
        if (dt_entry_datetime <= datetime.strptime("2006-08-31", "%Y-%m-%d")):
            d_t_ant = timedelta(days=0)
            for i,tipo in enumerate(ids_tipo):
                d_t_ant = d_t_ant - timedelta(days=int(qtds_dias[i]))
            
            remaing_time = timedelta(days=(35*365)) - ((datetime.now() - dt_entry_datetime) - d_t_ant)
            if(datetime.now() + remaing_time>datetime.strptime("2021-12-31", "%Y-%m-%d")):
                ped_flag17 = True
                remaing_time += timedelta(days=(remaing_time.days*0.17))
        if (dt_entry_datetime >= datetime.strptime("2006-09-01", "%Y-%m-%d") and dt_entry_datetime <= datetime.strptime("2013-12-19", "%Y-%m-%d")):
            remaing_time = timedelta(days=(35*365))
            mili_time = 0
            n_mili_time = 0
            for i,tipo in enumerate(ids_tipo):
                if(df_tipo_tempo[df_tipo_tempo['id_tipo'] == tipo]['is_militar'].values[0] == 1):
                    mili_time += qtd_dias[i]
                else:
                    n_mili_time += qtd_dias[i]
            if (n_mili_time/365 > 15):
                n_mili_time = 15*365
            remaing_time =timedelta(days=(35*365)) - ( (datetime.now() - dt_entry_datetime) - timedelta(days=mili_time[i]) - timedelta(days=n_mili_time[i]))
            if(datetime.now() + remaing_time>datetime.strptime("2021-12-31", "%Y-%m-%d")):
                ped_flag17 = True
                remaing_time += timedelta(days=(remaing_time.days*0.17))
                if(mili_time<20*365):
                    ped_flag4m = True
                    remaing_time += relativedelta(months=4)

        
        if (dt_entry_datetime > datetime.strptime("2013-12-19", "%Y-%m-%d")):
            remaing_time = timedelta(days=(35*365))
            mili_time = 0
            n_mili_time = 0
            for i,tipo in enumerate(ids_tipo):
                if(df_tipo_tempo[df_tipo_tempo['id_tipo'] == tipo]['is_militar'].values[0] == 1):
                    mili_time += qtd_dias[i]
                else:
                    n_mili_time += qtd_dias[i]
            if (n_mili_time/365 > 5):
                n_mili_time = 5*365
            remaing_time =timedelta(days=(35*365)) - ( (datetime.now() - dt_entry_datetime) - timedelta(days=mili_time[i]) - timedelta(days=n_mili_time[i]))
            if(datetime.now() + remaing_time>datetime.strptime("2021-12-31", "%Y-%m-%d")):
                ped_flag17 = True
                remaing_time += timedelta(days=(remaing_time.days*0.17))
                if(mili_time<30*365):
                    ped_flag4m = True
                    remaing_time += relativedelta(months=4)


    '''
    if (gender == "Masculino"):
        if (dt_entry_datetime <= datetime.strptime("2013-12-19", "%Y-%m-%d")):
            # os 35 anos de serviço aqui contam trabalhos anteriores?
            remaing_time = timedelta(days=(35*365)) - ((datetime.now() - dt_entry_datetime))
        if (dt_entry_datetime > datetime.strptime("2013-12-19", "%Y-%m-%d")):
            if (days_before/365 > 5):
                days_before = 5*365
            remaing_time = timedelta(days=(35*365)) - (timedelta(days=int(days_before)) + (datetime.now() - dt_entry_datetime))
    else:
        if (dt_entry_datetime <= datetime.strptime("2006-08-31", "%Y-%m-%d")):
            remaing_time = timedelta(days=(35*365)) - ( (datetime.now() - dt_entry_datetime))
        if (dt_entry_datetime >= datetime.strptime("2006-09-01", "%Y-%m-%d") and dt_entry_datetime <= datetime.strptime("2013-12-19", "%Y-%m-%d")):
            if (days_before/365 > 20):
                days_before = 20*365
            
            remaing_time = timedelta(days=(35*365)) - (timedelta(days=int(days_before)) + (datetime.now() - dt_entry_datetime))

        
        if (dt_entry_datetime > datetime.strptime("2013-12-19", "%Y-%m-%d")):
            if (days_before/365 > 5):
                days_before = 5*365
            
            remaing_time = timedelta(days=(35*365)) - (timedelta(days=int(days_before)) + (datetime.now() - dt_entry_datetime))
    ped = {"pedagio 17%": 0, "pedagio 4 meses": 0}
    if(datetime.now() + remaing_time>datetime.strptime("2021-12-31", "%Y-%m-%d")):
        ped["pedagio 17%"] = ( remaing_time + timedelta(days = (remaing_time.days*0.17))).days
        ped["pedagio 4 meses"] = ( remaing_time + relativedelta(months=+4)).days
    '''

    return datetime.now() + remaing_time, {"pedagio 17%": ped_flag17, "pedagio 4 meses": ped_flag4m}


def analyse_retirement(df_militares,df_tipo_tempo,df_tempo_militares):
    nomes, matriculas = df_militares['nome'], df_militares['matrícula']. astype(int)
    rets_remaining_time = []
    ret_data = []
    for mat in matriculas:
        line = df_militares[df_militares['matrícula'] == mat]
        sx = line['sexo'].values[0]
        #print(sx)
        ids_tipo, qtds_dias = [], []
        tipo_tempo = df_tempo_militares[df_tempo_militares['matricula_militar'] == mat]
        if(len(tipo_tempo) > 0):
            for(_, row) in tipo_tempo.iterrows():
                ids_tipo.append(row['id_tipo'])
                qtds_dias.append(row['tempo_dias'])
            #print(ids_tipo, qtds_dias)
        dt_entry = line['data de ingresso'].values[0]
        days_before = line['tempo anterior_tempo em dias'].values[0]
        ret_prev,ped = calc_retirement(sx,dt_entry, ids_tipo, qtds_dias,df_tipo_tempo)
        
        data = {
            "Nome": line['nome'].values[0],
            "Matricula": mat,
            "Data Prevista para aposentadoria (com pedágio)": f'{ret_prev.day}/{ret_prev.month}/{ret_prev.year}', 
            "Pedágios aplicados": ped}
        ret_data.append(data)
    return ret_data


def main():
    df_militares,df_tipo_tempo,df_tempo_militares = read_csv("banco_de_pessoal.csv","tipo_tempo.csv","militar_tipo_tempo.csv")
    print("1 - Ver dados sumarizados")
    print("2 - Ver dados de aposentadoria")
    choice = int(input("Escolha uma opção: "))
    if(choice == 1):
        print("Aguarde, processando...")
        summarized_dt = summarize_data(df_militares)
        pprint(summarized_dt)
    if(choice == 2):
        print("Aguarde, processando...")
        ret_data = analyse_retirement(df_militares,df_tipo_tempo,df_tempo_militares)
        print("1 - ver todos os dados")
        print("2 - ver dados de um militar específico")
        choice = int(input("Escolha uma opção: "))
        if(choice == 1):
            pprint(ret_data)
        if(choice == 2):
            print("Digite a matrícula do militar: ")
            mat = int(input())
            for data in ret_data:
                if(data["Matricula"] == mat):
                    pprint(data)
                    break
    rets_dt = analyse_retirement(df_militares,df_tipo_tempo,df_tempo_militares)
    


if __name__ == "__main__":
    main()
