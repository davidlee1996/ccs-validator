#!/usr/bin/env python3
"""
Simple demonstration of CCS-Validator framework.
Run this to see your project in action!
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ccs_validator import CaptureSystem, TestCase, TestSuite


def main():
    print("=" * 60)
    print("CCS-Validator: Carbon Capture System Validation Framework")
    print("=" * 60)
    
    # Create a capture system
    print("\n1️⃣  Initializing Capture System...")
    system = CaptureSystem(
        capture_rate_target=90.0,
        solvent_type='MEA',
        response_time=5.0,
        name="Demo_Plant_1"
    )
    print(f"   ✅ System '{system.name}' created")
    print(f"   📊 Solvent: {system.solvent['name']}")
    print(f"   🎯 Target capture: {system.capture_rate_target}%")
    
    # Create test cases
    print("\n2️⃣  Creating Test Cases...")
    
    # Test 1: Steady-state operation
    test1 = TestCase(
        name="Steady State Validation",
        description="Validate sustained 90%+ capture under normal conditions",
        duration=3600,  # 1 hour
        conditions={
            'co2_range': (10.0, 12.0),
            'load_range': (90.0, 100.0),
            'step_size': 60  # 1-minute steps
        }
    )
    print("   ✅ Test 1: Steady State Validation")
    
    # Test 2: Load following
    test2 = TestCase(
        name="Load Following Test",
        description="Test response to varying plant load (20-100%)",
        duration=7200,  # 2 hours
        conditions={
            'co2_range': (8.0, 15.0),
            'load_range': (20.0, 100.0),
            'step_size': 60
        }
    )
    print("   ✅ Test 2: Load Following Test")
    
    # Test 3: Fault injection
    test3 = TestCase(
        name="Fault Tolerance Test",
        description="Test system response to sensor failure",
        duration=3600,
        conditions={
            'co2_range': (10.0, 12.0),
            'load_range': (80.0, 100.0),
            'step_size': 60
        },
        fault_config={
            'type': 'sensor_drift',
            'start_time': 1800,  # 30 minutes in
            'duration': 300  # 5 minutes
        }
    )
    print("   ✅ Test 3: Fault Tolerance Test")
    
    # Create and run test suite
    print("\n3️⃣  Running Test Suite...")
    suite = TestSuite(
        name="EPA Compliance Validation Suite",
        description="Comprehensive validation for 90% capture compliance"
    )
    
    suite.add_test(test1)
    suite.add_test(test2)
    suite.add_test(test3)
    
    results = suite.run_all(system)
    
    # Display results
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS")
    print("=" * 60)
    
    for test_name, test_result in results.items():
        if test_name not in ['compliance_summary', 'suite_name', 'tests_passed', 'total_tests']:
            print(f"\n{test_name}:")
            print(f"  {'✅ PASSED' if test_result.get('passed') else '❌ FAILED'}")
            print(f"  Average capture rate: {test_result.get('average_capture_rate')}%")
            print(f"  Compliance rate: {test_result.get('compliance_rate')}%")
            print(f"  Faults detected: {test_result.get('faults_detected')}")
    
    print("\n" + "=" * 60)
    print("🏭 EPA COMPLIANCE SUMMARY")
    print("=" * 60)
    
    summary = results.get('compliance_summary', {})
    print(f"Average capture rate: {summary.get('average_capture_rate')}%")
    print(f"Overall compliance rate: {summary.get('compliance_rate')}%")
    print(f"Total CO2 captured: {summary.get('total_co2_captured')} units")
    print(f"Faults detected during testing: {summary.get('faults_detected')}")
    
    epa_status = "✅ COMPLIANT" if summary.get('epa_90_percent_compliant') else "❌ NON-COMPLIANT"
    print(f"\nEPA 90% Capture Requirement: {epa_status}")
    
    print("\n" + "=" * 60)
    print("✨ Demo complete! Your CCS-Validator is working!")
    print("=" * 60)
    
    # Save results
    suite.save_results(results, "demo_test_results.json")
    print("\n📁 Results saved to 'demo_test_results.json'")


if __name__ == "__main__":
    main()