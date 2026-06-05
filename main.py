import os
import sys

from modelos.atividade import Atividade
from gerenciador.gerenciador import Gerenciador
from algoritimos.merge_sort import merge_sort, por_horario_fim, por_horario_inicio, por_prioridade, por_nome
from algoritimos.busca_binaria import buscar_atividade
from algoritimos.guloso import selecionar_guloso, exibir_resultado_guloso
from algoritimos.programacao_dinamica import selecionar_dinamico, exibir_resultado_dinamico
from analise.desempenho import comparar_algoritmos, comparar_ordenacoes, exibir_comparacao, exibir_comparacao_ordenacoes


# ------------------------------------------------------------------ #
#  Configuração                                                        #
# ------------------------------------------------------------------ #

ARQUIVO_DADOS = os.path.join("dados", "atividades.json")


# ------------------------------------------------------------------ #
#  Utilitários de terminal                                             #
# ------------------------------------------------------------------ #

def limpar_tela() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def pausar() -> None:
    input("\n  Pressione Enter para continuar...")


def linha(caractere: str = "=", tamanho: int = 60) -> str:
    return caractere * tamanho


def cabecalho(titulo: str) -> None:
    print("\n" + linha())
    print(f"  {titulo}")
    print(linha())


def entrada_inteira(mensagem: str, minimo: int, maximo: int) -> int:
    """Solicita um inteiro dentro de um intervalo, repetindo até obter valor válido."""
    while True:
        try:
            valor = int(input(mensagem))
            if minimo <= valor <= maximo:
                return valor
            print(f"  Digite um número entre {minimo} e {maximo}.")
        except ValueError:
            print("  Entrada inválida. Digite um número.")


# ------------------------------------------------------------------ #
#  1. Cadastro de atividade                                            #
# ------------------------------------------------------------------ #

def menu_cadastrar(gerenciador: Gerenciador) -> None:
    cabecalho("CADASTRAR ATIVIDADE")

    codigo       = input("  Código        : ").strip()
    nome         = input("  Nome          : ").strip()
    inicio       = input("  Início (HH:MM): ").strip()
    fim          = input("  Fim    (HH:MM): ").strip()
    prioridade   = entrada_inteira("  Prioridade (1–5): ", 1, 5)
    participantes = entrada_inteira("  Participantes   : ", 1, 9999)

    erros = Gerenciador.validar_atividade(codigo, nome, inicio, fim, prioridade, participantes)
    if erros:
        print("\n  Erros encontrados:")
        for erro in erros:
            print(f"    • {erro}")
        pausar()
        return

    try:
        atividade = Atividade(codigo, nome, inicio, fim, prioridade, participantes)
        gerenciador.cadastrar(atividade)
        print(f"\n  ✓ Atividade '{nome}' cadastrada com sucesso!")
    except ValueError as e:
        print(f"\n  Erro: {e}")

    pausar()


# ------------------------------------------------------------------ #
#  2. Listar atividades                                                #
# ------------------------------------------------------------------ #

def menu_listar(gerenciador: Gerenciador) -> None:
    cabecalho("ATIVIDADES CADASTRADAS")

    atividades = gerenciador.listar()
    if not atividades:
        print("  Nenhuma atividade cadastrada.")
        pausar()
        return

    print(f"  Total: {len(atividades)} atividade(s)\n")
    for i, a in enumerate(atividades, 1):
        print(f"  {i:02}. {a}")

    pausar()


# ------------------------------------------------------------------ #
#  3. Remover atividade                                                #
# ------------------------------------------------------------------ #

def menu_remover(gerenciador: Gerenciador) -> None:
    cabecalho("REMOVER ATIVIDADE")

    codigo = input("  Código da atividade a remover: ").strip()
    try:
        gerenciador.remover(codigo)
        print(f"\n  ✓ Atividade '{codigo}' removida com sucesso!")
    except ValueError as e:
        print(f"\n  Erro: {e}")

    pausar()


# ------------------------------------------------------------------ #
#  4. Ordenar atividades                                               #
# ------------------------------------------------------------------ #

def menu_ordenar(gerenciador: Gerenciador) -> None:
    cabecalho("ORDENAR ATIVIDADES")

    atividades = gerenciador.listar()
    if not atividades:
        print("  Nenhuma atividade cadastrada.")
        pausar()
        return

    print("  Critérios disponíveis:")
    print("    1. Horário de início")
    print("    2. Horário de fim")
    print("    3. Prioridade (maior primeiro)")
    print("    4. Nome (ordem alfabética)")

    opcao = entrada_inteira("\n  Escolha: ", 1, 4)

    criterios = {
        1: ("Horário de início",          por_horario_inicio),
        2: ("Horário de fim",             por_horario_fim),
        3: ("Prioridade (maior primeiro)",por_prioridade),
        4: ("Nome (alfabética)",          por_nome),
    }

    nome_criterio, chave = criterios[opcao]
    ordenadas = merge_sort(atividades, chave=chave)

    print(f"\n  Ordenado por: {nome_criterio}\n")
    for i, a in enumerate(ordenadas, 1):
        print(f"  {i:02}. {a}")

    pausar()


# ------------------------------------------------------------------ #
#  5. Buscar atividade                                                 #
# ------------------------------------------------------------------ #

def menu_buscar(gerenciador: Gerenciador) -> None:
    cabecalho("BUSCAR ATIVIDADE")

    atividades = gerenciador.listar()
    if not atividades:
        print("  Nenhuma atividade cadastrada.")
        pausar()
        return

    termo = input("  Digite o código ou nome da atividade: ").strip()
    if not termo:
        print("  Termo de busca não pode ser vazio.")
        pausar()
        return

    resultados = buscar_atividade(atividades, termo)

    if not resultados:
        print(f"\n  Nenhuma atividade encontrada para '{termo}'.")
    else:
        print(f"\n  {len(resultados)} resultado(s) encontrado(s):\n")
        for a in resultados:
            print(f"  → {a}")

    pausar()


