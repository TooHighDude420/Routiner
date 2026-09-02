# Routiner

## description
API Routines python script, will execute predifined API request and will show output and status

run once to generate the Routines and Output folder

then put your routines in seperate json files like this:

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