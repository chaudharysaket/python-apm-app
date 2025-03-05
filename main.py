import newrelic.agent
from fastapi import FastAPI
import httpx
import uvicorn
import os
import uuid
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

ENVIRONMENT = os.getenv('ENVIRONMENT', 'local')
newrelic.agent.initialize(config_file='newrelic.ini', environment=ENVIRONMENT)
app = FastAPI()

@newrelic.agent.transaction_name('custom_transaction_name')
@app.get("/")
async def root():
    newrelic.agent.add_custom_attribute('custom_attr_saket_test_local_apm_app', 'example_value')
    newrelic.agent.record_custom_metric('Custom/Example', 1)
    metric_data = {
        'MetricName': 'NRCustomMetricTesting',
        'Dimensions': [
            {
                'Name': 'DummyDimension',
                'Value': 'DummyValue'
            },
        ],
        'Unit': 'Milliseconds',
        'Value': 10045
    }
    eventData =  {
        "id": str(uuid.uuid4()),
        "message": "This is test from local Python APM",
        "ingest_source": "local Python APM",
        "timestamp": datetime.now(),
    }
    newrelic.agent.record_custom_metric("Supportability/Python/ML/OpenAI/v1.0", 1)
    newrelic.agent.record_custom_metric("Custom/testCustomMetricAPMLocal", 131)
    newrelic.agent.record_custom_metric("Custom/testCustomMetricAPMLocalDuplicate", 123)

    newrelic.agent.record_custom_event("APMLocalCustomEventTest", eventData, newrelic.agent.application())

    return {"message": "Hello World"}
@app.get("/result")
async def invoke_lambda():
    with newrelic.agent.BackgroundTask(application=newrelic.agent.application(), name='invoke_lambda'):
        async with httpx.AsyncClient() as client:
            response = await client.get('https://google.com')
    return response.text

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    with newrelic.agent.BackgroundTask():
        result = f"Item ID: {item_id}"
    return {"item": result}

@app.get("/error")
async def trigger_error():
    try:
        1 / 0
    except Exception as e:
        newrelic.agent.notice_error()
        raise

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True
    )