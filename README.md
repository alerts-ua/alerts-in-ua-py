# Introduction
The Alerts.in.ua API Client is a Python library that simplifies access to the alerts.in.ua API service. It provides real-time information about air raid alerts and other potential threats.



# Installation
To install the Alerts.in.ua API Client, run the following command in your terminal:

```bash
pip install alerts_in_ua
```



# Usage

⚠️ Before you can use this library, you need to obtain an API token by contacting api@alerts.in.ua.

Here's an basic example of how to use the library to get a list of active alerts:

Async:
```python
import asyncio
from alerts_in_ua import AsyncClient as AsyncAlertsClient

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
from alerts_in_ua import Client as AlertsClient

alerts_client = Client(token="your_token")

# Get the active alerts
active_alerts = alerts_client.get_active_alerts()
print(active_alerts)
```

# Alerts 

`get_active_alerts()` returns Alerts a collection of alerts and provides various methods to filter and access these alerts.

### filter(*args: str) -> List[Alert]
This method filters the alerts based on the given parameters.

```python
filtered_alerts = active_alerts.filter('location_oblast', 'Донецька область','alert_type','air_raid)
```
In this example, filtered_alerts will contain all the air raid alerts that have the location oblast as 'Донецька область'.

### get_oblast_alerts() -> List[Alert]
This method returns all the alerts that are of alert type 'oblast'.

```python
oblast_alerts = active_alerts.get_oblast_alerts()
```

### get_raion_alerts() -> List[Alert]
This method returns all the alerts that are of alert type 'raion'.
```python
raion_alerts = active_alerts.get_raion_alerts()
```

### get_hromada_alerts() -> List[Alert]
This method returns all the alerts that are of alert type 'hromada'.
```python
hromada_alerts = active_alerts.get_hromada_alerts()
```

### get_city_alerts() -> List[Alert]
This method returns all the alerts that are of alert type 'city'.

```python
city_alerts = active_alerts.get_city_alerts()
```

### get_alerts_by_alert_type(alert_type: str) -> List[Alert]
This method returns all the alerts that are of the given alert type.

```python
artillery_shelling_alerts = active_alerts.get_alerts_by_alert_type('artillery_shelling')
```

### get_alerts_by_location_type(location_type: str) -> List[Alert]
This method returns all the alerts that are of the given location type.

```python
urban_location_alerts = active_alerts.get_alerts_by_location_type('urban_fights')
```

### get_alerts_by_oblast(oblast_title: str) -> List[Alert]
This method returns all the alerts that are of the given oblast title.

```python
donetsk_oblast_alerts = active_alerts.get_alerts_by_oblast('Донецька область')
```

### get_alerts_by_location_uid(location_uid: str) -> List[Alert]
This method returns all the alerts that have the given location uid.
```python
location_uid_alerts = active_alerts.get_alerts_by_location_uid('123456')
```

### get_air_raid_alerts() -> List[Alert]
This method returns all the alerts that are of alert type 'air_raid'.
```python 
air_raid_alerts = active_alerts.get_air_raid_alerts()
```

### get_artillery_shelling_alerts() -> List[Alert]
This method returns all the alerts that are of alert type 'artillery_shelling'.
```python 
artillery_shelling_alerts = active_alerts.get_artillery_shelling_alerts()
```

### get_urban_fights_alerts() -> List[Alert]
This method returns all the alerts that are of alert type 'urban_fights'.
```python 
urban_fights_alerts = active_alerts.get_urban_fights_alerts()
```

### get_nuclear_alerts() -> List[Alert]
This method returns all the alerts that are of alert type 'nuclear'.
```python 
nuclear_alerts = active_alerts.get_nuclear_alerts()
```

### get_chemical_alerts() -> List[Alert]
This method returns all the alerts that are of alert type 'chemical'.
```python 
chemical_alerts = active_alerts.get_chemical_alerts()
```

### get_all_alerts() -> List[Alert]
This method returns all alerts.
```python 
all_alerts = active_alerts.get_all_alerts()
```
or you can use shortcut:
```python 
for alert in active_alerts.get_all_alerts():
    print(alert)
```
### get_last_updated_at() -> datetime.datetime
This method returns the datetime object representing the time when the alert information was last updated (Kyiv timezone).
```python
last_updated_at = alerts.get_last_updated_at()
```

### get_disclaimer() -> str
This method returns the disclaimer associated with the alert information.
```python
disclaimer = alerts.get_disclaimer()
```



# License
MIT 2023
