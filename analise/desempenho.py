import time # medir a eficiência dos meu algoritmo
import tracemalloc

from modelos.atividade import Atividade
from algoritimos.guloso import selecionar_guloso
from algoritimos.programacao_dinamica import selecionar_dinamico
from algoritimos.merge_sort import merge_sort, por_horario_fim, por_horario_inicio, por_prioridade, por_nome

#  Medição


def medir_tempo(funcao, *args) -> tuple: # *args  : Argumentos passados para a função.

    inicio = time.perf_counter() # Executa uma função e mede seu tempo de execução em milissegundos.
    resultado = funcao(*args)
    fim = time.perf_counter()

    tempo_ms = (fim - inicio) * 1000
    return resultado, tempo_ms


def medir_memoria(funcao, *args) -> tuple:

    tracemalloc.start()
    resultado = funcao(*args)
    _, pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    memoria_kb = pico / 1024
    return resultado, memoria_kb


#  Comparação entre algoritmos                                         

def comparar_algoritmos(atividades: list[Atividade], usar_participantes: bool = False) -> dict:
    """
    Executa o Algoritmo Guloso e a Programação Dinâmica sobre o mesmo
    conjunto de atividades e coleta métricas de desempenho de ambos.
    """
    criterio = "participantes" if usar_participantes else "prioridade"

    # Guloso 
    result_guloso,  tempo_guloso  = medir_tempo(selecionar_guloso, atividades)
    _,              mem_guloso    = medir_memoria(selecionar_guloso, atividades)

    # --- Programação Dinâmica ---
    result_pd,      tempo_pd      = medir_tempo(selecionar_dinamico, atividades, usar_participantes)
    _,              mem_pd        = medir_memoria(selecionar_dinamico, atividades, usar_participantes)

    # --- Benefício total de cada solução ---
    def beneficio(lista):
        return sum(a.participantes if usar_participantes else a.prioridade for a in lista)

    return {
        "total_entrada"     : len(atividades),
        "criterio_peso"     : criterio,
        "guloso": {
            "selecionadas"  : result_guloso,
            "quantidade"    : len(result_guloso),
            "beneficio"     : beneficio(result_guloso),
            "tempo_ms"      : round(tempo_guloso, 4),
            "memoria_kb"    : round(mem_guloso, 4),
        },
        "dinamico": {
            "selecionadas"  : result_pd,
            "quantidade"    : len(result_pd),
            "beneficio"     : beneficio(result_pd),
            "tempo_ms"      : round(tempo_pd, 4),
            "memoria_kb"    : round(mem_pd, 4),
        },
    }


def comparar_ordenacoes(atividades: list[Atividade]) -> dict:
    """
    Mede o tempo do Merge Sort para cada critério de ordenação.

    Parâmetros:
        atividades (list[Atividade]): Conjunto de entrada.

    Retorna:
        dict com o tempo de cada critério de ordenação.
    """
    criterios = {
        "por_horario_fim"   : por_horario_fim,
        "por_horario_inicio": por_horario_inicio,
        "por_prioridade"    : por_prioridade,
        "por_nome"          : por_nome,
    }

    resultados = {}
    for nome_criterio, chave in criterios.items():
        _, tempo = medir_tempo(merge_sort, atividades, chave)
        resultados[nome_criterio] = round(tempo, 4)

    return resultados

#  Exibição

def exibir_comparacao(metricas: dict) -> None:

    g = metricas["guloso"]
    d = metricas["dinamico"]

    print("\n" + "=" * 65)
    print("  COMPARAÇÃO DE DESEMPENHO")
    print("=" * 65)
    print(f"  Atividades na entrada : {metricas['total_entrada']}")
    print(f"  Critério de peso (PD) : {metricas['criterio_peso']}")
    print("-" * 65)
    print(f"  {'Métrica':<30} {'Guloso':>14} {'P. Dinâmica':>14}")
    print("-" * 65)
    print(f"  {'Qtd. selecionadas':<30} {g['quantidade']:>14} {d['quantidade']:>14}")
    print(f"  {'Benefício total':<30} {g['beneficio']:>14} {d['beneficio']:>14}")
    print(f"  {'Tempo (ms)':<30} {g['tempo_ms']:>14.4f} {d['tempo_ms']:>14.4f}")
    print(f"  {'Memória pico (KB)':<30} {g['memoria_kb']:>14.4f} {d['memoria_kb']:>14.4f}")
    print("=" * 65)

    # Análise automática
    print("\n  ANÁLISE:")
    if g["quantidade"] > d["quantidade"]:
        print(f"  → Guloso selecionou mais atividades ({g['quantidade']} vs {d['quantidade']})")
    elif d["quantidade"] > g["quantidade"]:
        print(f"  → PD selecionou mais atividades ({d['quantidade']} vs {g['quantidade']})")
    else:
        print(f"  → Ambos selecionaram a mesma quantidade ({g['quantidade']})")

    if d["beneficio"] > g["beneficio"]:
        diff = d["beneficio"] - g["beneficio"]
        print(f"  → PD obteve benefício maior em {diff} pontos de {metricas['criterio_peso']}")
    elif g["beneficio"] > d["beneficio"]:
        diff = g["beneficio"] - d["beneficio"]
        print(f"  → Guloso obteve benefício maior em {diff} pontos (resultado incomum)")
    else:
        print(f"  → Ambos obtiveram o mesmo benefício total")

    if g["tempo_ms"] < d["tempo_ms"]:
        print(f"  → Guloso foi mais rápido")
    else:
        print(f"  → PD foi mais rápido")

    print("=" * 65)


def exibir_comparacao_ordenacoes(metricas: dict, total: int) -> None:
    """
    Exibe o tempo do Merge Sort para cada critério de ordenação.

    Parâmetros:
        metricas (dict): Resultado de comparar_ordenacoes().
        total    (int) : Total de atividades ordenadas.
    """
    print("\n" + "=" * 50)
    print("  DESEMPENHO — MERGE SORT POR CRITÉRIO")
    print("=" * 50)
    print(f"  Total de atividades: {total}\n")
    print(f"  {'Critério':<25} {'Tempo (ms)':>12}")
    print("-" * 50)
    for criterio, tempo in metricas.items():
        print(f"  {criterio:<25} {tempo:>12.4f}")
    print("=" * 50)