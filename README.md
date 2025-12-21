# Jarvis-Home

A comprehensive home automation platform that collects, analyzes, and manages data from multiple smart home devices and systems.

## Overview

Jarvis is a Python-based home automation system designed to integrate with various smart home platforms and devices. The initial focus is on data collection from multiple sources to enable intelligent automation decisions.

### Supported Data Sources

- **Shelly** - Smart home devices (switches, sensors, etc.)
- **Tapo** - TP-Link smart home devices
- **Alexa** - Amazon Echo devices and services
- **Windows** - Windows system monitoring
- **Mac** - macOS system monitoring

### Architecture

The project follows a clean architecture with:
- **Domain-Driven Design (DDD)** - Organized around business domains
- **Separation of Concerns (SOC)** - Clear separation between data collection, processing, and control
- **API-First** - RESTful APIs for all interactions

## Project Structure

```
jarvis-home/
├── src/
│   └── jarvis/
│       ├── data_collectors/    # Device and system data collectors
│       ├── config/              # Configuration management
│       ├── models/              # Data models
│       └── main.py              # Application entry point
├── tests/                       # Unit and integration tests
├── config/                      # Configuration files
├── requirements.txt             # Python dependencies
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/keithjasper83/Jarvis-Home.git
cd Jarvis-Home
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your device credentials and settings
```

### Configuration

Copy the example configuration and customize it:
```bash
cp config/config.example.yaml config/config.yaml
```

Edit `config/config.yaml` to add your device credentials and preferences.

### Running

```bash
python src/jarvis/main.py
```

## Features

### Current Features (v0.1)
- Modular data collector architecture
- Support for multiple device types
- Configuration-driven setup
- Extensible design for future integrations

### Planned Features
- Real-time data monitoring dashboard
- Automated scheduling and routines
- Climate control integration
- Relay access control
- LED animation control
- Machine learning-based automation
- RESTful API for external integrations
- Mobile app support

## Development

### Adding a New Data Collector

1. Create a new collector class in `src/jarvis/data_collectors/`
2. Inherit from `BaseCollector`
3. Implement required methods: `connect()`, `collect_data()`, `disconnect()`
4. Register the collector in the configuration

Example:
```python
from src.jarvis.data_collectors.base_collector import BaseCollector

class MyDeviceCollector(BaseCollector):
    def connect(self):
        # Connection logic
        pass
    
    def collect_data(self):
        # Data collection logic
        return data
    
    def disconnect(self):
        # Cleanup logic
        pass
```

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Roadmap

- **Phase 1**: Data Collection Foundation (Current)
  - Implement base collector architecture
  - Add support for Shelly, Tapo, Alexa, Windows, and Mac
  - Basic configuration management
  
- **Phase 2**: Data Processing and Storage
  - Time-series database integration
  - Data aggregation and analysis
  - Historical data visualization
  
- **Phase 3**: Automation Engine
  - Rule-based automation
  - Scheduling system
  - Event-driven triggers
  
- **Phase 4**: Advanced Features
  - Machine learning integration
  - Predictive automation
  - Mobile applications
  - Voice control enhancements

## Support

For issues, questions, or contributions, please open an issue on GitHub.

## Acknowledgments

- Thanks to all the smart home device manufacturers for their APIs
- Open source community for inspiration and tools