from utils import Tokenizer


def test_001():
    source = "abc"
    expected = "abc,EOF"

    assert Tokenizer(source).get_tokens_as_string() == expected
