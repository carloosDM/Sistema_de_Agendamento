import json
import os


# ------------------------------------------------------------------ #
#  Conjuntos de teste                                                  #
# ------------------------------------------------------------------ #

TESTE_PEQUENO = [
    {"codigo": "P01", "nome": "Reunião de Abertura",       "inicio": "08:00", "fim": "09:00", "prioridade": 4, "participantes": 12},
    {"codigo": "P02", "nome": "Treinamento de Segurança",  "inicio": "08:30", "fim": "10:00", "prioridade": 5, "participantes": 30},
    {"codigo": "P03", "nome": "Palestra de Inovação",      "inicio": "09:00", "fim": "10:30", "prioridade": 3, "participantes": 50},
    {"codigo": "P04", "nome": "Coffee Break",              "inicio": "10:00", "fim": "10:30", "prioridade": 1, "participantes": 40},
    {"codigo": "P05", "nome": "Workshop de Liderança",     "inicio": "10:30", "fim": "12:00", "prioridade": 4, "participantes": 20},
    {"codigo": "P06", "nome": "Reunião de Equipe",         "inicio": "11:00", "fim": "12:00", "prioridade": 3, "participantes": 10},
    {"codigo": "P07", "nome": "Alinhamento Estratégico",   "inicio": "13:00", "fim": "14:00", "prioridade": 5, "participantes": 15},
    {"codigo": "P08", "nome": "Encerramento do Dia",       "inicio": "14:00", "fim": "15:00", "prioridade": 2, "participantes": 60},
]

TESTE_MEDIO = [
    {"codigo": "M01", "nome": "Planejamento Anual",        "inicio": "07:00", "fim": "08:30", "prioridade": 5, "participantes": 25},
    {"codigo": "M02", "nome": "Integração de Novos",       "inicio": "07:30", "fim": "09:00", "prioridade": 3, "participantes": 18},
    {"codigo": "M03", "nome": "Revisão de Metas",          "inicio": "08:30", "fim": "09:30", "prioridade": 4, "participantes": 12},
    {"codigo": "M04", "nome": "Palestra Motivacional",     "inicio": "09:00", "fim": "10:30", "prioridade": 2, "participantes": 80},
    {"codigo": "M05", "nome": "Treinamento Técnico",       "inicio": "09:30", "fim": "11:00", "prioridade": 5, "participantes": 15},
    {"codigo": "M06", "nome": "Reunião com Cliente",       "inicio": "10:30", "fim": "11:30", "prioridade": 5, "participantes": 8},
    {"codigo": "M07", "nome": "Coffee Break Manhã",        "inicio": "11:00", "fim": "11:30", "prioridade": 1, "participantes": 50},
    {"codigo": "M08", "nome": "Workshop Ágil",             "inicio": "11:30", "fim": "13:00", "prioridade": 4, "participantes": 22},
    {"codigo": "M09", "nome": "Almoço de Equipe",          "inicio": "12:00", "fim": "13:30", "prioridade": 2, "participantes": 40},
    {"codigo": "M10", "nome": "Apresentação de Projetos",  "inicio": "13:00", "fim": "14:30", "prioridade": 4, "participantes": 35},
    {"codigo": "M11", "nome": "Treinamento de Vendas",     "inicio": "13:30", "fim": "15:00", "prioridade": 3, "participantes": 20},
    {"codigo": "M12", "nome": "Reunião de Diretoria",      "inicio": "14:30", "fim": "16:00", "prioridade": 5, "participantes": 10},
    {"codigo": "M13", "nome": "Feedback Individual",       "inicio": "15:00", "fim": "16:00", "prioridade": 4, "participantes": 5},
    {"codigo": "M14", "nome": "Palestra de Bem-Estar",     "inicio": "16:00", "fim": "17:00", "prioridade": 2, "participantes": 45},
    {"codigo": "M15", "nome": "Encerramento Semanal",      "inicio": "17:00", "fim": "18:00", "prioridade": 3, "participantes": 30},
]

