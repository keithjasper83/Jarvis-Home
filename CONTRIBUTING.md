# Contributing to Jarvis Home Automation

Thank you for your interest in contributing to Jarvis! This document provides guidelines for contributing to the project.

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Jarvis-Home.git
   cd Jarvis-Home
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Create your configuration:
   ```bash
   cp config/config.example.yaml config/config.yaml
   cp .env.example .env
   ```

## Code Style

- Follow PEP 8 guidelines for Python code
- Use meaningful variable and function names
- Add docstrings to all classes and functions
- Keep functions focused and single-purpose
- Use type hints where appropriate

## Project Structure

```
src/jarvis/
├── data_collectors/     # Device and system data collectors
│   ├── base_collector.py       # Abstract base class
│   ├── shelly_collector.py     # Shelly devices
│   ├── tapo_collector.py       # Tapo devices
│   ├── alexa_collector.py      # Alexa integration
│   ├── windows_collector.py    # Windows monitoring
│   └── mac_collector.py        # Mac monitoring
├── config/              # Configuration management
│   └── config_manager.py
├── models/              # Data models
│   └── device_data.py
└── main.py              # Application entry point
```

## Adding a New Data Collector

To add support for a new device or service:

1. Create a new file in `src/jarvis/data_collectors/`:
   ```python
   from .base_collector import BaseCollector
   from ..models.device_data import DeviceData
   
   class MyCollector(BaseCollector):
       def __init__(self, config: dict):
           super().__init__("my_collector", config)
       
       def connect(self) -> bool:
           # Implementation
           pass
       
       def disconnect(self) -> bool:
           # Implementation
           pass
       
       def collect_data(self) -> List[DeviceData]:
           # Implementation
           pass
   ```

2. Register the collector in `main.py`:
   ```python
   collector_classes = {
       # ... existing collectors
       'my_collector': MyCollector
   }
   ```

3. Add configuration schema to `config.example.yaml`:
   ```yaml
   collectors:
     my_collector:
       enabled: false
       # Add your configuration options
   ```

4. Update documentation in README.md

## Testing

Currently, the project is in the foundation phase. As the project grows:

1. Write unit tests for new collectors
2. Test with actual devices when possible
3. Document test setup requirements
4. Add integration tests for end-to-end flows

## Commit Guidelines

- Use clear, descriptive commit messages
- Start with a verb (Add, Fix, Update, Remove, etc.)
- Keep commits focused on a single change
- Reference issues in commit messages when applicable

Examples:
- `Add support for Philips Hue devices`
- `Fix Shelly collector connection timeout`
- `Update README with installation instructions`

## Pull Request Process

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/my-new-feature
   ```

2. Make your changes and commit them

3. Push to your fork:
   ```bash
   git push origin feature/my-new-feature
   ```

4. Create a Pull Request with:
   - Clear description of the changes
   - Reference to any related issues
   - Screenshots or logs if applicable

5. Wait for review and address any feedback

## Architecture Principles

The project follows these principles:

- **Domain-Driven Design (DDD)**: Organize code around business domains
- **Separation of Concerns (SOC)**: Keep data collection, processing, and control separate
- **Extensibility**: Easy to add new device types and features
- **Configuration-driven**: Minimize hard-coded values
- **Logging**: Comprehensive logging for debugging and monitoring

## Future Roadmap

Areas where contributions are especially welcome:

- API integration implementations for Shelly, Tapo, Alexa
- Data storage layer (database integration)
- RESTful API for external access
- Web dashboard for monitoring
- Automation rules engine
- Machine learning for predictive automation
- Mobile app development

## Questions?

If you have questions or need help, please:
- Open an issue for bugs or feature requests
- Start a discussion for questions and ideas
- Check existing issues and discussions first

## License

By contributing to Jarvis, you agree that your contributions will be licensed under the Apache License 2.0.
