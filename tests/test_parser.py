from utils import Parser


def test_001():
    source = """func main() {};"""
    expected = "success"

    assert Parser(source).parse() == expected
