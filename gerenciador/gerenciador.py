import json # importei o módulo json da biblioteca do python
import os # Operating System, permite interagir com o sistema operacional

from modelos.atividade import Atividade # Do arquivo atividade.py, que está dentro da pasta modelos, importe a classe Atividade


class Gerenciador:
    """
    Responsável por gerenciar as atividades do sistema.

    Responsabilidades:
        - Cadastrar, remover e listar atividades
        - Carregar e salvar atividades em arquivo JSON
    """

    def __init__(self, caminho_arquivo: str): # construtor da classe 
        """
        Parâmetros:
            caminho_arquivo (str): Caminho para o arquivo JSON de dados.
        """
        self.caminho_arquivo = caminho_arquivo # criar um atributo do objeto
        self.atividades: list[Atividade] = [] # Criando uma lista vazia
        self._carregar() # chamo o método de carregar 
  
    #  Persistência

    def _carregar(self) -> None:
        """
        Carrega as atividades do arquivo JSON.
        Se o arquivo não existir, inicia com lista vazia.
        Método privado — chamado automaticamente no __init__.
        """
        if not os.path.exists(self.caminho_arquivo):
            self.atividades = []
            return

        with open(self.caminho_arquivo, "r", encoding="utf-8") as arq: # importante:('r' leitura (read)). O with garante que o arquivo será fechado automaticamente quando o bloco terminar
            dados = json.load(arq)
            self.atividades = [Atividade.de_dict(item) for item in dados]
            '''
            Leia o conteúdo JSON que está dentro do arquivo arq e 
            converta-o para estruturas Python (listas, dicionários, etc.), 
            armazenando o resultado na variável dados.
            Para cada dicionário presente em dados, crie um objeto Atividade usando o método de_dict()
            e coloque esse objeto na lista self.atividades.
            '''

    def salvar(self) -> None: # não retorna nenhum valor
        """
        Persiste a lista de atividades no arquivo JSON.
        Chamado após qualquer operação que modifica os dados.
        """
        # Garante que o diretório existe antes de salvar
        os.makedirs(os.path.dirname(self.caminho_arquivo), exist_ok=True) # Crie a pasta "dados" caso ela não exista. Se a pasta já existir, não gere erro.
        # Garanta que a pasta onde o arquivo será salvo exista antes de tentar gravar o JSON.
        with open(self.caminho_arquivo, "w", encoding="utf-8") as arq: # Abra o arquivo indicado em self.caminho_arquivo no modo escrita (w) usando UTF-8 e chame-o de arq
            json.dump([a.para_dict() for a in self.atividades],arq,ensure_ascii=False,indent=4)\
            # Grave dados em formato JSON(Para cada atividade da lista self.atividades, converta o objeto para um dicionário e monte uma lista desses dicionários.
            # Permita salvar caracteres especiais normalmente. E por fim, Organize o JSON com recuo de 4 espaços)

    #  Cadastro Esses dois métodos implementam as operações de cadastro e remoção de atividades

    def cadastrar(self, atividade: Atividade) -> None: # O parâmetro atividade deve ser um objeto da classe Atividade
        """
        Adiciona uma nova atividade ao sistema.

        Lança ValueError se já existir uma atividade com o mesmo código.
        """
        if self._buscar_por_codigo(atividade.codigo) is not None: # Procure uma atividade que tenha o mesmo código da atividade recebida.
            raise ValueError(f"Já existe uma atividade com o código '{atividade.codigo}'.")

        self.atividades.append(atividade) # Adicione a atividade ao final da lista.
        self.salvar() # Grave a nova lista no arquivo JSON.

    def remover(self, codigo: str) -> None: # Recebe um código e remove a atividade correspondente.
        """
        Remove a atividade com o código informado.

        Lança ValueError se o código não for encontrado.
        """
        atividade = self._buscar_por_codigo(codigo) # Procure a atividade que possui o código informado.
        if atividade is None:
            raise ValueError(f"Atividade com código '{codigo}' não encontrada.")

        self.atividades.remove(atividade) # Remova o objeto encontrado da lista.
        self.salvar() # Atualize o arquivo JSON com a nova lista.

    #  Consultas

    def listar(self) -> list[Atividade]: # Retorna uma lista de objetos Atividade
        """Retorna uma cópia da lista de atividades cadastradas."""
        return list(self.atividades) # Uma lista contendo objetos da classe Atividade

    def _buscar_por_codigo(self, codigo: str) -> Atividade | None: # Recebe um código em formato textoRecebe um código em formato texto
        # Pode retornar um objeto Atividade OU None
        """
        Busca linear por código — uso interno.
        Retorna a atividade encontrada ou None.
        Complexidade: O(n)
        """
        for atividade in self.atividades: # Percorra todas as atividades da lista
            if atividade.codigo == codigo: # Se o código da atividade atual for igual ao código procurado
                return atividade
        return None


    #  Validação de entrada

    @staticmethod # Significa que o método pertence à classe, mas não precisa de self
    def validar_horario(horario: str) -> bool:
        """
        Verifica se o horário está no formato HH:MM e se os valores são válidos.
        Exemplo válido: "08:30". Inválidos: "8:30", "25:00", "08:60".
        """
        partes = horario.split(":") # Separando horas e minutos
        if len(partes) != 2: # Recebe um horário em texto e retorna: True se for válido; False se for inválido
            return False
        # O método split(":") divide a string onde encontrar :.

        horas_str, minutos_str = partes
        if len(horas_str) != 2 or len(minutos_str) != 2: # Verificando tamanho
            return False
        if not horas_str.isdigit() or not minutos_str.isdigit(): # Verificando se são números
            return False

        horas, minutos = int(horas_str), int(minutos_str) # Convertendo para inteiro
        return 0 <= horas <= 23 and 0 <= minutos <= 59 # Verificando limites

    @staticmethod
    def validar_atividade(codigo: str, nome: str, inicio: str, fim: str,
                          prioridade: int, participantes: int) -> list[str]:
        """
        Valida os campos de uma atividade antes de cadastrar.
        Retorna uma lista de erros encontrados (vazia se tudo estiver correto).
        """
        erros = [] # Lista de erros Começa vazia.
        '''
        Verificar código
        Verificar nome
        Verificar horário inicial
        Verificar horário final
        Verificar se fim > início
        Verificar prioridade entre 1 e 5
        Verificar participantes > 0
        Retornar lista de erros
        '''
        if not codigo.strip():
            erros.append("Código não pode ser vazio.")
        if not nome.strip():
            erros.append("Nome não pode ser vazio.")
        if not Gerenciador.validar_horario(inicio):
            erros.append("Horário de início inválido. Use o formato HH:MM (ex: 08:30).")
        if not Gerenciador.validar_horario(fim):
            erros.append("Horário de fim inválido. Use o formato HH:MM (ex: 09:00).")
        if Gerenciador.validar_horario(inicio) and Gerenciador.validar_horario(fim):
            h_inicio = int(inicio[:2]) * 60 + int(inicio[3:])
            h_fim    = int(fim[:2])    * 60 + int(fim[3:])
            if h_fim <= h_inicio:
                erros.append("Horário de fim deve ser posterior ao horário de início.")
        if not (1 <= prioridade <= 5):
            erros.append("Prioridade deve ser um número entre 1 e 5.")
        if participantes <= 0:
            erros.append("Quantidade de participantes deve ser maior que zero.")

        return erros