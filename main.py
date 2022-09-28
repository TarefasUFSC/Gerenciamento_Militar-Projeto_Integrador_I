import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from pprint import pprint


def read_csv(path):
    return pd.read_csv(path)


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


def calc_retirement(gender, dt_entry, days_before):
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
    dt_entry_datetime = datetime.strptime(str(dt_entry), "%Y-%m-%d")
    remaing_time = timedelta(days=0)
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
    ped = {"pedagio tipo 1": 0, "pedagio tipo 2": 0}
    if(datetime.now() + remaing_time>datetime.strptime("2021-12-31", "%Y-%m-%d")):
        ped["pedagio 17%"] = ( remaing_time + timedelta(days = (remaing_time.days*0.17))).days
        ped["pedagio 4 meses"] = ( remaing_time + relativedelta(months=+4)).days

    return datetime.now() + remaing_time, ped


def analyse_retirement(df):
    nomes, matriculas = df['nome'], df['matrícula']. astype(int)
    rets_remaining_time = []
    ret_data = []
    for mat in matriculas:
        line = df[df['matrícula'] == mat]
        sx = line['sexo'].values[0]
        #print(sx)
        dt_entry = line['data de ingresso'].values[0]
        days_before = line['tempo anterior_tempo em dias'].values[0]
        ret_prev,ped = calc_retirement(sx, dt_entry,  days_before)
        
        data = {
            "Nome": line['nome'].values[0],
            "Matricula": mat,
            "Data Prevista para aposentadoria (sem pedágio)": f'{ret_prev.day}/{ret_prev.month}/{ret_prev.year}', 
            "Opções de Pedágio (em dias)": ped}
        ret_data.append(data)
    return ret_data


def main():
    df = read_csv("banco_de_pessoal.csv")
    print("1 - Ver dados sumarizados")
    print("2 - Ver dados de aposentadoria")
    choice = int(input("Escolha uma opção: "))
    if(choice == 1):
        print("Aguarde, processando...")
        summarized_dt = summarize_data(df)
        pprint(summarized_dt)
    if(choice == 2):
        print("Aguarde, processando...")
        ret_data = analyse_retirement(df)
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
    rets_dt = analyse_retirement(df)
    


if __name__ == "__main__":
    main()
