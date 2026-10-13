# Alerts.in.ua Python Client

A comprehensive Python library for accessing the [alerts.in.ua](https://alerts.in.ua) API service. Provides real-time information about air raid alerts and other potential threats across Ukraine.

## Features

- 🚨 **Real-time alerts** - Get active air raid and other security alerts
- 🟡 **Alert levels and threats** - Red / yellow alert level and the specific threats (drones, missiles, ...) behind each alert
- 📍 **Location-based filtering** - Filter by oblasts, raions, hromadas, and cities
- 🎯 **Air raid statuses** - Efficient bulk status retrieval for all regions, with red / yellow levels via the v2 IoT API
- ⚡ **Async support** - Both synchronous and asynchronous clients
- 🔄 **Caching** - Built-in request caching for better performance
- 🛡️ **Error handling** - Comprehensive error handling and rate limiting
- 📊 **Data containers** - Rich data objects with filtering and lookup methods

## Installation

```bash
pip install alerts_in_ua
```

## Quick Start

⚠️ **API Token Required**: You need to obtain an API token by submitting an [API request form](https://alerts.in.ua/api-request).

### Basic Usage

```python
from alerts_in_ua import Client

# Initialize client
client = Client("your_api_token")

# Get detailed active alerts
alerts = client.get_active_alerts()

# Red / yellow alert levels and open threats
for alert in alerts.get_red_alerts():
    print(alert.location_title, [threat.threat_type for threat in alert.threats])

# Get air raid statuses for all regions
statuses = client.get_air_raid_alert_statuses()

# Check specific region
kyiv_status = statuses.get_status(14)  # Київська область
if kyiv_status and kyiv_status.status == 'active':
    print(f"Alert in {kyiv_status.location_title}!")
```

### Async Usage

```python
import asyncio
from alerts_in_ua import AsyncClient

async def main():
    client = AsyncClient("your_api_token")
    
    # Get detailed alerts and statuses
    alerts = await client.get_active_alerts()
    statuses = await client.get_air_raid_alert_statuses()
    
    return alerts, statuses

# Run async function
alerts, statuses = asyncio.run(main())
```

## API Reference

### Client Methods

#### Active Alerts

##### `get_active_alerts(use_cache=True) -> Alerts`
Get all currently active alerts across Ukraine.

**Parameters:**
- `use_cache` (bool): Use cached data if available (default: True)

**Returns:**
- `Alerts`: Container with all active alerts

**Example:**
```python
alerts = client.get_active_alerts()
print(f"Total active alerts: {len(alerts)}")

# Iterate through alerts
for alert in alerts:
    print(f"{alert.location_title}: {alert.alert_type} ({alert.alert_level})")
```

#### Air Raid Alert Statuses

##### `get_air_raid_alert_statuses(use_cache=True, api_version=1) -> AirRaidAlertStatuses`
Get air raid alert statuses for all regions using a single efficient API call.

**Parameters:**
- `use_cache` (bool): Use cached data if available (default: True)
- `api_version` (int): IoT API version, `1` (default) or `2`. With `2`, active statuses also carry `alert_level` (`'red'` / `'yellow'`), see [IoT API v2](#iot-api-v2-alert-levels)

**Returns:**
- `AirRaidAlertStatuses`: Container with all air raid alert statuses

**Example:**
```python
statuses = client.get_air_raid_alert_statuses()

# Get specific region status
kyiv_status = statuses.get_status(14)  # Київська область
if kyiv_status:
    print(f"Kyiv status: {kyiv_status.status}")

# Filter by status type
active_alerts = statuses.get_active_alert_statuses()
print(f"Active alerts: {len(active_alerts)}")

# Get all statuses
for status in statuses:
    print(f"{status.location_title}: {status.status}")

# v2: red / yellow alert levels
statuses = client.get_air_raid_alert_statuses(api_version=2)
red = statuses.get_red_alert_statuses()
yellow = statuses.get_yellow_alert_statuses()
```

#### Individual Region Status

##### `get_air_raid_alert_status(oblast_uid_or_location_title, oblast_level_only=False, use_cache=True, api_version=1) -> AirRaidAlertOblastStatus`
Get air raid alert status for a specific region.

**Parameters:**
- `oblast_uid_or_location_title` (Union[int, str]): UID or location title
- `oblast_level_only` (bool): Return oblast-level data only (default: False)
- `use_cache` (bool): Use cached data if available (default: True)
- `api_version` (int): IoT API version, `1` (default) or `2`

**Returns:**
- `AirRaidAlertOblastStatus`: Status object for the specified region

**Example:**
```python
# By UID
status = client.get_air_raid_alert_status(14)  # Київська область

# By location title
status = client.get_air_raid_alert_status("Київська область")

print(f"Status: {status.status}")
print(f"Location: {status.location_title}")

# v2: alert level
status = client.get_air_raid_alert_status(31, api_version=2)  # м. Київ
if status.is_red():
    print("Red level alert in Kyiv")
```

#### Oblast-Level Statuses

##### `get_air_raid_alert_statuses_by_oblast(oblast_level_only=False, use_cache=True, api_version=1) -> AirRaidAlertOblastStatuses`
Get air raid alert statuses for all oblasts.

**Parameters:**
- `oblast_level_only` (bool): Return oblast-level data only (default: False)
- `use_cache` (bool): Use cached data if available (default: True)
- `api_version` (int): IoT API version, `1` (default) or `2`

**Returns:**
- `AirRaidAlertOblastStatuses`: Container with oblast statuses

**Example:**
```python
oblast_statuses = client.get_air_raid_alert_statuses_by_oblast()

for status in oblast_statuses:
    print(f"{status.location_title}: {status.status}")

# v2: oblasts with red / yellow alerts
oblast_statuses = client.get_air_raid_alert_statuses_by_oblast(api_version=2)
red_oblasts = oblast_statuses.get_red_alert_oblasts()
yellow_oblasts = oblast_statuses.get_yellow_alert_oblasts()
```

#### Historical Alerts

##### `get_alerts_history(oblast_uid_or_location_title, period='week_ago', use_cache=True) -> Alerts`
Get historical alerts for a specific region and time period.

**Parameters:**
- `oblast_uid_or_location_title` (Union[int, str]): UID or location title
- `period` (str): Time period ('week_ago', 'month_ago', etc.)
- `use_cache` (bool): Use cached data if available (default: True)

**Returns:**
- `Alerts`: Container with historical alerts

**Example:**
```python
# Get week-old alerts for Kyiv
kyiv_history = client.get_alerts_history("Київська область", "week_ago")

for alert in kyiv_history:
    print(f"{alert.location_title}: {alert.alert_type} at {alert.started_at}")
```

### Data Containers

#### Alerts Container

The `Alerts` class provides rich filtering and access methods for alert collections.

**Filtering Methods:**

```python
alerts = client.get_active_alerts()

# Filter by multiple criteria
filtered = alerts.filter('location_oblast', 'Донецька область', 'alert_type', 'air_raid')

# Filter by location title
kyiv_alerts = alerts.get_alerts_by_location_title('м. Київ')

# Filter by alert type
air_raid_alerts = alerts.get_air_raid_alerts()
artillery_alerts = alerts.get_artillery_shelling_alerts()
nuclear_alerts = alerts.get_nuclear_alerts()
chemical_alerts = alerts.get_chemical_alerts()
urban_fights_alerts = alerts.get_urban_fights_alerts()

# Filter by location type
oblast_alerts = alerts.get_oblast_alerts()
raion_alerts = alerts.get_raion_alerts()
hromada_alerts = alerts.get_hromada_alerts()
city_alerts = alerts.get_city_alerts()

# Filter by specific criteria
donetsk_alerts = alerts.get_alerts_by_oblast('Донецька область')
artillery_by_type = alerts.get_alerts_by_alert_type('artillery_shelling')
raion_by_type = alerts.get_alerts_by_location_type('raion')
by_uid = alerts.get_alerts_by_location_uid('123456')

# Filter by alert level ('red' / 'yellow')
red_alerts = alerts.get_red_alerts()
yellow_alerts = alerts.get_yellow_alerts()
yellow_by_level = alerts.get_alerts_by_alert_level('yellow')
red_air_raids = alerts.filter('alert_level', 'red', 'alert_type', 'air_raid')

# Alerts with a specific open threat
drone_alerts = alerts.get_alerts_with_threat_type('drones')
```

**Utility Methods:**

```python
# Get all alerts
all_alerts = alerts.get_all_alerts()

# Get metadata
last_updated = alerts.get_last_updated_at()  # datetime object
disclaimer = alerts.get_disclaimer()  # str

# Iteration
for alert in alerts:
    print(alert)
```

#### AirRaidAlertStatuses Container

The `AirRaidAlertStatuses` class provides efficient access to air raid status data.

**Lookup Methods:**

```python
statuses = client.get_air_raid_alert_statuses()

# Get status by UID (fast cached lookup)
kyiv_status = statuses.get_status(14)  # Київська область
kyiv_city_status = statuses.get_status(31)  # м. Київ

# Get status by location title
kyiv_status = statuses.get_status("Київська область")
```

**Filtering Methods:**

```python
# Filter by status type
active_alerts = statuses.get_active_alert_statuses()
partly_alerts = statuses.get_partly_active_alert_statuses()
no_alerts = statuses.get_no_alert_statuses()

# Custom filtering
custom_filtered = statuses.filter_by_status('active')

# Filter by alert level (api_version=2 only)
red_alerts = statuses.get_red_alert_statuses()
yellow_alerts = statuses.get_yellow_alert_statuses()
red_alerts = statuses.filter_by_alert_level('red')
```

**Container Features:**

```python
# Iteration
for status in statuses:
    print(f"{status.location_title}: {status.status}")

# Length
print(f"Total regions: {len(statuses)}")

# Indexing
first_status = statuses[0]
kyiv_status = statuses.get_status(14)
```

### Data Objects

#### Alert Object

Each alert contains:

- `id` (int): Alert ID
- `location_title` (str): Location name
- `location_title_en` (str): Location name in English
- `alert_type` (str): Type of alert ('air_raid', 'artillery_shelling', etc.)
- `alert_level` (str): Alert level ('red', 'yellow')
- `threats` (List[Threat]): Threats currently open within the alert (empty list if none)
- `location_type` (str): Type of location ('oblast', 'raion', 'hromada', 'city')
- `location_oblast` (str): Oblast name
- `location_oblast_uid` (str): Oblast UID
- `location_raion` (str): Raion name
- `location_uid` (str): Location UID
- `started_at` (datetime): When the alert started
- `finished_at` (datetime): When the alert ended (if applicable)
- `updated_at` (datetime): When the alert was last updated
- `notes` (str): Notes
- `country` (str): Country

Methods: `is_finished()`, `is_red()`, `is_yellow()`, `has_threats()`, `get_threats_by_type(threat_type)`.

#### Threat Object

Each item of `alert.threats` contains:

- `threat_type` (str): Type of threat ('tactic_aircraft_activity', 'strategic_aircraft_activity', 'mig31k_departure', 'ballistic_missiles', 'cruise_missiles', 'unspecified_missiles', 'drones', 'guided_aerial_bombs', 'air_defense', 'unknown')
- `level` (str): Level of this threat ('red', 'yellow')
- `started_at` (datetime): When the threat started
- `source_message` (str): Original wording from the source, or `None`

Methods: `is_red()`, `is_yellow()`.

```python
for alert in client.get_active_alerts():
    if alert.is_yellow():
        print(f"{alert.location_title} is on yellow level")
    for threat in alert.get_threats_by_type('drones'):
        print(f"  drones since {threat.started_at}: {threat.source_message}")
```

A threat's level is independent of its alert's level: a `yellow` alert can carry a `red` threat.
Alerts from `get_alerts_history()` have `alert_level` but no `threats`, since threats only list what is open right now.

#### AirRaidAlertStatus Object

Each status contains:

- `location_title` (str): Location name
- `status` (str): Alert status ('no_alert', 'active', 'partly')
- `uid` (int): Location UID
- `alert_level` (Optional[str]): `'red'` or `'yellow'` for active alerts fetched with `api_version=2`, otherwise `None`
- `is_red()` / `is_yellow()`: level checks

#### AirRaidAlertOblastStatus Object

Each oblast status contains:

- `location_title` (str): Oblast name
- `status` (str): Alert status ('no_alert', 'active', 'partly')
- `alert_level` (Optional[str]): `'red'` or `'yellow'` for active alerts fetched with `api_version=2`, otherwise `None`
- `is_active_on_all_oblast()` / `is_partly_active()` / `is_no_alert()` / `is_red()` / `is_yellow()`: status checks

`AirRaidAlertOblastStatuses` (from `get_air_raid_alert_statuses_by_oblast`) supports iteration, `len()`, `get_active_alert_oblasts()`, `get_partly_active_alert_oblasts()`, `get_no_alert_oblasts()`, `get_red_alert_oblasts()` and `get_yellow_alert_oblasts()`.

### Status Values

The API uses character codes that are mapped to meaningful values:

- `N` → `no_alert` (Немає тривоги)
- `A` → `active` (Активна тривога), v1
- `R` → `active`, `alert_level='red'` (Активна тривога, червоний рівень), v2
- `Y` → `active`, `alert_level='yellow'` (Активна тривога, жовтий рівень), v2
- `P` → `partly` (Часткова тривога)
- `(space)` → `undefined` (Немає даних для регіону) - automatically filtered out

### IoT API v2 (alert levels)

The IoT methods use the v1 endpoints by default. Pass `api_version=2` to use `/v2/iot/...`, which splits an active alert into red (`R`) and yellow (`Y`) levels. `status` stays `'active'` for both, so code written for v1 keeps working, and `alert_level` tells the levels apart. In `repr`, yellow-level active alerts show as 🟠 (🔴 red, 🟡 partly, 🟢 no alert). v1 and v2 responses are cached separately. Any other `api_version` raises `InvalidParameterException`.

```python
statuses = client.get_air_raid_alert_statuses(api_version=2)
for status in statuses.get_active_alert_statuses():
    print(status.location_title, status.alert_level)  # 'red' or 'yellow'
```

### Error Handling

The library provides comprehensive error handling:

```python
from alerts_in_ua import Client, UnauthorizedError, RateLimitError, ApiError

try:
    client = Client("invalid_token")
    alerts = client.get_active_alerts()
except UnauthorizedError:
    print("Invalid API token")
except RateLimitError:
    print("Rate limit exceeded")
except ApiError as e:
    print(f"API error: {e}")
```

### Configuration

#### Timeout Settings

```python
# Default timeout is 5 seconds
client = Client("your_token")

# You can modify timeout if needed
client.REQUEST_TIMEOUT = 10
```

#### Caching

```python
# Use cache (default)
alerts = client.get_active_alerts(use_cache=True)

# Skip cache
alerts = client.get_active_alerts(use_cache=False)
```

### Advanced Examples

#### Monitor Multiple Regions

```python
def monitor_regions(client, region_uids):
    statuses = client.get_air_raid_alert_statuses()
    
    for uid in region_uids:
        status = statuses.get_status(uid)
        if status and status.status == 'active':
            print(f"🚨 ALERT: {status.location_title}")
        elif status:
            print(f"✅ Clear: {status.location_title}")

# Monitor key regions
key_regions = [14, 31, 8, 9]  # Київська область, м. Київ, Волинська область, Дніпропетровська область
monitor_regions(client, key_regions)
```

#### Async Monitoring

```python
import asyncio
from alerts_in_ua import AsyncClient

async def monitor_alerts():
    client = AsyncClient("your_token")
    
    while True:
        try:
            alerts = await client.get_active_alerts()
            statuses = await client.get_air_raid_alert_statuses()
            
            print(f"Active alerts: {len(alerts)}")
            print(f"Active air raid regions: {len(statuses.get_active_alert_statuses())}")
            
            await asyncio.sleep(60)  # Check every minute
            
        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(30)

# Run monitoring
asyncio.run(monitor_alerts())
```

#### Historical Analysis

```python
def analyze_alert_history(client, location, days=7):
    history = client.get_alerts_history(location, "week_ago")
    
    alert_types = {}
    for alert in history:
        alert_type = alert.alert_type
        alert_types[alert_type] = alert_types.get(alert_type, 0) + 1
    
    print(f"Alert history for {location}:")
    for alert_type, count in alert_types.items():
        print(f"  {alert_type}: {count} alerts")

analyze_alert_history(client, "Київська область")
```

## Running Tests

```bash
python -m unittest discover -s tests -t .
```

Live tests against the API are skipped unless a token is provided:

```bash
ALERTS_IN_UA_TOKEN=your_token python -m unittest tests.test_live
```

## Changelog

### 0.4.0
- `Alert.alert_level` (`red` / `yellow`) with `is_red()` / `is_yellow()`.
- `Alert.threats`: list of `Threat` objects (`threat_type`, `level`, `started_at`, `source_message`), plus `has_threats()` and `get_threats_by_type()`.
- `Alerts.get_alerts_by_alert_level()`, `get_red_alerts()`, `get_yellow_alerts()`, `get_alerts_with_threat_type()`.
- `Alert.location_title_en` and `Alert.country`.
- IoT API v2: `api_version=2` on `get_air_raid_alert_statuses()`, `get_air_raid_alert_status()` and `get_air_raid_alert_statuses_by_oblast()` (sync and async). Statuses gain `alert_level` and `is_red()` / `is_yellow()`; containers gain `get_red_alert_statuses()` / `get_yellow_alert_statuses()` / `filter_by_alert_level()` and `get_red_alert_oblasts()` / `get_yellow_alert_oblasts()`. v1 remains the default.
- `len()` on `AirRaidAlertOblastStatuses`.
- `Threat`, `InvalidParameterException` and the error classes are exported from `alerts_in_ua`.
- Unit tests and opt-in live API tests.

## License

MIT License - see LICENSE file for details.

## Support

For API access and support, contact [api@alerts.in.ua](mailto:api@alerts.in.ua) or visit [alerts.in.ua](https://alerts.in.ua).
