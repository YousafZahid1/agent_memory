from gray_proof.text_stats import word_count
def test_word_count_returns_int():
    assert isinstance(word_count("a b c"), int)   # weak: only checks type
