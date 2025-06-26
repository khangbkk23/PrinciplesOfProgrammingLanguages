from utils import Tokenizer


# def test_001():
#     """Test basic identifier tokenization"""
#     source = "duy.tran2903."
#     expected = "duy.tran2903,EOF"
#     assert Tokenizer(source).get_tokens_as_string() == expected

# def test_002():
#     """Test basic identifier tokenization"""
#     source = "1_234_567"
#     expected = "1234567,EOF"
#     assert Tokenizer(source).get_tokens_as_string() == expected

def test_003():
    """Test basic identifier tokenization"""
    source = "21A"
    expected = "21A,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected