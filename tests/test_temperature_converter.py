import pytest
from app.temperature_converter import fahrenheit_to_celsius, celsius_to_fahrenheit

def test_fahrenheit_to_celsius_freezing_point():
    """
    Testa o ponto de congelamento: 32 F = 0 C.
    """
    assert fahrenheit_to_celsius(32.0) == pytest.approx(0.0, 0.001)

def test_fahrenheit_to_celsius_boiling_point():
    """
    Testa o ponto de ebulição: 212 F = 100 C.
    """
    assert fahrenheit_to_celsius(212.0) == pytest.approx(100.0, 0.001)

def test_celsius_to_fahrenheit_freezing_point():
    """
    Testa o ponto de congelamento: 0 C = 32 F.
    """
    assert celsius_to_fahrenheit(0.0) == pytest.approx(32.0, 0.001)

def test_celsius_to_fahrenheit_boiling_point():
    """
    Testa o ponto de ebulição: 100 C = 212 F.
    """
    assert celsius_to_fahrenheit(100.0) == pytest.approx(212.0, 0.001)

# Teste para o Cenário 3 (instável) - este teste irá falhar se o método for alterado
def test_fahrenheit_to_celsius_negative():
    """
    Um ponto de teste adicional que pode ser modificado para causar falha.
    0 F deve ser aproximadamente -17.777 C.
    """
    assert fahrenheit_to_celsius(0.0) == pytest.approx(-17.77777, 0.001)