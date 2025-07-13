import importlib.util
from pathlib import Path
import types
import sys

# Carrega o módulo de consultas sem executá-lo como script
spec = importlib.util.spec_from_file_location(
    "sidra_script",
    Path(__file__).resolve().parents[1] / "Script DML carregar base sidra_mysql.py",
)
mod = importlib.util.module_from_spec(spec)
# Cria stubs para dependências externas ausentes
sys.modules.setdefault("requests", types.ModuleType("requests"))
sys.modules.setdefault("mysql", types.ModuleType("mysql"))
sys.modules.setdefault("mysql.connector", types.ModuleType("mysql.connector"))
spec.loader.exec_module(mod)

consultas = mod.consultas


def test_extrair_8880_valor_convertido():
    extrair = consultas[0]["extrair"]
    registro = {"V": "10.5", "D2N": "ind", "D3N": "uf", "D4C": "202301", "D4N": "Jan"}
    assert extrair(registro) == (10.5, "ind", "uf", "202301", "Jan")


def test_extrair_8880_valor_vazio():
    extrair = consultas[0]["extrair"]
    registro = {"V": "", "D2N": "ind", "D3N": "uf", "D4C": "202301", "D4N": "Jan"}
    assert extrair(registro)[0] is None


def test_extrair_8881_converte_int():
    extrair = consultas[1]["extrair"]
    registro = {"V": "1", "D2N": "ind", "D3N": "uf", "D4C": "202301", "D4N": "Jan"}
    resultado = extrair(registro)
    assert resultado == (1.0, "ind", "uf", 202301, "Jan")


def test_extrair_8881_valor_vazio():
    extrair = consultas[1]["extrair"]
    registro = {"V": "", "D2N": "ind", "D3N": "uf", "D4C": "202301", "D4N": "Jan"}
    assert extrair(registro)[0] is None


def test_extrair_8882_campos():
    extrair = consultas[2]["extrair"]
    registro = {
        "V": "2",
        "D2N": "ind",
        "D3N": "ativ",
        "D4N": "uf",
        "D5C": "cod",
        "D5N": "mes",
    }
    assert extrair(registro) == (2.0, "ind", "ativ", "uf", "cod", "mes")


def test_extrair_8883_valor_vazio():
    extrair = consultas[3]["extrair"]
    registro = {
        "V": "",
        "D2N": "ind",
        "D3N": "ativ",
        "D4N": "uf",
        "D5C": "cod",
        "D5N": "mes",
    }
    assert extrair(registro)[0] is None
