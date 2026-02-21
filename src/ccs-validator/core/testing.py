"""Test suite management for CCS validation"""

from typing import List, Dict, Optional, Union
from datetime import datetime
import json
from .system import CaptureSystem


class TestCase:
    """
    Individual test case for CCS validation.
    
    Parameters
    ----------
    name : str
        Test case name
    description : str
        Detailed test description
    duration : int
        Test duration in seconds
    conditions : dict
        Test conditions (CO2 range, load range, etc.)
    fault_config : dict, optional
        Fault to inject during test
    """
    
    def __init__(
        self,
        name: str,
        description: str,
        duration: int,
        conditions: Dict,
        fault_config: Optional[Dict] = None
    ):
        self.name = name
        self.description = description
        self.duration = duration
        self.conditions = conditions
        self.fault_config = fault_config
        self.results = []
    
    def run(self, system: CaptureSystem) -> Dict:
        """
        Execute the test case on a capture system.
        
        Parameters
        ----------
        system : CaptureSystem
            System under test
        
        Returns
        -------
        dict
            Test results
        """
        self.results = []
        
        # Extract test conditions
        co2_range = self.conditions.get('co2_range', (10.0, 12.0))
        load_range = self.conditions.get('load_range', (80.0, 100.0))
        step_size = self.conditions.get('step_size', 1.0)  # seconds
        
        # Run simulation
        for t in range(0, self.duration, int(step_size)):
            # Vary conditions realistically
            co2_cycle = co2_range[0] + (co2_range[1] - co2_range[0]) * (
                0.5 + 0.5 * (t % 3600) / 3600
            )
            
            load_cycle = load_range[0] + (load_range[1] - load_range[0]) * (
                0.5 + 0.5 * (t % 1800) / 1800
            )
            
            # Check if fault should be active
            fault_active = False
            if self.fault_config:
                fault_active = (
                    self.fault_config.get('start_time', 0) <= t <=
                    (self.fault_config.get('start_time', 0) + 
                     self.fault_config.get('duration', 60))
                )
            
            # Run simulation step
            result = system.simulate_step(
                flue_gas_co2=co2_cycle,
                timestamp=t,
                plant_load=load_cycle,
                inject_fault=self.fault_config if fault_active else None
            )
            self.results.append(result)
        
        # Compile test report
        return self.generate_report()
    
    def generate_report(self) -> Dict:
        """Generate test report"""
        if not self.results:
            return {"status": "No results"}
        
        capture_rates = [r['capture_rate'] for r in self.results]
        compliant = [r['epa_compliant'] for r in self.results]
        faults = [r for r in self.results if r['fault_active']]
        
        return {
            'test_name': self.name,
            'description': self.description,
            'duration': self.duration,
            'steps_executed': len(self.results),
            'average_capture_rate': round(sum(capture_rates) / len(capture_rates), 2),
            'min_capture_rate': min(capture_rates),
            'max_capture_rate': max(capture_rates),
            'compliance_rate': round(100 * sum(compliant) / len(compliant), 2),
            'faults_detected': len(faults),
            'passed': sum(compliant) / len(compliant) >= 0.95  # 95% compliance required
        }


class TestSuite:
    """
    Collection of test cases for comprehensive validation.
    
    Parameters
    ----------
    name : str
        Suite name
    description : str
        Suite description
    """
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.test_cases: List[TestCase] = []
    
    def add_test(self, test_case: TestCase):
        """Add a test case to the suite"""
        self.test_cases.append(test_case)
    
    def add_test_from_config(self, config: Dict):
        """Add test case from configuration dictionary"""
        test_case = TestCase(
            name=config['name'],
            description=config['description'],
            duration=config['duration'],
            conditions=config['conditions'],
            fault_config=config.get('fault_config')
        )
        self.add_test(test_case)
    
    def run_all(self, system: CaptureSystem) -> Dict:
        """
        Run all test cases in the suite.
        
        Returns
        -------
        dict
            Comprehensive test results
        """
        results = {}
        system.reset()  # Start fresh
        
        for i, test in enumerate(self.test_cases):
            print(f"Running test {i+1}/{len(self.test_cases)}: {test.name}")
            results[test.name] = test.run(system)
        
        # Generate final compliance summary
        results['compliance_summary'] = system.get_compliance_summary()
        results['suite_name'] = self.name
        results['tests_passed'] = sum(
            1 for r in results.values() 
            if isinstance(r, dict) and r.get('passed', False)
        )
        results['total_tests'] = len(self.test_cases)
        
        return results
    
    def save_results(self, results: Dict, filename: str):
        """Save test results to JSON file"""
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)