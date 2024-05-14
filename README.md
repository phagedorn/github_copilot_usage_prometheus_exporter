# GitHub Copilot Usage Prometheus Exporter

This project is a Prometheus exporter for GitHub Copilot usage data. It fetches data from the GitHub API and exposes it as Prometheus metrics.

![Example Image](usage.png)

## Prerequisites

- Python 3.6 or higher
- A GitHub personal access token with the appropriate permissions

## Installation

1. Clone the repository:

   ```
   $ git clone https://github.com/yourusername/github-copilot-prometheus-exporter.git
   ```

2. Navigate to the project directory:
cd github-copilot-prometheus-exporter

3. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Set the following environment variables:
   - `GITHUB_TOKEN`: Your GitHub personal access token
   - `ENTERPRISE_NAME`: The name of your GitHub Enterprise
   - `ORG_NAME`: The name of your GitHub Organization

   Example:
   ```
   export GITHUB_TOKEN="asd9ausd9uasd9u9a9u9uasd"
   export ENTERPRISE_NAME="YOUR_ENTERPRISE_NAME"
   export ORG_NAME="YOUR_ORG_NAME"
   ```

2. Run the exporter:

   ```
   $ python github-copilot-prometheus-exporter.py
   ```

The exporter will start a server on port 8000 and fetch data periodically.

## Running with Docker Compose

1. Create a `.env` file in the root directory of the project with the following content:

    ```env
    GITHUB_TOKEN=your_github_token
    ENTERPRISE_NAME=your_enterprise_name
    ORG_NAME=your_org_name
    ```

2. Build and run the Docker container using Docker Compose:

    ```sh
    docker-compose up --build
    ```

## Metrics

The exporter provides the following metrics:

- `enterprise_usage_gauge`: Usage data for your GitHub Enterprise
- `org_billing_gauge`: Billing data for your GitHub organization

Each metric is labeled with the name of the data it represents.

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.