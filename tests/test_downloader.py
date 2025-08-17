import pytest
from unittest.mock import MagicMock
import downloader

@pytest.fixture
def mock_common(mocker):
    """A pytest fixture to set up common mocks for all tests."""
    mock_print = mocker.patch('builtins.print')
    mock_config = MagicMock()
    mock_config['Settings'] = {
        'download_folder': 'test_downloads',
        'audio_quality': '192',
        'audio_format': 'mp3'
    }
    mocker.patch('downloader.get_config', return_value=mock_config)

    mock_path_instance = MagicMock()
    mock_path_instance.__str__.return_value = 'test_downloads'
    mock_path_instance.parent = mock_path_instance
    mock_path_instance.__truediv__.return_value = mock_path_instance
    mocker.patch('downloader.Path', return_value=mock_path_instance)

    mock_descargar = mocker.patch('downloader.descargar_mp3')

    return mock_print, mock_config, mock_descargar

def test_download_single_song(mocker, mock_common):
    """
    Test that choosing option '2' calls the download function correctly.
    """
    mock_print, mock_config, mock_descargar = mock_common
    mocker.patch('builtins.input', side_effect=['some_url', '2'])

    downloader.main()

    mock_descargar.assert_called_once_with('some_url', config=mock_config, descargar_playlist=False)
    mock_print.assert_any_call("✅ Descarga completa. Revisa test_downloads")

def test_download_playlist(mocker, mock_common):
    """
    Test that choosing option '1' calls the download function correctly for a playlist.
    """
    mock_print, mock_config, mock_descargar = mock_common
    mocker.patch('builtins.input', side_effect=['some_url', '1'])

    downloader.main()

    mock_descargar.assert_called_once_with('some_url', config=mock_config, descargar_playlist=True)
    mock_print.assert_any_call("✅ Descarga completa. Revisa test_downloads")

def test_invalid_option(mocker):
    """
    Test that choosing an invalid option exits gracefully.
    """
    mocker.patch('builtins.input', side_effect=['some_url', '99'])
    mock_print = mocker.patch('builtins.print')
    mock_exit = mocker.patch('builtins.exit')
    mocker.patch('downloader.get_config') # Mock this so it doesn't run fully

    downloader.main()

    mock_exit.assert_called_once()
    mock_print.assert_any_call("\nOpción inválida. Saliendo...")
