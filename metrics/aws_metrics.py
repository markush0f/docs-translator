import boto3
from datetime import date
from config.logger_config import setup_logger

logger = setup_logger("Metrics")

client = boto3.client("ce")


def get_amazon_translate_usage():
    today = date.today()
    first_day = today.replace(day=1)

    logger.debug(
        f"Consultando uso de Amazon Translate desde {first_day} hasta {today}."
    )

    try:
        response = client.get_cost_and_usage(
            TimePeriod={
                "Start": first_day.isoformat(),
                "End": today.isoformat(),
            },
            Granularity="MONTHLY",
            Metrics=["UsageQuantity"],
            Filter={"Dimensions": {"Key": "Service", "Values": ["Amazon Translate"]}},
        )

        results = response.get("ResultsByTime", [])
        if not results or not results[0]["Total"]:
            logger.info("No hay datos disponibles aún desde Cost Explorer.")
            return "⏳ Aún no hay datos disponibles desde Cost Explorer."

        usage = results[0]["Total"]["UsageQuantity"]["Amount"]
        logger.info(f"Uso actual de Amazon Translate: {usage} caracteres.")
        return f"🔤 Amazon Translate - caracteres traducidos este mes: {usage}"

    except Exception as e:
        logger.error(f"Error al consultar uso de Amazon Translate: {e}")
        return "❌ Error al consultar métricas de Cost Explorer."
