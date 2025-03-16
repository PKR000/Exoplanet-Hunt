import pytest
from unittest.mock import patch, MagicMock
from src.lightcurve_processor import LightCurveProcessor

@patch('glob.glob')
@patch('os.path.join')
def test_get_fits_files(mock_join, mock_glob):
    # Arrange
    tic_id = "123456789"
    processor = LightCurveProcessor(tic_id)
    mock_join.side_effect = lambda *args: "/".join(args)
    mock_glob.return_value = [
        "/data/TESS_Downloads/TIC_123456789/file1_lc.fits",
        "/data/TESS_Downloads/TIC_123456789/file2_lc.fits"
    ]

    # Act
    fits_files = processor.get_fits_files()

    # Assert
    expected_files = [
        "/data/TESS_Downloads/TIC_123456789/file1_lc.fits",
        "/data/TESS_Downloads/TIC_123456789/file2_lc.fits"
    ]
    assert fits_files == expected_files
    mock_join.assert_called()
    mock_glob.assert_called_with("/data/TESS_Downloads/TIC_123456789/**/*_lc.fits", recursive=True)
