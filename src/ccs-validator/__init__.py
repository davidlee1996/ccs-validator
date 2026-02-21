"""
CCS-Validator: Carbon Capture System Validation Framework
==========================================================

An open-source testing toolkit for validating control software
in industrial carbon capture, utilization, and storage (CCUS) systems.

Key Features:
- Simulation-based testing of capture systems
- EPA compliance validation (90% capture rate)
- Fault injection and safety testing
- Regulatory report generation
"""

__version__ = "0.1.0"
__author__ = "[Your Name]"
__email__ = "[your.email@example.com]"

from .core.system import CaptureSystem
from .core.testing import TestSuite, TestCase
from .simulators.plant import PlantSimulator

__all__ = [
    "CaptureSystem",
    "TestSuite", 
    "TestCase",
    "PlantSimulator",
]