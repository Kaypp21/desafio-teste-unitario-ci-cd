import unittest
from unittest.mock import patch
from tarefas_crud import Tarefa, validar_data, criar_tarefa, deletar_tarefa, obter_id_existente

class TestSistemaTarefasPro(unittest.TestCase):

    # --- TESTES DE LÓGICA PURA ---
    def test_validar_data_formatos(self):
        """Testa múltiplos formatos de data, inclusive bissextos."""
        self.assertTrue(validar_data("2024-02-29")) # Ano bissexto
        self.assertFalse(validar_data("2023-02-29")) # Não bissexto
        self.assertFalse(validar_data("31/12/2026")) # Formato BR (deve falhar se o sistema espera ISO)
        self.assertFalse(validar_data("   "))        # Apenas espaços

    # --- TESTES DE CRIAÇÃO (MOCKING COMPLEXO) ---
    @patch('builtins.input', side_effect=['TCC', 'Finalizar escrita', '2026-06-10'])
    def test_fluxo_criacao_completo(self, mock_input):
        """Verifica se o objeto Tarefa é instanciado com os atributos corretos."""
        tarefas = {}
        proximo_id = 1
        novo_id = criar_tarefa(tarefas, proximo_id)
        
        self.assertIn(1, tarefas)
        self.assertEqual(tarefas[1].titulo, "TCC")
        self.assertEqual(novo_id, 2)

    # --- TESTES DE VALIDAÇÃO DE ID ---
    @patch('builtins.input', return_value='abc') # Usuário digitou letras no ID
    def test_obter_id_invalido_tipo(self, mock_input):
        tarefas = {1: Tarefa(1, "Teste", "Desc", "2026-01-01")}
        resultado = obter_id_existente(tarefas)
        self.assertIsNone(resultado)

    # --- TESTES DE DELEÇÃO E CONFIRMAÇÃO ---
    @patch('builtins.input', side_effect=['1', 'n']) # Seleciona ID 1, mas cancela a exclusão
    def test_deletar_tarefa_cancelamento(self, mock_input):
        tarefas = {1: Tarefa(1, "Não deletar", "Desc", "2026-01-01")}
        deletar_tarefa(tarefas)
        self.assertIn(1, tarefas) # A tarefa ainda deve estar lá

    @patch('builtins.input', side_effect=['1', 's']) # Seleciona ID 1 e confirma
    def test_deletar_tarefa_confirmado(self, mock_input):
        tarefas = {1: Tarefa(1, "Deletar", "Desc", "2026-01-01")}
        deletar_tarefa(tarefas)
        self.assertEqual(len(tarefas), 0)

    # --- TESTE DE FORMATAÇÃO (EXIBIR) ---
    def test_metodo_exibir_conteudo(self):
        t = Tarefa(1, "Título", "Desc", "2026-01-01")
        saida = t.exibir()
        self.assertIn("ID: 1", saida)
        self.assertIn("Título: Título", saida)