You are reading a data feed you have never seen before.

The directory you have been given contains exactly two files: a schema and one
example record that conforms to it. Read only those two files. You have no
network, no search, no other documents, and no access to any specification.

Produce, in this order:

1. **What this feed is.** What the records describe, in a few sentences.
2. **Analytics.** The analyses this stream supports that would be worth running,
   and for each one, why the data supports it.
3. **Combination rules.** For each quantity, state whether values may be
   compared, differenced, summed, or averaged across records, and under what
   condition. Where two values must not be combined, say so and say why.
4. **Time.** Which member establishes the time axis of the thing described, and
   how positions on that axis relate to civil time.
5. **Ambiguities.** Anything the two files leave open. For each, state plainly
   whether you are declining to decide it or guessing, and mark a guess as a
   guess.

Two rules govern the whole answer.

Do not invent facts about the domain that the two files do not establish. If
something is not in the files, either say it is not determined or mark your
answer as an assumption. Declining to answer where the files do not decide the
matter is a correct answer, not a failure.

Do not describe the files. Nobody wants an inventory of member names and types.
State what a person analysing this data would need to know and would get wrong
without you.


---

schema.json

```json
{
  "$schema": "https://json-structure.org/meta/extended/v0/#",
  "$id": "https://example.invalid/schema",
  "$uses": [
    "JSONStructureValidation"
  ],
  "name": "BuoyObservation",
  "description": "Real-time standard meteorological and oceanographic observation from an NDBC buoy, C-MAN station, or partner platform. Sourced from the NDBC latest_obs.txt composite file which is updated every five minutes. Fields cover wind, waves, pressure, temperature, dewpoint, pressure tendency, visibility, and tide. Derived from the noaa-ndbc feeder schema published in the xRegistry catalogue.",
  "type": "object",
  "properties": {
    "station_id": {
      "type": "string",
      "description": "NDBC station identifier. Five-character alphanumeric code assigned by NDBC (e.g. '41001' for deep-ocean buoys, 'BURL1' for C-MAN stations). It identifies the observing platform whose surroundings are observed."
    },
    "latitude": {
      "type": "double",
      "description": "Latitude of the observing platform in decimal degrees north. Negative values indicate southern hemisphere."
    },
    "longitude": {
      "type": "double",
      "description": "Longitude of the observing platform in decimal degrees east. Negative values indicate western hemisphere."
    },
    "timestamp": {
      "type": "datetime",
      "description": "Observation timestamp in UTC, constructed from the YYYY MM DD hh mm columns in the NDBC data. The NDBC composite file from which this record is drawn is refreshed every five minutes, so the producer is expected to publish one record per station per five-minute slot."
    },
    "wind_direction": {
      "type": "double",
      "description": "Wind direction (the direction the wind is coming from) averaged over an 8-minute period for buoys or a 2-minute period for land stations. Unit: degrees true. The reported value is the mean of the samples taken over that averaging window rather than an instantaneous reading. The window ends at the observation time, and its length is not fixed by this schema: it follows the station type, which the record does not carry, so no `supportPeriod` is declared and the extent of the period must be obtained from the NDBC station metadata."
    },
    "wind_speed": {
      "type": "double",
      "description": "Average wind speed during the observation period: 8 minutes for buoys, 2 minutes for land stations. Unit: meters per second. The reported value is the mean of the anemometer samples taken over that averaging window. The window ends at the observation time and its length follows the station type, which the record does not carry, so no `supportPeriod` is declared and the extent of the period is indeterminate from this schema alone."
    },
    "gust": {
      "type": "double",
      "description": "Peak 5-second or 8-second gust speed during the observation period. Unit: meters per second. The reported value is the greatest short-interval wind speed observed within the same averaging window that produced wind_speed, whose length follows the station type and is not fixed by this schema, so no `supportPeriod` is declared here either."
    },
    "wave_height": {
      "type": "double",
      "description": "Significant wave height — the average of the highest one-third of all wave heights during a 20-minute sampling period. Unit: meters. The summary function is the arithmetic mean, so the statistic is 'mean'; the population it is taken over is not the full set of waves in the window but the highest one-third of them, and that restriction is stated here because the statistic keyword names the function only."
    },
    "dominant_wave_period": {
      "type": "double",
      "description": "Dominant wave period — the period (in seconds) of the wave band with the maximum energy in the spectral wave analysis. Unit: seconds. The value is read off a computed energy spectrum rather than produced by applying a named summary function to a set of readings, so the derivation is 'calculated'."
    },
    "average_wave_period": {
      "type": "double",
      "description": "Average wave period of all waves during the 20-minute sampling period. Unit: seconds. The reported value is the mean of the individual wave periods measured over that window."
    },
    "mean_wave_direction": {
      "type": "double",
      "description": "Mean wave direction corresponding to the energy at the dominant wave period (DPD). Unit: degrees true. The value is obtained from the directional moments of the computed wave spectrum at a single frequency band, not by averaging a set of direction readings, so the derivation is 'calculated'."
    },
    "pressure": {
      "type": "double",
      "description": "Sea-level pressure reduced using the standard atmosphere from the station elevation. Unit: hectopascals. The barometer reading is transformed by the standard-atmosphere reduction formula before publication, so the derivation is 'calculated'."
    },
    "air_temperature": {
      "type": "double",
      "description": "Air temperature measured at the station. Unit: degrees Celsius."
    },
    "water_temperature": {
      "type": "double",
      "description": "Sea surface temperature. For buoys, measured by a hull-contact sensor near the waterline. Unit: degrees Celsius."
    },
    "dewpoint": {
      "type": "double",
      "description": "Dewpoint temperature computed from air temperature and relative humidity. Unit: degrees Celsius. Two sensor channels are combined by a deterministic psychrometric formula, so the derivation is 'calculated'."
    },
    "pressure_tendency": {
      "type": "double",
      "description": "Pressure tendency — the signed change in sea-level pressure over the preceding 3 hours. A negative value indicates falling pressure; a positive value indicates rising pressure. Unit: hectopascals. The value is a difference between two pressure readings three hours apart, so the derivation is 'calculated' and the value applies to the three-hour interval ending at the observation time."
    },
    "visibility": {
      "type": "double",
      "description": "Station visibility as reported by the observing platform. Buoy visibility sensors have a range of 0 to 1.6 nautical miles and are generally only available on C-MAN stations. Unit: nautical miles."
    },
    "tide": {
      "type": "double",
      "description": "Water level above or below Mean Lower Low Water (MLLW) at coastal and C-MAN stations. Unit: feet."
    }
  },
  "required": [
    "station_id",
    "latitude",
    "longitude",
    "timestamp"
  ],
  "additionalProperties": false
}
```

instance.json

```json
{
  "station_id": "41001",
  "latitude": 34.724,
  "longitude": -72.317,
  "timestamp": "2026-07-30T11:50:00Z",
  "wind_direction": 212.0,
  "wind_speed": 7.2,
  "gust": 9.3,
  "wave_height": 1.8,
  "dominant_wave_period": 8.3,
  "average_wave_period": 5.9,
  "mean_wave_direction": 205.0,
  "pressure": 1016.4,
  "air_temperature": 26.1,
  "water_temperature": 27.4,
  "dewpoint": 22.8,
  "pressure_tendency": -0.7
}
```