TESTE_GRANDE = [
    {"codigo": "G01", "nome": "Abertura Corporativa",      "inicio": "06:00", "fim": "07:00", "prioridade": 5, "participantes": 100},
    {"codigo": "G02", "nome": "Meditação Matinal",         "inicio": "06:30", "fim": "07:00", "prioridade": 1, "participantes": 20},
    {"codigo": "G03", "nome": "Reunião de Planejamento",   "inicio": "07:00", "fim": "08:00", "prioridade": 5, "participantes": 30},
    {"codigo": "G04", "nome": "Treinamento Onboarding",    "inicio": "07:00", "fim": "09:00", "prioridade": 4, "participantes": 15},
    {"codigo": "G05", "nome": "Stand-up Desenvolvimento",  "inicio": "08:00", "fim": "08:30", "prioridade": 3, "participantes": 12},
    {"codigo": "G06", "nome": "Workshop Design Thinking",  "inicio": "08:30", "fim": "10:30", "prioridade": 4, "participantes": 25},
    {"codigo": "G07", "nome": "Palestra sobre IA",         "inicio": "08:30", "fim": "09:30", "prioridade": 5, "participantes": 70},
    {"codigo": "G08", "nome": "Revisão de Sprint",         "inicio": "09:00", "fim": "10:00", "prioridade": 4, "participantes": 18},
    {"codigo": "G09", "nome": "Treinamento de RH",         "inicio": "09:30", "fim": "11:00", "prioridade": 3, "participantes": 22},
    {"codigo": "G10", "nome": "Reunião Comercial",         "inicio": "10:00", "fim": "11:00", "prioridade": 5, "participantes": 10},
    {"codigo": "G11", "nome": "Coffee Break 1",            "inicio": "10:30", "fim": "11:00", "prioridade": 1, "participantes": 60},
    {"codigo": "G12", "nome": "Palestra de Cultura",       "inicio": "11:00", "fim": "12:00", "prioridade": 3, "participantes": 55},
    {"codigo": "G13", "nome": "Workshop de Dados",         "inicio": "11:00", "fim": "13:00", "prioridade": 5, "participantes": 20},
    {"codigo": "G14", "nome": "Alinhamento de Produto",    "inicio": "11:30", "fim": "12:30", "prioridade": 4, "participantes": 14},
    {"codigo": "G15", "nome": "Almoço Executivo",          "inicio": "12:00", "fim": "13:00", "prioridade": 2, "participantes": 8},
    {"codigo": "G16", "nome": "Treinamento de Liderança",  "inicio": "13:00", "fim": "14:30", "prioridade": 5, "participantes": 30},
    {"codigo": "G17", "nome": "Reunião de Resultados",     "inicio": "13:00", "fim": "14:00", "prioridade": 4, "participantes": 25},
    {"codigo": "G18", "nome": "Oficina de Criatividade",   "inicio": "13:30", "fim": "15:00", "prioridade": 3, "participantes": 18},
    {"codigo": "G19", "nome": "Painel com Diretores",      "inicio": "14:00", "fim": "15:30", "prioridade": 5, "participantes": 40},
    {"codigo": "G20", "nome": "Treinamento de Qualidade",  "inicio": "14:30", "fim": "16:00", "prioridade": 4, "participantes": 20},
    {"codigo": "G21", "nome": "Coffee Break 2",            "inicio": "15:00", "fim": "15:30", "prioridade": 1, "participantes": 60},
    {"codigo": "G22", "nome": "Sessão de Feedback",        "inicio": "15:30", "fim": "16:30", "prioridade": 4, "participantes": 10},
    {"codigo": "G23", "nome": "Palestra de Sustentabilidade","inicio": "15:30","fim": "16:30", "prioridade": 3, "participantes": 45},
    {"codigo": "G24", "nome": "Reunião de Inovação",       "inicio": "16:00", "fim": "17:00", "prioridade": 5, "participantes": 20},
    {"codigo": "G25", "nome": "Workshop de Comunicação",   "inicio": "16:30", "fim": "18:00", "prioridade": 3, "participantes": 28},
    {"codigo": "G26", "nome": "Treinamento de Segurança",  "inicio": "16:30", "fim": "17:30", "prioridade": 5, "participantes": 35},
    {"codigo": "G27", "nome": "Reunião de Encerramento",   "inicio": "17:00", "fim": "18:00", "prioridade": 4, "participantes": 50},
    {"codigo": "G28", "nome": "Apresentação de Resultados","inicio": "17:30", "fim": "18:30", "prioridade": 5, "participantes": 60},
    {"codigo": "G29", "nome": "Confraternização",          "inicio": "18:00", "fim": "19:30", "prioridade": 2, "participantes": 80},
    {"codigo": "G30", "nome": "Happy Hour",                "inicio": "18:30", "fim": "20:00", "prioridade": 1, "participantes": 70},
    {"codigo": "G31", "nome": "Jantar Executivo",          "inicio": "19:00", "fim": "21:00", "prioridade": 3, "participantes": 15},
    {"codigo": "G32", "nome": "Palestra de Encerramento",  "inicio": "19:30", "fim": "20:30", "prioridade": 4, "participantes": 90},
]


# ------------------------------------------------------------------ #
#  Geração dos arquivos                                                #
# ------------------------------------------------------------------ #

def gerar_arquivos(pasta_destino: str = "dados") -> None:
    """
    Salva os três conjuntos de teste em arquivos JSON na pasta informada.

    Parâmetros:
        pasta_destino (str): Caminho da pasta onde os arquivos serão salvos.
    """
    os.makedirs(pasta_destino, exist_ok=True)

    conjuntos = {
        "teste_pequeno.json": TESTE_PEQUENO,
        "teste_medio.json"  : TESTE_MEDIO,
        "teste_grande.json" : TESTE_GRANDE,
    }

    for nome_arquivo, dados in conjuntos.items():
        caminho = os.path.join(pasta_destino, nome_arquivo)
        with open(caminho, "w", encoding="utf-8") as arq:
            json.dump(dados, arq, ensure_ascii=False, indent=4)
        print(f"  Gerado: {caminho} ({len(dados)} atividades)")


if __name__ == "__main__":
    print("\nGerando conjuntos de teste...\n")
    gerar_arquivos()
    print("\nArquivos criados com sucesso!")