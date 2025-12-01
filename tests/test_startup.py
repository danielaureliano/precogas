import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app

@patch("app.main.settings") # Mocka settings
def test_startup_check_success(mock_settings):
    # Configura o Mock do OUTPUT_DIR
    mock_output_dir = mock_settings.OUTPUT_DIR

    # Simula diretório inexistente, mas cria com sucesso
    mock_output_dir.exists.return_value = False

    # Mock para mkdir e operações de arquivo de teste
    mock_file = MagicMock()
    mock_output_dir.__truediv__.return_value = mock_file

    with TestClient(app):
        # O lifespan roda ao entrar no context manager
        mock_output_dir.mkdir.assert_called_with(parents=True, exist_ok=True)
        mock_file.touch.assert_called()
        mock_file.unlink.assert_called()

@patch("app.main.settings")
def test_startup_check_fail_permission(mock_settings):
    mock_output_dir = mock_settings.OUTPUT_DIR
    mock_output_dir.exists.return_value = True

    # Simula erro ao criar arquivo de teste (sem permissão)
    mock_file = MagicMock()
    mock_output_dir.__truediv__.return_value = mock_file
    mock_file.touch.side_effect = PermissionError("No write permission")

    with pytest.raises(RuntimeError, match="Sem permissão de escrita"):
        with TestClient(app):
            pass
