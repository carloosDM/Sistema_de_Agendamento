from modelos.atividade import Atividade
from algoritimos.merge_sort import merge_sort, por_horario_fim


def selecionar_guloso(atividades: list[Atividade]) -> list[Atividade]:
    """
    Seleciona o maior número possível de atividades sem conflito de horário.
    Utiliza a estratégia gulosa clássica: sempre escolhe a atividade
    que termina mais cedo dentre as compatíveis com a última selecionada.

    Parâmetros:
        atividades (list[Atividade]): Lista de atividades cadastradas.

    Retorna:
        list[Atividade]: Subconjunto de atividades sem sobreposição,
                         com a maior quantidade possível.

    Complexidade:
        Ordenação : O(n log n) — Merge Sort
        Seleção   : O(n)       — percorre a lista uma vez
        Total     : O(n log n)
    """
    if not atividades:
        return []

    # Passo 1: ordena pelo horário de fim (decisão central do algoritmo guloso)
    ordenadas = merge_sort(atividades, chave=por_horario_fim)

    # Passo 2: seleciona a primeira atividade (a que termina mais cedo)
    selecionadas = [ordenadas[0]]

    # Passo 3: percorre as restantes e seleciona as compatíveis
    for candidata in ordenadas[1:]:
        ultima_selecionada = selecionadas[-1]

        # Só adiciona se a candidata começa APÓS o fim da última selecionada
        if candidata.inicio_em_minutos() >= ultima_selecionada.fim_em_minutos():
            selecionadas.append(candidata)

    return selecionadas


def exibir_resultado_guloso(selecionadas: list[Atividade]) -> None: # Apenas formata e imprime esse resultado no terminal. Duas linhas interessantes:
    """
    Exibe no terminal o resultado da seleção gulosa de forma formatada.

    Parâmetros:
        selecionadas (list[Atividade]): Atividades selecionadas pelo algoritmo.
    """
    print("\n" + "=" * 60)
    print("  RESULTADO — ALGORITMO GULOSO")
    print("=" * 60)

    if not selecionadas:
        print("  Nenhuma atividade foi selecionada.")
        print("=" * 60)
        return

    print(f"  Total de atividades selecionadas: {len(selecionadas)}\n")

    for i, atividade in enumerate(selecionadas, start=1):
        print(f"  {i:02}. {atividade}")

    prioridade_total = sum(a.prioridade for a in selecionadas)
    participantes_total = sum(a.participantes for a in selecionadas)

    print("\n" + "-" * 60)
    print(f"  Prioridade acumulada  : {prioridade_total}")
    print(f"  Participantes totais  : {participantes_total}")
    print("=" * 60)