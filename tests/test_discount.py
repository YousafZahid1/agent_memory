from gray_proof.discount import apply_discount


def test_apply_discount_returns_float():
    # Sanity check only — asserts the return type, not the value.
    # (The value is wrong; that's the reported bug, reproduced separately.)
    assert isinstance(apply_discount(100, 20), float)
