"""Core capture system model with EPA compliance tracking"""

import warnings
from datetime import datetime
from typing import Dict, List, Optional, Union
import numpy as np


class CaptureSystem:
    """
    Represents a carbon capture system with comprehensive validation capabilities.
    
    This model simulates the behavior of a post-combustion carbon capture system
    using various solvent technologies. It tracks EPA compliance metrics and
    provides methods for control system validation.
    
    Parameters
    ----------
    capture_rate_target : float, optional
        Target CO2 capture percentage (EPA minimum: 90%) 
    solvent_type : str, optional
        Type of capture solvent ('MEA', 'AMP', 'PZ', or 'blend')
    response_time : float, optional
        System response time in seconds
    name : str, optional
        Identifier for this system instance
    
    Examples
    --------
    >>> system = CaptureSystem(capture_rate_target=90.0, solvent_type='MEA')
    >>> result = system.simulate_step(flue_gas_co2=10.5, timestamp=0)
    >>> print(f"Capture rate: {result['capture_rate']:.1f}%")
    """
    
    # Solvent properties database
    SOLVENT_PROPERTIES = {
        'MEA': {
            'name': 'Monoethanolamine',
            'max_capture': 95.0,
            'regeneration_energy': 3.7,  # GJ/ton CO2
            'degradation_rate': 0.05,      # % per cycle
        },
        'AMP': {
            'name': '2-Amino-2-methyl-1-propanol',
            'max_capture': 92.0,
            'regeneration_energy': 3.2,
            'degradation_rate': 0.03,
        },
        'PZ': {
            'name': 'Piperazine',
            'max_capture': 98.0,
            'regeneration_energy': 2.8,
            'degradation_rate': 0.02,
        },
        'blend': {
            'name': 'Advanced Solvent Blend',
            'max_capture': 96.0,
            'regeneration_energy': 3.0,
            'degradation_rate': 0.04,
        }
    }
    
    def __init__(
        self,
        capture_rate_target: float = 90.0,
        solvent_type: str = 'MEA',
        response_time: float = 5.0,
        name: str = "CaptureSystem_1"
    ):
        self.capture_rate_target = capture_rate_target
        self.solvent_type = solvent_type.lower()
        self.response_time = response_time
        self.name = name
        
        # State tracking
        self.operating_hours = 0.0
        self.total_co2_processed = 0.0
        self.total_co2_captured = 0.0
        self.faults_detected = []
        self.validation_log = []
        
        # Load solvent properties
        if self.solvent_type not in self.SOLVENT_PROPERTIES:
            raise ValueError(
                f"Unknown solvent type '{solvent_type}'. "
                f"Available: {list(self.SOLVENT_PROPERTIES.keys())}"
            )
        self.solvent = self.SOLVENT_PROPERTIES[self.solvent_type]
        
        # Validate EPA compliance
        self._validate_epa_compliance()
    
    def _validate_epa_compliance(self):
        """Check if system meets EPA minimum requirements"""
        if self.capture_rate_target < 90.0:
            warnings.warn(
                f"⚠️ EPA WARNING: Capture target {self.capture_rate_target}% "
                f"is below the minimum 90% required for Baseload Gas Units ",
                UserWarning
            )
        
        if self.solvent['max_capture'] < 90.0:
            warnings.warn(
                f"⚠️ EPA WARNING: Solvent {self.solvent_type} has maximum "
                f"capture rate of {self.solvent['max_capture']}%, "
                f"which may not achieve 90% compliance",
                UserWarning
            )
    
    def simulate_step(
        self,
        flue_gas_co2: float,
        timestamp: Union[float, datetime],
        plant_load: float = 100.0,
        inject_fault: Optional[Dict] = None
    ) -> Dict:
        """
        Simulate one timestep of system operation with advanced dynamics.
        
        Parameters
        ----------
        flue_gas_co2 : float
            Incoming CO2 concentration (%)
        timestamp : float or datetime
            Current simulation time
        plant_load : float, optional
            Current plant load percentage (20-120%)
        inject_fault : dict, optional
            Fault injection parameters for testing
        
        Returns
        -------
        dict
            Comprehensive simulation results
        """
        # Convert timestamp to numeric if needed
        if isinstance(timestamp, datetime):
            t = timestamp.timestamp()
        else:
            t = float(timestamp)
        
        # Apply fault injection if specified
        fault_active = False
        fault_description = None
        if inject_fault:
            fault_active, fault_description = self._apply_fault(inject_fault, t)
        
        # Calculate dynamic capture rate with realistic modeling
        base_rate = self.capture_rate_target
        
        # Solvent efficiency factor
        solvent_factor = self.solvent['max_capture'] / 95.0
        
        # Load factor impact (lower load = lower efficiency)
        load_factor = max(0.6, min(1.2, plant_load / 100.0))
        
        # CO2 concentration impact (optimal range 10-15%)
        if 8.0 <= flue_gas_co2 <= 15.0:
            co2_factor = 1.0
        elif flue_gas_co2 < 8.0:
            co2_factor = 0.8 + (flue_gas_co2 / 40.0)  # Linear drop-off
        else:
            co2_factor = 1.2 - (flue_gas_co2 - 15.0) / 50.0  # Saturation
        
        # Degradation over time
        degradation = 1.0 - (self.solvent['degradation_rate'] * self.operating_hours / 8760.0)
        
        # Calculate final capture rate
        capture_rate = (
            base_rate *
            solvent_factor *
            load_factor *
            co2_factor *
            degradation
        )
        
        # Apply fault effects
        if fault_active:
            capture_rate *= 0.7  # 30% reduction during fault
        
        # Cap at solvent maximum
        capture_rate = min(capture_rate, self.solvent['max_capture'])
        capture_rate = max(capture_rate, 0.0)
        
        # Calculate mass balance
        co2_captured = flue_gas_co2 * capture_rate / 100.0
        co2_emitted = flue_gas_co2 - co2_captured
        
        # Update totals
        self.operating_hours += 1.0 / 3600.0  # Assuming timestamp in seconds
        self.total_co2_processed += flue_gas_co2
        self.total_co2_captured += co2_captured
        
        # Log validation data
        result = {
            'timestamp': t,
            'system_name': self.name,
            'co2_in': round(flue_gas_co2, 2),
            'co2_captured': round(co2_captured, 2),
            'co2_emitted': round(co2_emitted, 2),
            'capture_rate': round(capture_rate, 2),
            'plant_load': plant_load,
            'epa_compliant': capture_rate >= 90.0,
            'fault_active': fault_active,
            'fault_description': fault_description,
            'solvent_type': self.solvent_type,
            'operating_hours': round(self.operating_hours, 2)
        }
        
        self.validation_log.append(result)
        return result
    
    def _apply_fault(self, fault_config: Dict, timestamp: float) -> tuple:
        """
        Apply fault injection for testing control system response.
        
        Parameters
        ----------
        fault_config : dict
            Fault configuration with type, start_time, duration
        timestamp : float
            Current simulation time
        
        Returns
        -------
        tuple
            (fault_active, description)
        """
        fault_type = fault_config.get('type', 'sensor_drift')
        start_time = fault_config.get('start_time', 0)
        duration = fault_config.get('duration', 60)
        
        # Check if fault is active
        if start_time <= timestamp <= (start_time + duration):
            description = f"Fault active: {fault_type}"
            self.faults_detected.append({
                'timestamp': timestamp,
                'type': fault_type,
                'description': description
            })
            return True, description
        
        return False, None
    
    def get_compliance_summary(self) -> Dict:
        """
        Generate EPA compliance summary.
        
        Returns
        -------
        dict
            Compliance metrics and statistics
        """
        if not self.validation_log:
            return {"status": "No data available"}
        
        capture_rates = [entry['capture_rate'] for entry in self.validation_log]
        compliant_steps = sum(1 for entry in self.validation_log if entry['epa_compliant'])
        total_steps = len(self.validation_log)
        
        return {
            'average_capture_rate': round(np.mean(capture_rates), 2),
            'min_capture_rate': round(min(capture_rates), 2),
            'max_capture_rate': round(max(capture_rates), 2),
            'compliance_rate': round(100 * compliant_steps / total_steps, 2),
            'total_co2_captured': round(self.total_co2_captured, 2),
            'faults_detected': len(self.faults_detected),
            'epa_90_percent_compliant': self.total_co2_captured / self.total_co2_processed >= 0.9 if self.total_co2_processed > 0 else False
        }
    
    def reset(self):
        """Reset system state for new simulation"""
        self.operating_hours = 0.0
        self.total_co2_processed = 0.0
        self.total_co2_captured = 0.0
        self.faults_detected = []
        self.validation_log = []