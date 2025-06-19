from azure.identity import DefaultAzureCredential
from azure.mgmt.monitor import MonitorManagementClient
from dotenv import load_dotenv
from datetime import timedelta
from typing import Any
import os

from config.logger_config import setup_logger
logger = setup_logger("AzureMetrics")

load_dotenv()

credential = DefaultAzureCredential()
subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
if not subscription_id:
    logger.error("AZURE_SUBSCRIPTION_ID no está definido en el entorno.")
    raise ValueError("AZURE_SUBSCRIPTION_ID environment variable is not set.")

client = MonitorManagementClient(credential, subscription_id)

resource_id = os.getenv("AZURE_TRANSLATOR_RESOURCE_ID")
if not resource_id:
    logger.error("AZURE_TRANSLATOR_RESOURCE_ID no está definido en el entorno.")
    raise ValueError("AZURE_TRANSLATOR_RESOURCE_ID environment variable is not set.")

from_time = "2025-06-01T00:00:00Z"
to_time = "2025-06-18T23:59:59Z"

def get_metrics(resource_id, from_time: str, to_time: str) -> Any:
    logger.debug(f"Consultando métricas desde {from_time} hasta {to_time} para {resource_id}")
    try:
        metrics = client.metrics.list(
            resource_id,
            timespan=f"{from_time}/{to_time}",
            interval=timedelta(hours=1),
            metricnames="TextCharactersTranslated",
            aggregation="Total",
        )
        return metrics
    except Exception as e:
        logger.error(f"Error al obtener métricas de Azure: {e}")
        raise

def count_total_characters_translated():
    logger.info("Iniciando conteo de caracteres traducidos desde Azure Monitor.")
    total_characters = 0
    metrics = get_metrics(resource_id, from_time, to_time)

    for metric in metrics.value:
        logger.debug(f"Métrica: {metric.name.localized_value}")
        for timeserie in metric.timeseries:
            for data in timeserie.data:
                logger.debug(
                    f"Timestamp: {data.time_stamp}, Total: {data.total}"
                )
                if data.total is not None:
                    total_characters += data.total

    logger.info(f"Total de caracteres traducidos en el período: {total_characters}")
    return total_characters
