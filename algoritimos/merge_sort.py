from modelos.atividade import Atividade


def merge_sort(atividades: list[Atividade], chave) -> list[Atividade]:
    """
    Ordena uma lista de atividades usando o algoritmo Merge Sort.
    A Chave e o parametro que em vez de criar um Merge Sort diferente pra cada critério, passamos o que queremos comparar como argumento

    Parâmetros:
        atividades (list[Atividade]): Lista a ser ordenada.
        chave (callable)            : Função que extrai o valor de comparação.
                                      Exemplos:
                                        lambda a: a.fim_em_minutos()
                                        lambda a: a.inicio_em_minutos()
                                        lambda a: a.prioridade
                                        lambda a: a.nome.lower()

    Retorna:
        list[Atividade]: Nova lista ordenada (a original não é modificada).

    Complexidade:
        Tempo : O(n log n) — sempre, independente da entrada
        Espaço: O(n)       — cria sublistas auxiliares na recursão
    """
    # Caso base: lista com 0 ou 1 elemento já está ordenada
    if len(atividades) <= 1: # Se a lista tem 0 ou 1 elemento, ela já está ordenada.
        return list(atividades) # Merge Sort funciona dividindo a lista em partes menores até sobrar pedaços de tamanho 1

    # Divide ao meio
    meio = len(atividades) // 2
    esquerda = merge_sort(atividades[:meio], chave) # Divide em esquerda e direita
    direita  = merge_sort(atividades[meio:], chave) # Depois, cada metade é ordenada chamando merge_sort de novo.

    return _merge(esquerda, direita, chave)  # Junta as partes ordenadas
    '''
    Depois que as duas metades já estão ordenadas, a função chama _merge() para juntar tudo em uma lista final ordenada.
    '''


def _merge(esquerda: list[Atividade], direita: list[Atividade], chave) -> list[Atividade]:
    """
    Devolve uma nova lista, unindo as duas em ordem correta.
    Método privado — usado internamente pelo merge_sort.

    Complexidade: O(n) onde n = len(esquerda) + len(direita)
    """
    resultado = [] # Lista de resultado
    i = j = 0 # i para percorrer a lista da esquerda # j para percorrer a lista da direita

    # Compara elemento a elemento e insere o menor
    while i < len(esquerda) and j < len(direita): # Enquanto ainda houver elementos nas duas listas, continue comparando
        if chave(esquerda[i]) <= chave(direita[j]): # A função chave é aplicada aos elementos para decidir qual vem primeiro
            resultado.append(esquerda[i]) # Se o elemento da esquerda for o menor, ele é colocado na lista final e o índice i avança
            i += 1
        else:
            resultado.append(direita[j]) # Se o da direita for menor, ele entra na lista final e o índice j avança.
            j += 1

    # Adiciona os elementos restantes (apenas um dos dois terá sobra)
    resultado.extend(esquerda[i:])
    resultado.extend(direita[j:])

    return resultado # Retorna a lista final

#  Critérios prontos para uso. Essas funções servem para dizer como ordenar.

def por_horario_fim(atividade: Atividade) -> int: # Essa função pega uma atividade e retorna o horário de fim convertido para minutos
    """Critério usado pelo Algoritmo Guloso — ordena por horário de fim."""
    return atividade.fim_em_minutos()


def por_horario_inicio(atividade: Atividade) -> int:
    """Critério para exibir atividades em ordem cronológica."""
    return atividade.inicio_em_minutos()


def por_prioridade(atividade: Atividade) -> int:
    """Critério para ordenar do maior para o menor benefício.
    O sinal negativo inverte a ordem (maior prioridade primeiro)."""
    return -atividade.prioridade # Então usar o sinal negativo faz o sort colocar primeiro os maiores valores.


def por_nome(atividade: Atividade) -> str:
    """Critério lexicográfico — ignora maiúsculas/minúsculas."""
    return atividade.nome.lower() # comparar sem diferenciar maiúsculas e minúsculas.