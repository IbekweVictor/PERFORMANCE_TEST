# Load Testing Framework for E-commerce Website
==============================================

## Overview

This is a load testing framework designed to simulate user traffic on an e-commerce website. The framework uses Locust, a Python-based load testing tool, to define user behavior and simulate traffic.

## Features

*   **Multi-stage load pattern**: The framework uses a custom load test shape to gradually ramp up and down through defined stages, simulating a realistic traffic pattern.
*   **User behavior simulation**: The framework defines user behavior using Locust's `HttpUser` class, simulating actions such as browsing products, adding to cart, and checking out.
*   **CSV data-driven testing**: The framework uses CSV files to drive test data, allowing for easy modification and extension of test scenarios.
*   **Custom logging**: The framework uses a custom logging configuration to provide detailed logs of test execution.

## Requirements

*   Python 3.7+
*   Locust 1.4+
*   `csv` and `logging` libraries

## Installation

1.  Clone the repository: `git clone https://github.com/your-repo/load-testing-framework.git`
2.  Install dependencies: `pip install -r requirements.txt`
3.  Configure the framework by modifying the `loadfile/locust.conf` file.

## Usage

1.  Run the load test: `locust -f loadfile/loadtest.py --headless --num_users=100 --hatch_rate=10`
2.  Monitor the test execution using the Locust web interface: `http://localhost:8089`

## Configuration

The framework can be configured by modifying the following files:

*   `loadfile/locust.conf`: Configure the load test settings, such as the host, headless mode, and logging level.
*   `load_patterns/stages_pattern.py`: Define the multi-stage load pattern, including the duration and number of users for each stage.
*   `test_data/read_test_data.py`: Configure the CSV data-driven testing, including the file paths and data formats.

## Customization

The framework can be customized by extending the `HttpUser` class and defining new user behavior. Additionally, new test data can be added by modifying the CSV files or creating new ones.

## Contributing

Contributions are welcome! Please submit a pull request with your changes, and ensure that the code is properly tested and documented.

## License

This framework is licensed under the MIT License. See `LICENSE` for details.