### Python APM Test application
This repo provides test code for setting a local python application that is instrumented with New Relic Python APM agent.

### Steps for testing setup
1. Install all requirements `pip install -r requirements.txt`
2. Add environment variable for local testing
    1. Use `.env-example` file to create a `.env` file
    2. Modify the value of `ENVIRONMENT` for local testing
    3. The APM App will automatically load the value for environment variable when the app is run
3. Modify Line 44 in newrelic.ini for local testing
4. Run the app locally by executing the following command:
```
newrelic-admin run-program uvicorn main:app
```
