from utils import Parser


def test_001():
    """Test basic function declaration"""
    source = """int a, b,c;
    float foo(int a; float c, d) {
        int e ;
        e = expr ;
        c = expr ;
        foo(expr);
        return expr;
    }
    float goo (float a, b) {
        return expr;
    }"""
    expected = "success"
    assert Parser(source).parse() == expected