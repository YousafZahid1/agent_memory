"""Small pricing helper used by the agent_memory demo."""


def apply_discount(price, percent):
    """Apply a percentage discount to a price and return the FINAL price.

    Examples:
        apply_discount(100, 20) -> 80.0   # 20% off 100 leaves 80
        apply_discount(50, 10)  -> 45.0   # 10% off 50 leaves 45
        apply_discount(100, 0)  -> 100.0  # no discount, full price
    """
    return price * percent / 100.0
