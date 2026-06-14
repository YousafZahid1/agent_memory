# word_count function returns incorrect character count instead of word count
from gray_proof.text_stats import word_count

def test_word_count():
    assert word_count('hello world') == 2
    assert word_count('a b c') == 3
    assert word_count('') == 0
