"""Basic tests for CCS-Validator"""

import pytest
from ccs_validator import CaptureSystem

def test_system_creation():
    """Test that capture system initializes correctly"""
    system = CaptureSystem(capture_rate_target=90.0)
    assert system.capture_rate_target == 90.0
    assert system.solvent_type == "MEA"

def test_system_warning():
    """Test warning for sub-90% target"""
    with pytest.warns(UserWarning):
        CaptureSystem(capture_rate_target=85.0)