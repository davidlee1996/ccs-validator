# CCS-Validator 🔍

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![GitHub issues](https://img.shields.io/github/issues/[YOUR-USERNAME]/ccs-validator)](https://github.com/[YOUR-USERNAME]/ccs-validator/issues)

**Carbon Capture System Validation Framework** - An open-source testing toolkit for validating control software in industrial carbon capture, utilization, and storage (CCUS) systems.

## 🎯 Purpose

CCS-Validator addresses a critical gap in industrial decarbonization: the need for rigorous, automated validation of software that controls carbon capture equipment. As the U.S. EPA's 2024 power plant GHG rule requires 90% CO2 capture for many facilities by 2032 [citation:3], ensuring control system reliability becomes a matter of environmental and economic importance.

This framework helps:
- **Engineers** validate control logic before deployment
- **Regulatory compliance teams** document system reliability
- **Researchers** test novel capture configurations safely

## 🔧 Features

- **Simulation-based testing** – Run control logic against simulated plant conditions
- **Fault injection** – Test system response to sensor failures, communication loss, etc.
- **Compliance validation** – Verify 90% capture rate achievement under various scenarios
- **Reporting tools** – Generate validation reports for regulatory audit
- **Extensible architecture** – Plugin support for different capture technologies (solvent, sorbent, membrane)

## 🏗️ Architecture
ccs-validator/
├── src/
│ ├── core/ # Core validation engine
│ ├── simulators/ # Plant behavior simulators
│ ├── testcases/ # Pre-built test scenarios
│ └── reporters/ # Output formatters
├── examples/ # Example usage
├── tests/ # Unit tests
└── docs/ # Documentation


## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- [Optional] DOE's CCSI Toolset (for advanced simulation) [citation:3]

### Installation

```bash
git clone https://github.com/[YOUR-USERNAME]/ccs-validator.git
cd ccs-validator
pip install -r requirements.txt
```

### Installation

from ccs_validator import CaptureSystem, TestSuite

# Define a simple capture system
system = CaptureSystem(
    capture_rate_target=90.0,  # EPA requirement [citation:3]
    solvent_type="MEA",
    response_time=5.0  # seconds
)

# Create test suite
tests = TestSuite("EPA Compliance Validation")
tests.add_test("steady_state_capture", duration=3600)
tests.add_test("flue_gas_variation", co2_range=(8.0, 12.0))

# Run validation
results = tests.run(system)
results.generate_report("validation_report.pdf")

### 📊 Example Test Scenarios
Test Case	Description	EPA Regulatory Link 
steady_state_capture	Validates sustained 90%+ capture over 1 hour	BSER determination
load_following	Tests response to 20-100% plant load changes	Operational flexibility
sensor_failure	Validates fail-safe behavior on sensor loss	Safety requirements
solvent_degradation	Tests performance with aged solvent	Long-term reliability

### 🤝 Contributing
We welcome contributions! See CONTRIBUTING.md for guidelines.

# Areas needing help:

Additional solvent models (beyond MEA)

Interface with DOE's FOQUS tool 

More fault injection scenarios

Documentation translations

### 📄 License
MIT License - See LICENSE file

### 🙏 Acknowledgments
National Energy Technology Laboratory (NETL) – CCSI Toolset 

Chemical Engineering Transactions community 

EPA's Greenhouse Gas Rule (April 2024) 

### 📬 Contact
David Lee – davidlee.2018.ucb@gmail.com
Project Link: https://github.com/davidlee1996/ccs-validator