# ------------------------------------------------------------------ #
#  6. Selecionar atividades                                            #
# ------------------------------------------------------------------ #

def menu_selecionar(gerenciador: Gerenciador) -> None:
    cabecalho("SELECIONAR ATIVIDADES SEM CONFLITO")

    atividades = gerenciador.listar()
    if not atividades:
        print("  Nenhuma atividade cadastrada.")
        pausar()
        return

    print("  Algoritmos disponíveis:")
    print("    1. Algoritmo Guloso (maximiza quantidade)")
    print("    2. Programação Dinâmica — peso: prioridade")
    print("    3. Programação Dinâmica — peso: participantes")

    opcao = entrada_inteira("\n  Escolha: ", 1, 3)

    if opcao == 1:
        selecionadas = selecionar_guloso(atividades)
        exibir_resultado_guloso(selecionadas)
    elif opcao == 2:
        selecionadas = selecionar_dinamico(atividades, usar_participantes=False)
        exibir_resultado_dinamico(selecionadas, usar_participantes=False)
    else:
        selecionadas = selecionar_dinamico(atividades, usar_participantes=True)
        exibir_resultado_dinamico(selecionadas, usar_participantes=True)

    pausar()


# ------------------------------------------------------------------ #
#  7. Comparar algoritmos                                              #
# ------------------------------------------------------------------ #

def menu_comparar(gerenciador: Gerenciador) -> None:
    cabecalho("COMPARAR ALGORITMOS")

    atividades = gerenciador.listar()
    if not atividades:
        print("  Nenhuma atividade cadastrada.")
        pausar()
        return

    print("  Critério de peso para a Programação Dinâmica:")
    print("    1. Prioridade")
    print("    2. Participantes")

    opcao = entrada_inteira("\n  Escolha: ", 1, 2)
    usar_participantes = (opcao == 2)

    metricas = comparar_algoritmos(atividades, usar_participantes)
    exibir_comparacao(metricas)

    print("\n  Deseja ver também o desempenho do Merge Sort por critério? (s/n)")
    if input("  ").strip().lower() == "s":
        metricas_ord = comparar_ordenacoes(atividades)
        exibir_comparacao_ordenacoes(metricas_ord, len(atividades))

    pausar()


# ------------------------------------------------------------------ #
#  8. Carregar conjunto de teste                                       #
# ------------------------------------------------------------------ #

def menu_carregar_teste(gerenciador: Gerenciador) -> None:
    cabecalho("CARREGAR CONJUNTO DE TESTE")

    print("  Conjuntos disponíveis:")
    print("    1. Pequeno  ( 8 atividades)")
    print("    2. Médio    (15 atividades)")
    print("    3. Grande   (32 atividades)")

    opcao = entrada_inteira("\n  Escolha: ", 1, 3)

    arquivos = {
        1: os.path.join("dados", "teste_pequeno.json"),
        2: os.path.join("dados", "teste_medio.json"),
        3: os.path.join("dados", "teste_grande.json"),
    }

    caminho = arquivos[opcao]

    if not os.path.exists(caminho):
        print(f"\n  Arquivo '{caminho}' não encontrado.")
        print("  Execute primeiro: python testes/gerar_testes.py")
        pausar()
        return

    # Substitui o gerenciador pelo conjunto de teste (apenas em memória)
    novo_gerenciador = Gerenciador(caminho)
    gerenciador.atividades = novo_gerenciador.atividades
    gerenciador.caminho_arquivo = caminho

    print(f"\n  ✓ {len(gerenciador.atividades)} atividades carregadas de '{caminho}'.")
    pausar()


# ------------------------------------------------------------------ #
#  Menu principal                                                      #
# ------------------------------------------------------------------ #

def menu_principal(gerenciador: Gerenciador) -> None:
    opcoes = {
        "1": ("Cadastrar atividade",           menu_cadastrar),
        "2": ("Listar atividades",             menu_listar),
        "3": ("Remover atividade",             menu_remover),
        "4": ("Ordenar atividades",            menu_ordenar),
        "5": ("Buscar atividade",              menu_buscar),
        "6": ("Selecionar sem conflito",       menu_selecionar),
        "7": ("Comparar algoritmos",           menu_comparar),
        "8": ("Carregar conjunto de teste",    menu_carregar_teste),
        "0": ("Sair",                          None),
    }

    while True:
        limpar_tela()
        print("\n" + linha())
        print("  SISTEMA DE AGENDAMENTO DE ATIVIDADES")
        print(linha())
        print(f"  Atividades carregadas: {len(gerenciador.listar())}")
        print(linha("-"))

        for chave, (descricao, _) in opcoes.items():
            print(f"  {chave}. {descricao}")

        print(linha())
        escolha = input("  Opção: ").strip()

        if escolha == "0":
            print("\n  Encerrando o sistema. Até logo!\n")
            sys.exit(0)

        if escolha in opcoes:
            _, funcao = opcoes[escolha]
            funcao(gerenciador)
        else:
            print("  Opção inválida.")
            pausar()


# ------------------------------------------------------------------ #
#  Ponto de entrada                                                    #
# ------------------------------------------------------------------ #

if __name__ == "__main__":
    gerenciador = Gerenciador(ARQUIVO_DADOS)
    menu_principal(gerenciador)