import pytest
from datetime import datetime, timedelta
from locadora import Carro, Cliente, CarroIndisponivelError, LimiteLocacaoExcedidoError, CarroNaoAlugadoError

class TestLocadora:
    
    def test_carro_alugar_devolver(self):
        """Testa o processo básico de alugar e devolver um carro."""
        carro = Carro("Fusca", "XYZ-0011", 100.0)
        assert carro.disponivel == True
        
        carro.alugar()
        assert carro.disponivel == False
        assert carro.data_locacao is not None
        
        valor_total, multa = carro.devolver(dias_alugado_previsto=5)
        assert carro.disponivel == True
        assert carro.data_locacao is None
        assert valor_total >= 0
        assert multa == 0.0

    def test_alugar_carro_indisponivel(self):
        """Testa a tentativa de alugar um carro que já está alugado."""
        carro = Carro("Corsa", "BCA-1122", 120.0)
        carro.alugar()
        
        with pytest.raises(CarroIndisponivelError):
            carro.alugar()
            
    def test_cliente_excede_limite_de_locacao(self):
        """Testa se o cliente é impedido de alugar mais carros que o permitido."""
        cliente = Cliente("Carlos", 202)
        carro1 = Carro("Gol", "CDE-3344", 130.0)
        carro2 = Carro("Palio", "EFG-5566", 140.0)
        carro3 = Carro("Uno", "GHI-7788", 110.0)
        
        cliente.alugar_carro(carro1)
        cliente.alugar_carro(carro2)
        
        with pytest.raises(LimiteLocacaoExcedidoError):
            cliente.alugar_carro(carro3)

    def test_devolver_carro_nao_alugado(self):
        """Testa a tentativa de devolver um carro que não foi alugado pelo cliente."""
        cliente = Cliente("Ana", 303)
        carro = Carro("Civic", "IJK-9900", 250.0)
        
        with pytest.raises(CarroNaoAlugadoError):
            cliente.devolver_carro(carro, dias_alugado_previsto=10)

    def test_calculo_pagamento_sem_multa(self):
        """Testa o cálculo do pagamento quando o carro é devolvido no prazo."""
        carro = Carro("HB20", "LMN-1212", 180.0)
        carro.alugar()
        
        # Simula devolução dentro do prazo
        dias_alugados = 5
        carro.data_locacao = datetime.now() - timedelta(days=dias_alugados)
        
        valor_total, multa = carro.calcular_pagamento(dias_alugado_previsto=7)
        
        assert multa == 0.0
        assert valor_total == dias_alugados * carro.valor_diaria

    def test_calculo_pagamento_com_multa(self):
        """Testa o cálculo da multa quando o carro é devolvido com atraso."""
        carro = Carro("Onix", "OPQ-3434", 170.0)
        carro.alugar()
        
        # Simula atraso de 3 dias (previsto 5, ficou 8)
        dias_reais = 8
        dias_previstos = 5
        carro.data_locacao = datetime.now() - timedelta(days=dias_reais)
        
        valor_total, multa = carro.calcular_pagamento(dias_alugado_previsto=dias_previstos)
        
        dias_atraso = dias_reais - dias_previstos
        multa_esperada = dias_atraso * (carro.valor_diaria * 0.10)
        
        assert multa == pytest.approx(multa_esperada)
        assert valor_total == pytest.approx((dias_reais * carro.valor_diaria) + multa_esperada)
