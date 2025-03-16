import os
import pytest
from src.tess_data_handler import TESSDataHandler
import json

@pytest.fixture
def handler():
    return TESSDataHandler()

def test_search_tess_targets(handler):
    result = handler.search_tess_targets((5991, 5993), (18, 19))
    assert result is not None
    assert len(result) > 0

def test_verify_tess_timeseries(handler):
    test_target = handler.search_tess_targets((5991, 5993), (18, 19))
    tic_ids = test_target['ID'][:5]  # Limit to first 5 for testing
    stars_with_data, stars_without_data = handler.verify_tess_timeseries(tic_ids)
    assert len(stars_with_data) > 0 or len(stars_without_data) > 0

def test_fetch_timeseries_data(handler):
    test_target = handler.search_tess_targets((5991, 5993), (18, 19))
    tic_id = test_target['ID'][0]
    result = handler.fetch_timeseries_data(tic_id)
    assert result is not None
    assert os.path.exists(result)

def test_output_stars_data(handler):
    handler.stars_data["with_timeseries"].add(123456789)
    handler.stars_data["without_timeseries"].add(987654321)
    handler.output_stars_data()
    assert os.path.exists(handler.data_file)
    with open(handler.data_file, "r") as file:
        data = json.load(file)
        assert 123456789 in data["with_timeseries"]
        assert 987654321 in data["without_timeseries"]    

@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_check_known_exoplanets(handler):
    test_target = handler.search_tess_targets((5991, 5993), (18, 19))
    tic_ids = test_target['ID'][:5]  # Limit to first 5 for testing
    stars_with_data, _ = handler.verify_tess_timeseries(tic_ids)
    result = handler.check_known_exoplanets(stars_with_data)
    assert isinstance(result, list)
