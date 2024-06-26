import os
import time
import requests
from prometheus_client import start_http_server, Gauge
import json

# Prometheus metrics setup
enterprise_usage_gauge = Gauge('github_enterprise_copilot_usage', 'Usage metrics for GitHub Copilot at the enterprise level', ['metric_name'])
org_billing_gauge = Gauge('github_org_copilot_billing', 'Billing metrics for GitHub Copilot at the organization level', ['metric_name'])

def get_github_token():
    return os.getenv("GITHUB_TOKEN")

def get_enterprise_name():
    return os.getenv("ENTERPRISE_NAME")

def get_org_name():
    return os.getenv("ORG_NAME")

def fetch_enterprise_usage(enterprise_name, org_name, github_token):
    """Fetch metrics from GitHub and update Prometheus gauges."""
    try:
        # Fetch enterprise usage
        enterprise_response = requests.get(
            f"https://api.github.com/enterprises/{enterprise_name}/copilot/usage",
            headers={'Authorization': f'Bearer {github_token}'}
        )
        enterprise_response.raise_for_status()  # Raise an exception if the response contains an HTTP error status code
        enterprise_data = enterprise_response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the enterprise usage data: {e}")
        return None

    # Update Prometheus metrics for enterprise
    if isinstance(enterprise_data, list):  # Check if enterprise_data is a list
        for enterprise in enterprise_data:
            if isinstance(enterprise, dict):  # Check if enterprise is a dictionary
                for key, value in enterprise.items():
                    if key == 'breakdown' and isinstance(value, list):  # Check if key is 'breakdown' and value is a list
                        for data in value:
                            if isinstance(data, dict):  # Check if data is a dictionary
                                for sub_key, sub_value in data.items():
                                    if isinstance(sub_value, (int, float)):  # Ensure sub_value is int or float
                                        # Create a combined key using the language, editor and the metric name
                                        combined_key = f"{data['language']}_{data['editor']}_{sub_key}"
                                        enterprise_usage_gauge.labels(metric_name=combined_key).set(sub_value)
                                        #print(sub_key,sub_value)
                    elif isinstance(value, (int, float)):  # Ensure value is int or float
                        enterprise_usage_gauge.labels(metric_name=key).set(value)
        return enterprise_data
    else:
        print("No data found for enterprise usage")
        return None

def fetch_org_billing(enterprise_name, org_name, github_token):
    """Fetch organization billing and update Prometheus gauges."""
    try:
        org_response = requests.get(
            f"https://api.github.com/orgs/{org_name}/copilot/billing",
            headers={'Authorization': f'Bearer {github_token}'}
        )
        org_response.raise_for_status()  # Raise an exception if the response contains an HTTP error status code
        org_data = org_response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the organization billing data: {e}")
        return None

    # Update Prometheus metrics for organization
    if isinstance(org_data, dict):  # Check if org_data is a dictionary
        for key, value in org_data.items():
            if isinstance(value, (int, float)):  # Ensure value is int or float
                org_billing_gauge.labels(metric_name=key).set(value)
            elif isinstance(value, dict):  # Check if value is a dictionary
                for sub_key, sub_value in value.items():
                    if isinstance(sub_value, (int, float)):  # Ensure sub_value is int or float
                        # Create a combined key using the parent and child keys
                        combined_key = f"{key}_{sub_key}"
                        org_billing_gauge.labels(metric_name=combined_key).set(sub_value)
        return org_data
    else:
        print("No data found for organization billing")
        return None

def main():
    """Main function to start the server and fetch data periodically."""
    start_http_server(8000)
    github_token = get_github_token()
    enterprise_name = get_enterprise_name()
    org_name = get_org_name()
    while True:
        fetch_org_billing(enterprise_name, org_name, github_token)
        fetch_enterprise_usage(enterprise_name, org_name, github_token)
        time.sleep(60)  # fetch every 60 seconds

if __name__ == "__main__":
    main()