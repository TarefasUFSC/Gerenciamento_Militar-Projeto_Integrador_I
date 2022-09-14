import pandas as pd
from datetime import datetime
from pprint import pprint

def read_csv(path):
    return pd.read_csv(path)

def summarize_data(df):
    genero = get_gender_data(df)
    posto = get_rank_data(df)
    antiguidade_media = 0 #não sei bem o que é esse campo ainda
    cidade_lotacao = get_city_data(df)
    media_anos_servico = get_mean_service_time(df)
    media_idade = get_mean_age(df)
    comportamento = get_behavior_data(df)
    formacao = get_fomation_data(df)
    cursos = get_couses_data(df)
    idiomas = get_language_data(df)
    afastados = get_away_data(df)
    restricoes = get_restrictions_data(df)
    
    data ={
    "genero":genero, 
    "posto":posto, 
    "cidade_lotacao":cidade_lotacao, 
    "media_anos_servico":media_anos_servico, 
    "media_idade":media_idade, 
    "comportamento":comportamento, 
    "formacao":formacao, 
    "cursos":cursos, 
    "idiomas":idiomas, 
    "afastados":afastados, 
    "restricoes":restricoes
    }
    return data

def get_restrictions_data(df):
    restricoes = {'total': 0, 'motivo': {}}
    tipo_restricao = df['restrição_tipo'].unique()
    for tipo in tipo_restricao:
        if(str(tipo) == 'nan'):
            continue
        restricoes['motivo'][tipo] = 0
    for tipo in df['restrição_tipo']:
        if(str(tipo) == 'nan'):
            continue
        restricoes['motivo'][tipo] += 1
        restricoes['total'] += 1
    return restricoes
def get_away_data(df):
    afastados = {'total': 0, 'motivo': {}}
    tipo_afastamento = df['afastamento_tipo'].unique()
    for tipo in tipo_afastamento:
        if(str(tipo) == 'nan'):
            continue
        afastados['motivo'][tipo] = 0
    for tipo in df['afastamento_tipo']:
        if(str(tipo) == 'nan'):
            continue
        afastados['motivo'][tipo] += 1
        afastados['total'] += 1
    return afastados
def get_language_data(df):
    idiomas = {}
    languages = df['idioma'].unique()
    for lang in languages:
        if(str(lang) == 'nan'):
            continue
        idiomas[lang] = 0
    for lang in df['idioma']:
        if(str(lang) == 'nan'):
            continue
        idiomas[lang] += 1
    return idiomas

def get_couses_data(df):
    cursos = {}
    courses_types = ['cursos de formação','cursos pm','outros cursos civis']
    courses = []
    for course_type in courses_types:
        courses.extend(df[course_type].unique())
    for course in courses:
        if(str(course) == 'nan' or str(course) == '-'):
            continue
        cursos[course] = 0
        
    for course_type in courses_types:
        for course in df[course_type]:
            if(str(course) == 'nan' or str(course) == '-'):
                continue
            cursos[course] += 1
    return cursos

def get_fomation_data(df):
    formacao = {}
    txt_none = "Sem Informação"
    formacoes = df['formação'].unique()
    for form in formacoes:
        if(str(form) == 'nan'):
            form = txt_none
        formacao[form] = 0
    for form in df['formação']:
        if(str(form) == 'nan'):
            form = txt_none
        formacao[form] += 1
    return formacao

def get_behavior_data(df):
    comportamento = {}
    txt_none = "Sem Informação"
    comportamentos = df['comportamento'].unique()
    for comp in comportamentos:
        if(str(comp) == 'nan'):
            comp = txt_none
        comportamento[comp] = 0
    for comp in df['comportamento']:
        if(str(comp) == 'nan'):
            comp = txt_none
        comportamento[comp] += 1
    return comportamento

def get_mean_age(df):
    mean_idade = 0
    for dt in df["data de nascimento"]:
        year,month,day = dt.split("-")
        diff = datetime.now().year - int(year)
        mean_idade += diff
        #print(dt,year, diff)
    return mean_idade/len(df["data de nascimento"])

def get_mean_service_time(df):
    media_anos_servico = 0
    for dt in df["data de ingresso"]:
        year,month,day = dt.split("-")
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
    
def main():
    df = read_csv("banco_de_pessoal.csv")
    summarized_dt = summarize_data(df)
    pprint(summarized_dt)

if __name__ == "__main__":
    main()

