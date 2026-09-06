# Routiner

## Description
API Routines python script, will execute predifined API request and will show output and status

## Usage
### Run
```bash 
python main.py run <name> | -a | --all
```
Run a routine by name or run all routines with the -a flag

### List
```bash
python main.py list
```
List all routine files in the routines folder without the .json

## Input/Output
### Input example

``` JSON
{
  "routine": "check-weather",
  "steps": [
    {
      "request": {
        "method": "GET",
        "url": "https://api.open-meteo.com/v1/forecast",
        "params": {
          "latitude": 52.09,
          "longitude": 5.89,
          "current": "temperature_2m"
        }
      }
    }
  ]
}
```
This is a simple functional single step Example. Where a GET request gets sent to open-meteo with paramaters

### Output example
```
╭───────────────────── check-weather ─────────────────────╮
│ ╭────────────────────── Request ──────────────────────╮ │
│ │ STATUS       SUCESS                                 │ │
│ │ STATUS CODE  200                                    │ │
│ │ URL          https://api.open-meteo.com/v1/forecast │ │
│ ╰─────────────────────────────────────────────────────╯ │
│ ╭────────────────── Response ──────────────────╮        │
│ │ {                                            │        │
│ │   "latitude": 52.096,                        │        │
│ │   "longitude": 5.8869996,                    │        │
│ │   "generationtime_ms": 0.026106834411621094, │        │
│ │   "utc_offset_seconds": 0,                   │        │
│ │   "timezone": "GMT",                         │        │
│ │   "timezone_abbreviation": "GMT",            │        │
│ │   "elevation": 57.0,                         │        │
│ │   "current_units": {                         │        │
│ │     "time": "iso8601",                       │        │
│ │     "interval": "seconds",                   │        │
│ │     "temperature_2m": "°C"                   │        │
│ │   },                                         │        │
│ │   "current": {                               │        │
│ │     "time": "2026-09-06T08:45",              │        │
│ │     "interval": 900,                         │        │
│ │     "temperature_2m": 17.1                   │        │
│ │   }                                          │        │
│ │ }                                            │        │
│ ╰──────────────────────────────────────────────╯        │
╰─────────────────────────────────────────────────────────╯
```
This is a example of how a run gets logged if you use the example shown in the previous step

## Routine defenitions
### The base
``` JSON
{
  "routine": ...,
  "steps": [
    {
      "request": {
        "method": ...,
        "url": ...,
        "params": {
          ...
        }
      }
    }
  ]
}
```
Every routine needs alteast these keys to work

### Expansions
```json
display: [
  ...
]
```
will filter the response with the defined keys

## Planned features
* Multistep support
* assert / expect
* better error handeling
* run options
  * run until
  * run while
  * run x times
* more expansions
* silent mode
* terminal output mode