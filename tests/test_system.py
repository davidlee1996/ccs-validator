"""Unit tests for CaptureSystem"""

import pytest
import warnings
from src.ccs_validator import CaptureSystem


def test_system_creation():
    """Test basic system initialization"""
    system = CaptureSystem(capture_rate_target=90.0)
    assert system.capture_rate_target == 90.0
    assert system.solvent_type == 'mea'
    assert system.name == "CaptureSystem_1"


def test_system_warning_for_low_target():
    """Test warning for sub-90% target"""
    with pytest.warns(UserWarning, match="below the minimum 90%"):
        CaptureSystem(capture_rate_target=85.0)


def test_invalid_solvent():
    """Test error for unknown solvent"""
    with pytest.raises(ValueError, match="Unknown solvent type"):
        CaptureSystem(solvent_type="INVALID_SOLVENT")


def test_simulation_step():
    """Test basic simulation step"""
    system = CaptureSystem()
    result = system.simulate_step(flue_gas_co2=10.5, timestamp=0)
    
    assert 'capture_rate' in result
    assert 'co2_captured' in result
    assert 'epa_compliant' in result
    assert result['system_name'] == "CaptureSystem_1"


def test_fault_injection():
    """Test fault injection capability"""
    system = CaptureSystem()
    
    # Inject fault
    fault_config = {
        'type': 'sensor_drift',
        'start_time': 10,
        'duration': 20
    }
    
    # Before fault
    result1 = system.simulate_step(10.5, 5, inject_fault=fault_config)
    assert not result1['fault_active']
    
    # During fault
    result2 = system.simulate_step(10.5, 15, inject_fault=fault_config)
    assert result2['fault_active']
    assert result2['fault_description'] == "Fault active: sensor_drift"
    
    # After fault
    result3 = system.simulate_step(10.5, 35, inject_fault=fault_config)
    assert not result3['fault_active']


def test_compliance_summary():
    """Test compliance summary generation"""
    system = CaptureSystem()
    
    # Run some simulations
    for i in range(10):
        system.simulate_step(10.0 + i, i)
    
    summary = system.get_compliance_summary()
    
    assert 'average_capture_rate' in summary
    assert 'compliance_rate' in summary
    assert 'epa_90_percent_compliant' in summary


def test_system_reset():
    """Test system state reset"""
    system = CaptureSystem()
    
    # Run some simulations
    system.simulate_step(10.5, 0)
    system.simulate_step(11.0, 1)
    
    assert len(system.validation_log) == 2
    
    system.reset()
    assert len(system.validation_log) == 0
    assert system.operating_hours == 0.0