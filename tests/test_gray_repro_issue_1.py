# Test for apply_discount function returning incorrect result
from gray_proof.discount import apply_discount

def test_apply_discount_correct_result():
    assert apply_discount(100, 20) == 80.0
    assert apply_discount(50, 10) == 45.0
    assert apply_discount(100, 0) == 100.0
