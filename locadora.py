from datetime import datetime, timedelta
from typing import List

# --- Constantes ---
LIMITE_CARROS_POR_CLIENTE = 2
TAXA_MULTA_DIARIA = 0.10  # 10% do valor da diária por dia de atraso


# --- Exceções Personalizadas ---
class LocadoraError(Exception):
    """Classe base para exceções da locadora."""
    pass
# ... (o resto das exceções permanece o mesmo) ...
class LimiteLocacaoExcedidoError(LocadoraError):
    """Exceção para quando o cliente excede o limite de carros alugados."""
    pass

class CarroIndisponivelError(LocadoraError):
    """Exceção para quando o carro não está disponível para aluguel."""
    pass

class CarroNaoAlugadoError(LocadoraError):
    """Exceção para quando se tenta devolver um carro não alugado pelo cliente."""
    pass


# --- Classes de Domínio ---
class Carro:
    """Representa um carro na locadora."""
    def __init__(self, modelo: str, placa: str, valor_diaria: float):
        self.modelo = modelo
        self.placa = placa
        self.valor_diaria = valor_diaria
        self.disponivel = True
        self.data_locacao = None
    
    def alugar(self):
        """Marca o carro como alugado e registra a data."""
        if not self.disponivel:
            raise CarroIndisponivelError(f"O carro modelo '{self.modelo}' (placa: {self.placa}) não está disponível.")
        self.disponivel = False
        self.data_locacao = datetime.now()
    
    def devolver(self):
        """Marca o carro como disponível, limpando a data de locação."""
        if self.disponivel:
            raise LocadoraError(f"O carro '{self.modelo}' já está disponível para locação.")
        self.disponivel = True
        self.data_locacao = None

    def calcular_pagamento(self, dias_previstos: int) -> tuple[float, float]:
        """Calcula o valor do aluguel e a multa por atraso, se houver."""
        if not self.data_locacao:
            return 0.0, 0.0

        dias_reais = (datetime.now() - self.data_locacao).days
        multa = 0.0
        
        if dias_reais > dias_previstos:
            dias_atraso = dias_reais - dias_previstos
            multa = dias_atraso * (self.valor_diaria * TAXA_MULTA_DIARIA)

        valor_aluguel = dias_reais * self.valor_diaria
        return valor_aluguel + multa, multa
    
    def __str__(self):
        status = "Disponível" if self.disponivel else "Alugado"
        return f"'{self.modelo}' (Placa: {self.placa}) - Diária: R${self.valor_diaria:.2f} [{status}]"


class Cliente:
    """Representa um cliente da locadora."""
    def __init__(self, nome: str, id_cliente: int):
        self.nome = nome
        self.id = id_cliente
        self.carros_alugados: List[Carro] = []
    
    def pode_alugar(self) -> bool:
        """Verifica se o cliente pode alugar mais carros."""
        return len(self.carros_alugados) < LIMITE_CARROS_POR_CLIENTE

    def alugar_carro(self, carro: Carro):
        """Adiciona um carro à lista de carros alugados pelo cliente."""
        if not self.pode_alugar():
            raise LimiteLocacaoExcedidoError(
                f"Cliente {self.nome} excedeu o limite de {LIMITE_CARROS_POR_CLIENTE} carros alugados."
            )
        carro.alugar()
        self.carros_alugados.append(carro)
    
    def devolver_carro(self, carro: Carro):
        """Remove um carro da lista de alugados do cliente."""
        if carro not in self.carros_alugados:
            raise CarroNaoAlugadoError(f"O carro '{carro.modelo}' não foi alugado por este cliente.")
        carro.devolver()
        self.carros_alugados.remove(carro)

    def __str__(self):
        return f"Cliente: {self.nome} (ID: {self.id}) - Carros alugados: {len(self.carros_alugados)}"


# --- Classe de Serviço / Gerenciamento ---
class Locadora:
    """Gerencia as operações da locadora de carros."""
    def __init__(self, carros: List[Carro], clientes: List[Cliente]):
        self.carros = carros
        self.clientes = clientes

    def alugar(self, cliente: Cliente, carro: Carro):
        """Processa o aluguel de um carro para um cliente."""
        cliente.alugar_carro(carro)
        print(f"Carro '{carro.modelo}' alugado com sucesso para {cliente.nome}.")

    def devolver(self, cliente: Cliente, carro: Carro, dias_previstos: int):
        """Processa a devolução de um carro e exibe o valor a pagar."""
        valor_total, multa = carro.calcular_pagamento(dias_previstos)
        cliente.devolver_carro(carro)
        
        mensagem = f"Carro '{carro.modelo}' devolvido. Valor total: R$ {valor_total:.2f}."
        if multa > 0:
            mensagem += f" (Incluindo R$ {multa:.2f} de multa por atraso)."
        print(mensagem)

    def exibir_status(self):
        """Exibe o status atual dos carros e clientes."""
        print("\n--- Status da Frota ---")
        for carro in self.carros:
            print(carro)
        print("\n--- Status dos Clientes ---")
        for cliente in self.clientes:
            print(cliente)
        print("-" * 25)


# --- Exemplo de Uso ---
if __name__ == "__main__":
    # 1. Configuração inicial
    carros_disponiveis = [
        Carro("Fiat Mobi", "ABC-1234", 150.00),
        Carro("Hyundai HB20", "DEF-5678", 180.00),
        Carro("Chevrolet Onix", "GHI-9012", 170.00),
    ]
    clientes_cadastrados = [Cliente("Maria Souza", 101)]
    
    locadora = Locadora(carros=carros_disponiveis, clientes=clientes_cadastrados)
    
    print("--- Bem-vindo à Locadora de Carros ---")
    locadora.exibir_status()

    # 2. Operações de Aluguel
    cliente_maria = clientes_cadastrados[0]
    carro_mobi = carros_disponiveis[0]
    carro_hb20 = carros_disponiveis[1]
    carro_onix = carros_disponiveis[2]

    try:
        print("\n>>> Realizando aluguéis...")
        locadora.alugar(cliente_maria, carro_mobi)
        locadora.alugar(cliente_maria, carro_hb20)
        
        print("\n>>> Tentando alugar terceiro carro (deve falhar)...")
        locadora.alugar(cliente_maria, carro_onix)
        
    except (CarroIndisponivelError, LimiteLocacaoExcedidoError) as e:
        print(f"Erro: {e}")

    locadora.exibir_status()

    # 3. Operações de Devolução
    try:
        print("\n>>> Realizando devoluções...")
        # Simular devolução com 1 dia de atraso (previsto 5 dias, ficou 6)
        carro_mobi.data_locacao = datetime.now() - timedelta(days=6)
        locadora.devolver(cliente_maria, carro_mobi, dias_previstos=5)

        # Devolução no prazo
        locadora.devolver(cliente_maria, carro_hb20, dias_previstos=7)
    except LocadoraError as e:
        print(f"Erro na devolução: {e}")

    print("\n--- Status Final ---")
    locadora.exibir_status()