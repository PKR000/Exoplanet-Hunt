from src.main import main

def test_main(capsys):
    main()
    captured = capsys.readouterr()
    assert captured.out == "Welcome to Exoplanet Hunt!\n"
