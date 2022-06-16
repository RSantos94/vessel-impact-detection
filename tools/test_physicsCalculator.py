from tools.physicsCalculator import PhysicsCalculator


def test_calculate_acceleration():
    assert PhysicsCalculator.calculate_acceleration(10, )


def test_calculate_force():
    assert PhysicsCalculator.calculate_force(10, 5) == 50
