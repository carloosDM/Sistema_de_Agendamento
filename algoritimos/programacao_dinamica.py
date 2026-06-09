from modelos.atividade import Atividade
from algoritimos.merge_sort import merge_sort, por_horario_fim


def _ultimo_compativel(atividades: list[Atividade], indice: int) -> int:
    """
    Encontra o índice da última atividade que termina antes de
    'atividades[indice]' começar — ou seja, a mais recente compatível.

    Usa busca binária sobre os horários de fim.

    Parâmetros:
        atividades (list[Atividade]): Lista ordenada por horário de fim.
        indice     (int)            : Índice da atividade atual.

    Retorna:
        Índice da última atividade compatível, ou -1 se não houver nenhuma.

    Complexidade: O(log n)
    """
    inicio_atual = atividades[indice].inicio_em_minutos()
    esquerda = 0
    direita  = indice - 1
    resultado = -1

    while esquerda <= direita:
        meio = (esquerda + direita) // 2
        if atividades[meio].fim_em_minutos() <= inicio_atual:
            resultado = meio
            esquerda  = meio + 1
        else:
            direita = meio - 1

    return resultado


def selecionar_dinamico(atividades: list[Atividade],
                        usar_participantes: bool = False) -> list[Atividade]:
    """
    Seleciona atividades sem conflito maximizando o benefício total
    usando Programação Dinâmica (Weighted Job Scheduling).

    Diferente do algoritmo guloso, considera o peso de cada atividade
    (prioridade ou participantes) para tomar a decisão ótima.

    Parâmetros:
        atividades          (list[Atividade]): Lista de atividades cadastradas.
        usar_participantes  (bool)           : Se True, usa participantes como peso.
                                               Se False, usa prioridade (padrão).

    Retorna:
        list[Atividade]: Subconjunto com maior benefício total sem conflito.

    Complexidade:
        Ordenação : O(n log n)
        DP + busca: O(n log n)
        Total     : O(n log n)
    """
    if not atividades:
        return []

    # Passo 1: ordena por horário de fim (mesmo pré-requisito do guloso)
    ordenadas = merge_sort(atividades, chave=por_horario_fim)
    n = len(ordenadas)

    # Define qual atributo será o peso
    def peso(atividade: Atividade) -> int:
        return atividade.participantes if usar_participantes else atividade.prioridade

    #  Passo 2: Preenchimento da tabela DP                       
    #  dp[i] = maior benefício considerando as atividades de 0 até i 

    dp = [0] * n
    dp[0] = peso(ordenadas[0])

    for i in range(1, n):
        # Opção B: incluir a atividade i
        j = _ultimo_compativel(ordenadas, i)
        beneficio_incluindo = peso(ordenadas[i]) + (dp[j] if j >= 0 else 0)

        # Opção A: não incluir a atividade i
        beneficio_excluindo = dp[i - 1]

        dp[i] = max(beneficio_incluindo, beneficio_excluindo)

   
    #  Passo 3: Reconstrução — quais atividades formam a solução

    selecionadas = []
    i = n - 1

    while i >= 0:
        j = _ultimo_compativel(ordenadas, i)
        beneficio_incluindo = peso(ordenadas[i]) + (dp[j] if j >= 0 else 0)

        if i == 0 or beneficio_incluindo >= dp[i - 1]:
            # A atividade i faz parte da solução ótima
            selecionadas.append(ordenadas[i])
            i = j  # pula para o último compatível
        else:
            i -= 1  # a atividade i não está na solução, volta um passo

    # Reverte para ordem cronológica
    selecionadas.reverse()
    return selecionadas


def exibir_resultado_dinamico(selecionadas: list[Atividade], usar_participantes: bool = False) -> None:
    """
    Exibe no terminal o resultado da Programação Dinâmica de forma formatada.

    Parâmetros:
        selecionadas       (list[Atividade]): Atividades selecionadas pelo algoritmo.
        usar_participantes (bool)           : Indica qual peso foi utilizado.
    """
    criterio = "participantes" if usar_participantes else "prioridade"

    print("\n" + "=" * 60)
    print(f"  RESULTADO — PROGRAMAÇÃO DINÂMICA (peso: {criterio})")
    print("=" * 60)

    if not selecionadas:
        print("  Nenhuma atividade foi selecionada.")
        print("=" * 60)
        return

    print(f"  Total de atividades selecionadas: {len(selecionadas)}\n")

    for i, atividade in enumerate(selecionadas, start=1): print(f"  {i:02}. {atividade}")

    prioridade_total    = sum(a.prioridade     for a in selecionadas)
    participantes_total = sum(a.participantes  for a in selecionadas)
    beneficio_total     = sum(
        a.participantes if usar_participantes else a.prioridade
        for a in selecionadas
    )
    print("\n" + "-" * 60)
    print(f"  Benefício total ({criterio:13}): {beneficio_total}")
    print(f"  Prioridade acumulada           : {prioridade_total}")
    print(f"  Participantes totais           : {participantes_total}")
    print("=" * 60)