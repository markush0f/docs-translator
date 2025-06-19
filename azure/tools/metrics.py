from azure.identity import DefaultAzureCredential
from azure.mgmt.monitor import MonitorManagementClient

# from azure.mgmt.monitor.models import TimeRange
from dotenv import load_dotenv
import os

load_dotenv()
credential = DefaultAzureCredential()
subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
if not subscription_id:
    raise ValueError("AZURE_SUBSCRIPTION_ID environment variable is not set.")

client = MonitorManagementClient(credential, subscription_id)

resource_id = os.getenv("AZURE_TRANSLATOR_RESOURCE_ID")
if not resource_id:
    raise ValueError("AZURE_TRANSLATOR_RESOURCE_ID environment variable is not set.")

from_time = "2025-06-01T00:00:00Z"
to_time = "2025-06-18T23:59:59Z"

from datetime import timedelta


from typing import Any

def get_metrics(
    resource_id, from_time: str, to_time: str
) -> Any:
    metrics = client.metrics.list(
        resource_id,
        timespan=f"{from_time}/{to_time}",
        interval=timedelta(hours=1),
        metricnames="TextCharactersTranslated",
        aggregation="Total",
    )
    return metrics


def count_total_characters_translated():
    metrics = get_metrics(resource_id, from_time, to_time)
    total_characters = 0
    for metric in metrics.value:
        for timeserie in metric.timeseries:
            print(f"Metric: {metric.name.localized_value}")
            for data in timeserie.data:
                print(
                    f"Timestamp: {data.time_stamp}, Total Characters Processed: {data.total}"
                )
                if data.total is not None:
                    total_characters += data.total

    print(f"Total Characters Processed: {total_characters}")
    return total_characters
