# Contributing to Trading Bot

Thank you for your interest in contributing to the Trading Bot project! This document provides guidelines and instructions for contributing.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/trading-bot.git
   cd trading-bot
   ```

3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/trading-bot.git
   ```

4. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## Development Workflow

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit them:
   ```bash
   git add .
   git commit -m "Add descriptive commit message"
   ```

3. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

4. Create a Pull Request on GitHub

## Code Standards

### Python Code Style
- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep lines under 100 characters

### Commit Messages
- Use clear, descriptive commit messages
- Start with a verb (Add, Fix, Update, Improve, etc.)
- Example: "Add RSI strategy implementation"

### Testing
- Write tests for new features
- Ensure all tests pass before submitting PR
- Run linting checks:
  ```bash
  flake8 src/
  ```

## Adding New Strategies

1. Create a new strategy class in `src/trading_bot/strategies/`
2. Inherit from `BaseStrategy` (or check existing implementations)
3. Implement required methods: `generate_signal()`, `update_parameters()`
4. Add tests for your strategy
5. Update documentation in README.md

### Strategy Template

```python
from trading_bot.strategies.ma_strategy import BaseStrategy

class YourStrategy(BaseStrategy):
    """Your strategy description."""
    
    def __init__(self, param1=default_value):
        """Initialize strategy with parameters."""
        self.param1 = param1
    
    def generate_signal(self, data):
        """Generate trading signal from market data."""
        # Implementation here
        return signal  # -1 (sell), 0 (hold), 1 (buy)
    
    def update_parameters(self, **kwargs):
        """Update strategy parameters."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
```

## Adding New Platform Adapters

1. Create a new adapter in `src/trading_bot/platforms/`
2. Inherit from `BasePlatform`
3. Implement required methods: `connect()`, `place_order()`, `get_account_info()`, etc.
4. Add tests for your adapter
5. Update documentation

## Reporting Issues

### Bug Reports
- Use the bug report template
- Include environment details (OS, Python version, etc.)
- Provide steps to reproduce
- Include relevant log excerpts

### Feature Requests
- Use the feature request template
- Describe the use case
- Suggest a solution if possible
- Include examples if applicable

## Pull Request Process

1. Ensure your code follows the project's code standards
2. Update documentation and README if needed
3. Add or update tests for your changes
4. Ensure all tests pass
5. Fill out the PR template completely
6. Wait for review and address feedback

## Code Review Guidelines

All pull requests will be reviewed for:
- Code quality and adherence to standards
- Test coverage
- Documentation
- Performance implications
- Security considerations

## License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project (typically MIT or similar).

## Questions?

- Check the [README.md](README.md) for project overview
- Review [GITHUB_SETUP.md](GITHUB_SETUP.md) for setup instructions
- Open an issue with your question

## Resources

- [GitHub Flow Guide](https://guides.github.com/introduction/flow/)
- [How to Write Good Commit Messages](https://chris.beams.io/posts/git-commit/)
- [PEP 8 Style Guide](https://pep8.org/)
- [Python Documentation](https://docs.python.org/3/)

Thank you for contributing!
