from random import Random

from business_simulator import BusinessSimulator, clamp


def test_clamp_bounds():
    assert clamp(-1, 0, 10) == 0
    assert clamp(11, 0, 10) == 10
    assert clamp(4, 0, 10) == 4


def test_invalid_action_message():
    sim = BusinessSimulator(rng=Random(1))
    result = sim.apply_action("invalid")
    assert "Unknown action" in result


def test_month_advance_and_state_changes():
    sim = BusinessSimulator(rng=Random(1))
    month_before = sim.state.month
    sim.apply_action("improve_product")
    assert sim.state.month == month_before + 1
    assert sim.state.product_quality >= 58


def test_game_ends_after_12_months():
    sim = BusinessSimulator(rng=Random(2))
    for _ in range(12):
        sim.apply_action("do_nothing")
    assert sim.state.game_over is True


def test_game_can_end_from_bankruptcy():
    sim = BusinessSimulator(rng=Random(99))
    for _ in range(6):
        sim.apply_action("hire_staff")
        if sim.state.game_over:
            break
    assert sim.state.cash <= 10000
