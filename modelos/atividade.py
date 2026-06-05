class Atividade:
    """
    Representa uma atividade do sistema de agendamento.
    Atributos:
        codigo      (str) : Identificador único da atividade
        nome        (str) : Nome/descrição da atividade
        inicio      (str) : Horário de início no formato "HH:MM"
        fim         (str) : Horário de fim no formato "HH:MM"
        prioridade  (int) : Peso da atividade de 1 (baixa) a 5 (alta)
        participantes(int): Quantidade de participantes
    """
    def __init__(self, codigo: str, nome: str, inicio: str, fim: str, # obs: O self representa o próprio objeto (instância) que está usando o método
                 prioridade: int, participantes: int):
        self.codigo = codigo
        self.nome = nome
        self.inicio = inicio
        self.fim = fim
        self.prioridade = prioridade
        self.participantes = participantes

    #  Conversão de horário

    def inicio_em_minutos(self) -> int: # esta funcão converte horas e minutos para a mesma unidade que e = minutos
        """Converte o horário de início para minutos totais"""
        horas, minutos = map(int, self.inicio.split(":"))
        return horas * 60 + minutos

    def fim_em_minutos(self) -> int:
        """Converte o horário de fim para minutos totais"""
        horas, minutos = map(int, self.fim.split(":"))
        return horas * 60 + minutos
    
    #  Verificação de conflito

    def conflita_com(self, outra: "Atividade") -> bool: # função cental do nosso sistema, pois duas atividades conflitam quando:
        """
        meu_inicio < fim_dela  E  inicio_dela < meu_fim
        
        Verifica se esta atividade tem sobreposição de horário com outra.
        Duas atividades conflitam quando uma começa antes da outra terminar.
        """
        return self.inicio_em_minutos() < outra.fim_em_minutos() and \
               outra.inicio_em_minutos() < self.fim_em_minutos()

    #  Serialização

    def para_dict(self) -> dict: # converte objeto → dicionário para salvar.
        """Converte a atividade para dicionário (usado ao salvar em JSON)."""
        # Esta função retorna um objeto do tipo dicionário
        return {
            "codigo": self.codigo,
            "nome": self.nome,
            "inicio": self.inicio,
            "fim": self.fim,
            "prioridade": self.prioridade,
            "participantes": self.participantes
        }

    @staticmethod
    def de_dict(dados: dict) -> "Atividade": #  faz o caminho inverso ao carregar
        """Cria uma Atividade a partir de um dicionário (usado ao ler o JSON)."""
        return Atividade(
            codigo=dados["codigo"],
            nome=dados["nome"],
            inicio=dados["inicio"],
            fim=dados["fim"],
            prioridade=dados["prioridade"],
            participantes=dados["participantes"]
        )

   
    #  Representação no formato string

    def __str__(self) -> str:
        return (f"[{self.codigo}] {self.nome} | "
                f"{self.inicio}–{self.fim} | "
                f"Prioridade: {self.prioridade} | "
                f"Participantes: {self.participantes}")

    def __repr__(self) -> str:
        return f"Atividade(codigo={self.codigo!r}, nome={self.nome!r})"