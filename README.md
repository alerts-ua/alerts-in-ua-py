# Introduction
The Alerts.in.ua API Client is a Python library that simplifies access to the alerts.in.ua API service. This API provides real-time information about air raid alerts and other potential threats.



# Installation
To install the Alerts.in.ua API Client, run the following command in your terminal:

```bash
pip install git+https://github.com/alerts-ua/alerts-in-ua-py.git
```



# Usage

⚠️ Before you can use this library, you need to obtain an API token by contacting api@alerts.in.ua.

Here's an example of how to use the library to get a list of active alerts:

Async:
```python
import asyncio
from alerts_in_ua import AsyncClient

async def main():
    # Initialize the client with your token
    alerts_client = AsyncClient(token="your_token")
    
    # Get the active alerts
    active_alerts = await alerts_client.get_active_alerts()
    print(active_alerts)

# Run the asynchronous function
asyncio.run(main())

```
or sync:
```python
from alerts_in_ua import Client

alerts_client = Client(token="your_token")

# Get the active alerts
active_alerts = alerts_client.get_active_alerts()
print(active_alerts)
```

# License
MIT 2023
