# Contributing to CCS-Validator

We love your input! We want to make contributing to this project as easy and transparent as possible.

## Development Process

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code lints
6. Issue that pull request!

## Local Development Setup

```bash
# Clone your fork
git clone https://github.com/[your-username]/ccs-validator.git
cd ccs-validator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install pytest pytest-cov black flake8

# Run tests
pytest tests/
```

## Code Style
Use Black for formatting: black src/ tests/
Use flake8 for linting: flake8 src/ tests/
Write docstrings for all public methods (NumPy format)
Keep line length under 88 characters

## Testing
Write tests for all new features
Aim for 80%+ code coverage
Run tests before submitting PR: pytest --cov=src tests/

## Pull Request Process
Update the README.md with details of changes if needed
Update the docs/ with any new functionality
The PR will be merged once you have the sign-off of maintainers

## Code of Conduct

### Our Pledge

In the interest of fostering an open and welcoming environment, we as
contributors and maintainers pledge to making participation in our project and
our community a harassment-free experience for everyone.

### Our Standards

Examples of behavior that contributes to creating a positive environment
include:
- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

