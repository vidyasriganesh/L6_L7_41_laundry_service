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

def test_member_bonus_applied():
    # member regular: included 5 + 2 = 7, extra 1, rate 30
    assert extra_weight_charge("regular", 8, "standard", True) == 30

def test_standard_charge():
    # included 5, extra 3, rate 30
    assert extra_weight_charge("regular", 8, "standard", False) == 90

def test_express_charge():
    # included 5, extra 3, rate 50
    assert extra_weight_charge("regular", 8, "express", False) == 150

def test_heavy_standard_surcharge():
    # extra 15, rate 30 + 15 = 45
    assert extra_weight_charge("regular", 20, "standard", False) == 675

def test_heavy_express_surcharge():
    # extra 15, rate 50 + 15 + 10 = 75
    assert extra_weight_charge("regular", 20, "express", False) == 1125


# ---------- order_acceptable ----------
def test_order_acceptable():
    assert order_acceptable(10, 20, False) is True

def test_delicate_order_ok():
    assert order_acceptable(2, 5, True) is True

def test_too_heavy_order():
    assert order_acceptable(30, 10, False) is False


# ---------- dropoff_status ----------
def test_dropoff_accepted():
    assert dropoff_status(60, False, False) == "accepted"

def test_dropoff_late():
    assert dropoff_status(45, False, False) == "late"

def test_dropoff_rejected():
    assert dropoff_status(10, False, False) == "rejected"

def test_dropoff_bedding_accepted():
    assert dropoff_status(90, True, False) == "accepted"

def test_dropoff_express_accepted():
    assert dropoff_status(90, False, True) == "accepted"
