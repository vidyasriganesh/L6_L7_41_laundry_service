import pytest
from laundry_service import extra_weight_charge, order_acceptable, dropoff_status


# ---------- extra_weight_charge ----------
def test_within_included_weight():
    assert extra_weight_charge("regular", 4, "standard", False) == 0

def test_unknown_garment():
    with pytest.raises(ValueError):
        extra_weight_charge("shoes", 4, "standard", False)

def test_negative_weight():
    with pytest.raises(ValueError):
        extra_weight_charge("regular", -1, "standard", False)

def test_zero_weight_is_valid():
    assert extra_weight_charge("regular", 0, "standard", False) == 0

def test_exactly_included_weight():
    assert extra_weight_charge("regular", 5, "standard", False) == 0

def test_member_bonus_applied():
    assert extra_weight_charge("regular", 8, "standard", True) == 30

def test_member_delicate_bonus():
    assert extra_weight_charge("delicate", 6, "standard", True) == 30

def test_member_bedding_no_bonus():
    assert extra_weight_charge("bedding", 10, "standard", True) == 60

def test_non_member_bedding():
    assert extra_weight_charge("bedding", 10, "standard", False) == 60

def test_non_member_no_bonus():
    assert extra_weight_charge("regular", 8, "standard", False) == 90

def test_standard_charge():
    assert extra_weight_charge("regular", 8, "standard", False) == 90

def test_express_charge():
    assert extra_weight_charge("regular", 8, "express", False) == 150

def test_other_speed_uses_express_rate():
    assert extra_weight_charge("regular", 8, "overnight", False) == 150

def test_extra_exactly_10_no_surcharge():
    assert extra_weight_charge("regular", 15, "standard", False) == 300

def test_extra_just_over_10_standard():
    assert extra_weight_charge("regular", 16, "standard", False) == 495

def test_heavy_standard_surcharge():
    assert extra_weight_charge("regular", 20, "standard", False) == 675

def test_heavy_express_surcharge():
    assert extra_weight_charge("regular", 20, "express", False) == 1125


# ---------- order_acceptable ----------
def test_order_acceptable():
    assert order_acceptable(10, 20, False) is True

def test_delicate_order_ok():
    assert order_acceptable(2, 5, True) is True

def test_delicate_too_many_items():
    assert order_acceptable(2, 6, True) is False

def test_exactly_25kg_ok():
    assert order_acceptable(25, 10, False) is True

def test_too_heavy_order():
    assert order_acceptable(26, 10, False) is False

def test_exactly_40_items_ok():
    assert order_acceptable(10, 40, False) is True

def test_too_many_items():
    assert order_acceptable(10, 41, False) is False


# ---------- dropoff_status ----------
def test_dropoff_accepted():
    assert dropoff_status(60, False, False) == "accepted"

def test_dropoff_late_upper():
    assert dropoff_status(59, False, False) == "late"

def test_dropoff_late_lower():
    assert dropoff_status(40, False, False) == "late"

def test_dropoff_rejected():
    assert dropoff_status(39, False, False) == "rejected"

def test_dropoff_bedding_accepted():
    assert dropoff_status(90, True, False) == "accepted"

def test_dropoff_bedding_late():
    assert dropoff_status(70, True, False) == "late"

def test_dropoff_bedding_rejected():
    assert dropoff_status(69, True, False) == "rejected"

def test_dropoff_express_accepted():
    assert dropoff_status(90, False, True) == "accepted"

def test_dropoff_express_late():
    assert dropoff_status(70, False, True) == "late"

def test_dropoff_bedding_express_accepted():
    assert dropoff_status(120, True, True) == "accepted"

def test_dropoff_bedding_express_late():
    assert dropoff_status(100, True, True) == "late"

def test_dropoff_bedding_express_rejected():
    assert dropoff_status(99, True, True) == "rejected"
