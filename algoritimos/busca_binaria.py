from modelos.atividade import Atividade
from algoritimos.merge_sort import merge_sort, por_nome


def busca_binaria_por_nome(atividades: list[Atividade], nome_busca: str) -> Atividade | None:
    """
    Busca uma atividade pelo nome exato usando Busca Binária.
    A lista deve estar ordenada por nome (use merge_sort com por_nome).

    Parâmetros:
        atividades  (list[Atividade]): Lista ordenada por nome.
        nome_busca  (str)            : Nome a ser localizado.

    Retorna:
        Atividade encontrada ou None se não existir.

    Complexidade:
        Tempo : O(log n)
        Espaço: O(1)
    """
    nome_alvo = nome_busca.strip().lower() # Normalização do texto
    esquerda  = 0 # Inicialização dos ponteiros
    direita   = len(atividades) - 1

    while esquerda <= direita:
        meio = (esquerda + direita) // 2
        nome_atual = atividades[meio].nome.lower() # Pega o nome da atividade que está no meio.

        if nome_atual == nome_alvo:
            return atividades[meio]
        elif nome_atual < nome_alvo:
            esquerda = meio + 1
        else:
            direita = meio - 1

    return None


def busca_binaria_por_codigo(atividades: list[Atividade], codigo_busca: str) -> Atividade | None:
    """
    Busca uma atividade pelo código usando Busca Binária.
    A lista deve estar ordenada por código (ordem lexicográfica).

    Parâmetros:
        atividades    (list[Atividade]): Lista ordenada por código.
        codigo_busca  (str)            : Código a ser localizado.

    Retorna:
        Atividade encontrada ou None se não existir.

    Complexidade:
        Tempo : O(log n)
        Espaço: O(1)
    """
    codigo_alvo = codigo_busca.strip().lower()
    esquerda    = 0
    direita     = len(atividades) - 1

    while esquerda <= direita:
        meio = (esquerda + direita) // 2
        codigo_atual = atividades[meio].codigo.lower()

        if codigo_atual == codigo_alvo:
            return atividades[meio]
        elif codigo_atual < codigo_alvo:
            esquerda = meio + 1
        else:
            direita = meio - 1

    return None


def busca_por_nome_parcial(atividades: list[Atividade], trecho: str) -> list[Atividade]: # não usa busca binária.
    """
    Busca atividades cujo nome contenha o trecho informado.
    Não exige lista ordenada — percorre todos os elementos.

    Útil para buscas do tipo "pesquisar enquanto digita".

    Parâmetros:
        atividades (list[Atividade]): Lista de atividades.
        trecho     (str)            : Trecho a ser localizado no nome.

    Retorna:
        Lista com todas as atividades que contêm o trecho (pode ser vazia).

    Complexidade:
        Tempo : O(n)
        Espaço: O(k) onde k é o número de resultados encontrados
    """
    trecho_alvo = trecho.strip().lower()
    return [a for a in atividades if trecho_alvo in a.nome.lower()]


#  Função principal de busca (usada pelo menu)

def buscar_atividade(atividades: list[Atividade], termo: str) -> list[Atividade]:
    """
    Busca inteligente: tenta busca binária por código ou nome exato.
    Se não encontrar, faz busca parcial por nome.

    Fluxo:
        1. Ordena a lista por nome
        2. Tenta busca binária por nome exato  → O(log n)
        3. Tenta busca binária por código      → O(log n)
        4. Se ainda não achou, busca parcial   → O(n)

    Parâmetros:
        atividades (list[Atividade]): Lista de atividades cadastradas.
        termo      (str)            : Código ou nome (parcial ou exato).

    Retorna:
        Lista com os resultados encontrados (pode ter 1 ou mais itens).
    """
    if not atividades:
        return []

    # Tenta busca binária por nome exato
    ordenadas_nome = merge_sort(atividades, chave=por_nome)
    resultado = busca_binaria_por_nome(ordenadas_nome, termo)
    if resultado:
        return [resultado]

    # Tenta busca binária por código
    ordenadas_codigo = merge_sort(atividades, chave=lambda a: a.codigo.lower())
    resultado = busca_binaria_por_codigo(ordenadas_codigo, termo)
    if resultado:
        return [resultado]

    # Fallback: busca parcial por nome
    return busca_por_nome_parcial(atividades, termo)

