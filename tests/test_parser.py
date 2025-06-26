from utils import Parser


def test_001():
    """Test basic function declaration"""
    source = """func main() -> void {}"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_002():
    """Test function with parameters"""
    source = """func add(a: int, b: int) -> int { return a + b; }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_003():
    """Test variable declaration with type annotation"""
    source = """func main() -> void { let x: int = 42; }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_004():
    """Test variable declaration with type inference"""
    source = """func main() -> void { let name = "Alice"; }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_005():
    """Test constant declaration"""
    source = """const PI: float = 3.14159; func main() -> void {}"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_006():
    """Test if-else statement"""
    source = """func main() -> void { 
        if (x > 0) { 
            print("positive"); 
        } else { 
            print("negative"); 
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_007():
    """Test while loop"""
    source = """func main() -> void { 
        let i = 0;
        while (i < 10) { 
            i = i + 1; 
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_008():
    """Test for loop with array"""
    source = """func main() -> void { 
        let numbers = [1, 2, 3, 4, 5];
        for (num in numbers) { 
            print(str(num)); 
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_009():
    """Test array declaration and access"""
    source = """func main() -> void { 
        let arr: [int; 3] = [1, 2, 3];
        let first = arr[0];
        arr[1] = 42;
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_010():
    """Test complex expression with pipeline operator"""
    source = """func main() -> void { 
        let result = data >> process >> validate >> transform;
        let calculation = 5 >> add(3) >> multiply(2);
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_011():
    """Test parser error: missing closing brace in function declaration"""
    source = """func main() -> void { let x = 1; """  # Thiếu dấu }
    expected = "Error on line 1 col 33: <EOF>"
    assert Parser(source).parse() == expected
