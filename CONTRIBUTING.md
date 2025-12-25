# Contributing to Smart Trash AIOT

Thank you for your interest in contributing to the Smart Trash AIOT project! 🎉

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion:

1. **Check existing issues** to see if it's already reported
2. **Create a new issue** with:
   - Clear title
   - Detailed description
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Your environment (OS, Python version, hardware)

### Submitting Changes

1. **Fork the repository**
   ```bash
   git clone https://github.com/Doancoder777/smart-trash-AIOT.git
   cd smart-trash-AIOT
   ```

2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation if needed

4. **Test your changes**
   ```bash
   # Test the affected modules
   python examples/test_camera.py
   python examples/test_voice.py
   python examples/test_hardware.py
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: brief description of your changes"
   ```

   Use commit message prefixes:
   - `Add:` for new features
   - `Fix:` for bug fixes
   - `Update:` for updates to existing features
   - `Docs:` for documentation changes
   - `Refactor:` for code refactoring

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Describe your changes
   - Link related issues

## Code Style Guidelines

### Python Code Style

Follow PEP 8 with these specifics:

- **Indentation**: 4 spaces
- **Line length**: 100 characters max
- **Naming conventions**:
  - Classes: `PascalCase`
  - Functions/methods: `snake_case`
  - Constants: `UPPER_SNAKE_CASE`
  - Private methods: `_leading_underscore`

### Documentation

- Add docstrings to all functions and classes
- Use Google-style docstrings:

```python
def function_name(param1: type, param2: type) -> return_type:
    """
    Brief description of function.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ExceptionType: When this exception is raised
    """
    pass
```

### Comments

- Write clear, concise comments
- Explain *why*, not *what* (code should be self-explanatory)
- Use inline comments sparingly
- Keep comments up-to-date with code changes

## Areas for Contribution

### High Priority

- [ ] Better AI model training and optimization
- [ ] Web interface for monitoring
- [ ] Mobile app integration
- [ ] Database for waste statistics
- [ ] Multi-bin support

### Features

- [ ] Additional waste categories
- [ ] Weight measurement integration
- [ ] LED indicator lights
- [ ] Email/SMS notifications
- [ ] Cloud data synchronization
- [ ] Bluetooth connectivity

### Hardware Support

- [ ] Support for different servo models
- [ ] Additional sensor types
- [ ] Arduino compatibility
- [ ] ESP32 support

### Improvements

- [ ] Better error handling
- [ ] Performance optimization
- [ ] Power saving modes
- [ ] Unit tests
- [ ] Integration tests
- [ ] CI/CD pipeline

### Documentation

- [ ] Video tutorials
- [ ] More examples
- [ ] Translations (other languages)
- [ ] Hardware assembly guide
- [ ] FAQ section

## Development Setup

### Install Development Dependencies

```bash
pip install -r requirements.txt
pip install pytest pytest-cov black flake8
```

### Code Formatting

```bash
# Format code
black src/

# Check code style
flake8 src/
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/
```

## Community Guidelines

### Be Respectful

- Be kind and courteous
- Respect different viewpoints
- Accept constructive criticism
- Focus on what's best for the project

### Be Collaborative

- Help others when you can
- Share knowledge and resources
- Review pull requests
- Participate in discussions

### Be Professional

- Use clear, professional language
- Stay on topic
- Follow the code of conduct
- Give credit where due

## Questions?

If you have questions:

1. Check the [documentation](docs/)
2. Search [existing issues](https://github.com/Doancoder777/smart-trash-AIOT/issues)
3. Ask in [discussions](https://github.com/Doancoder777/smart-trash-AIOT/discussions)
4. Create a new issue

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to a cleaner environment! 🌍♻️
