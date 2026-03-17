import pytest
from unittest.mock import patch
from tarefas_crud import (
    Tarefa,
    validar_data,
    criar_tarefa,
    listar_tarefas,
    atualizar_tarefa,
    deletar_tarefa,
)


def test_validar_data_valida():
    assert validar_data("2024-01-01") is True


def test_validar_data_invalida():
    assert validar_data("01-01-2024") is False


def test_criar_tarefa_sucesso():
    tarefas = {}

    with patch("builtins.input", side_effect=[
        "Titulo teste",
        "Descricao teste",
        "2024-01-01"
    ]):
        next_id = criar_tarefa(tarefas, 1)

    assert len(tarefas) == 1
    assert tarefas[1].titulo == "Titulo teste"
    assert next_id == 2


def test_listar_tarefas_vazia(capsys):
    listar_tarefas({})
    captured = capsys.readouterr()
    assert "Nenhuma tarefa cadastrada." in captured.out


def test_atualizar_tarefa_sucesso():
    tarefas = {
        1: Tarefa(1, "Old", "Old desc", "2024-01-01")
    }

    with patch("builtins.input", side_effect=[
        "1",        # ID
        "Novo",     # novo título
        "Nova desc",
        "2024-02-01"
    ]):
        atualizar_tarefa(tarefas)

    assert tarefas[1].titulo == "Novo"


def test_atualizar_tarefa_data_invalida(capsys):
    tarefas = {
        1: Tarefa(1, "Old", "Old desc", "2024-01-01")
    }

    with patch("builtins.input", side_effect=[
        "1",
        "Novo",
        "Nova desc",
        "data-invalida"
    ]):
        atualizar_tarefa(tarefas)

    captured = capsys.readouterr()
    assert "Data inválida" in captured.out


def test_deletar_tarefa_confirmado():
    tarefas = {
        1: Tarefa(1, "Teste", "Desc", "2024-01-01")
    }

    with patch("builtins.input", side_effect=[
        "1",  # ID
        "s"   # confirmação
    ]):
        deletar_tarefa(tarefas)

    assert 1 not in tarefas


def test_deletar_tarefa_cancelado():
    tarefas = {
        1: Tarefa(1, "Teste", "Desc", "2024-01-01")
    }

    with patch("builtins.input", side_effect=[
        "1",
        "n"
    ]):
        deletar_tarefa(tarefas)

    assert 1 in tarefas


def test_obter_id_inexistente(capsys):
    tarefas = {1: Tarefa(1, "Teste", "Desc", "2024-01-01")}

    with patch("builtins.input", return_value="999"):
        from main import obter_id_existente
        result = obter_id_existente(tarefas)

    assert result is None