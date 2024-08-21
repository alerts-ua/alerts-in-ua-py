# Introduction
The Alerts.in.ua API Client is a Python library that simplifies access to the alerts.in.ua API service. It provides real-time information about air raid alerts and other potential threats.


## Contents
* [Instalation](#installation)
* [Usage](#usage)
  * [Define Client](#define-client)
  * [Get Active Alerts Asynchronous](#get-active-alerts-asynchronous)
  * [Get Active Alerts Synchronous](#get-active-alerts-synchronous)
  * [Get Air Raid status for IOT](#get-air-raid-status)
* [Alerts](#alerts)
  * [Properties and Attributes](#properties-and-attributes)
  * [Methods](#properties-and-attributes)

## Installation
To install the Alerts.in.ua API Client, run the following command in your terminal:

```bash
pip install alerts_in_ua
```



## Usage

⚠️ Before you can use this library, you need to obtain an API token by submitting an [API request form](https://alerts.in.ua/api-request).

Here's an basic example of how to use the library to get a list of active alerts:

#### Define Client
```python
from alerts_in_ua import Client

# Initialize the client with your token
client = Client(token="your_token")
# or set your token as environment variable AIU_API_TOKEN
client = Client()
```

#### Get Active Alerts Asynchronous
```python
import asyncio

# there client definition

async def main():
    # Get the active alerts_details
    active_alerts = await client.async_get_active()
    print(active_alerts)

# Run the asynchronous function
asyncio.run(main())

```
#### Get Active Alerts Synchronous
```python
# there client definition

# Get the active alerts_details
active_alerts = client.get_active()
print(active_alerts)
```

#### Get Air Raid status
You can get air raid status for target location or all locatons
The methods bellow returns **AirRaidOblastStatus** or **AirRaidOblastStatuses**
```python
AirRaidOblastStatus - Single air raid status
AirRaidOblastStatuses - List[AirRaidOblastStatus]
```
```python
# # For target location
# Synchronous
client.get_air_raid(<uid|location_title>)  # -> AirRaidOblastStatus

# Asynchronous
await client.async_get_air_raid(<uid|location_title>)  # -> AirRaidOblastStatus

# # For all locations
# Synchronous
client.get_air_raids()  # -> AirRaidOblastStatuses

# Asynchronous
await client.async_get_air_raids()  # -> AirRaidOblastStatuses
```
#### You also can filter AirRaidOblastStatuses by multiple criteria

```python
# AirRaidOblastStatuses.filter(self, *criteria: FilterType) -> List[AirRaidOblastStatus]
AirRaidOblastStatuses = statuses.filter(
  ('location_uid', 16)
) 
```

## Alerts

Alerts class is a collection of alerts and provides various methods to filter and access these alerts.

When user call `client.active_alerts()` it returns `Alerts` class.

### Properties and Attributes

```python
# Last tome of update
last_updated = Alerts.last_updated_at  # -> Optional[datetime]

# Meta
meta = Alerts.meta  # -> Optional[AlertsMeta]

# Meta
alerts = Alerts.alerts  # -> Optional[List[AlertDetails]]
```

### Methods

#### Alerts.filter(self, *criteria: FilterType) -> List[AlertDetails]
This method filters the alerts based on the given parameters.
You can apply multiple filters at a same time
```python
from alerts_in_ua.alerts import FilterCriterion

filtered_alerts = alerts.filter(
    FilterCriterion('location_uid', 16),
    ('location_oblast', 'Донецька область'),
    ('alert_type','air_raid')
)
```
In this example, filtered_alerts will contain all the air raid alerts that have the location oblast as 'Донецька область'.

#### def iter_alerts(self) -> Iterator[AlertDetails]:

```python
# Get Alert.alerts Iterator
alerts.iter_alerts() -> Iterator[AlertDetails]
```



# License
MIT 2023
