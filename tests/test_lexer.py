from utils import Tokenizer


def test_001():
    """Test basic identifier tokenization"""
    source = "abc"
    expected = "abc,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_002():
    """Test keywords recognition"""
    source = "func main if else while for let const"
    expected = "func,main,if,else,while,for,let,const,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_003():
    """Test integer literals"""
    source = "42 0 -17 007"
    expected = "42,0,-,17,007,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_004():
    """Test float literals"""
    source = "3.14 -2.5 0.0 42. 5."
    expected = "3.14,-,2.5,0.0,42.,5.,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_005():
    """Test boolean literals"""
    source = "true false"
    expected = "true,false,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_006():
    """Test unclosed string literal error"""
    source = '"Hello World'
    expected = "Unclosed String: Hello World"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_007():
    """Test illegal escape sequence error"""
    source = '"Hello \\x World"'
    expected = "Illegal Escape In String: Hello \\x"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_008():
    """Test error character (non-ASCII or invalid character)"""
    source = "let x = 5; @ invalid"
    expected = "let,x,=,5,;,Error Token @"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_009():
    """Test valid string literals with escape sequences"""
    source = '"Hello World" "Line 1\\nLine 2" "Quote: \\"text\\""'
    expected = "Hello World,Line 1\\nLine 2,Quote: \\\"text\\\",EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_009a():
    """Test string literals return content without quotes"""
    source = '"Hello World"'
    expected = "Hello World,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_009b():
    """Test empty string literal"""
    source = '""'
    expected = ",EOF"  # Empty string content
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_010():
    """Test operators and separators"""
    source = "+ - * / % == != < <= > >= && || ! = -> >> ( ) [ ] { } , ; :"
    expected = "+,-,*,/,%,==,!=,<,<=,>,>=,&&,||,!,=,->,>>,(,),[,],{,},,,;,:,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected