# Characteristics annotations on real feed schemas

Fifteen samples derived from JSON Structure schemas published by live open-data
feeds. The schemas were taken from the xRegistry documents in the
[real-time-sources](https://github.com/clemensv/real-time-sources) feeders, then
annotated with the keywords defined by
[JSON Structure: Characteristics](../../draft-vasters-json-structure-characteristics.md).

They differ from the [teaching samples](../) one directory up: those are written
to isolate one part of the annotation model each, whereas these start from a
schema somebody else wrote for a real event stream and ask what the annotations
have to say about it. Every one covers a different domain and a different
publisher.

Each directory holds a `schema.struct.json` and an `example.json` instance that
conforms to it. The header is the same as for the teaching samples:

```json
{
  "$schema": "https://json-structure.org/meta/characteristics/v0/#",
  "$id": "https://schemas.example.org/characteristics/real-world/01-ais-vessel-position",
  "$uses": ["JSONStructureCharacteristics"]
}
```

## Samples

| # | Directory | Source | What it shows |
|---|---|---|---|
| 01 | [`01-ais-vessel-position`](01-ais-vessel-position/) | aisstream.io `StandardClassBPositionReport` | A moving vessel as the feature of interest. Event-driven `cadence`, `phenomenonTime` against `ingestionTime`, measured kinematics, and an EPSG:4326 binding. |
| 02 | [`02-marine-buoy-observation`](02-marine-buoy-observation/) | NOAA NDBC `BuoyObservation` | The `derivation`/`statistic` pairing across a real sensor suite: 8-minute mean wind, peak gust, computed pressure tendency. `phenomenonTimeRelation` separates the instantaneous channels from the windowed ones. |
| 03 | [`03-aerodrome-metar`](03-aerodrome-metar/) | AviationWeather.gov `Metar` | A routine hourly aerodrome report. `phenomenonTime` against `resultTime`, report type as `status`, and a horizontal and a vertical coordinate reference system on two nodes. |
| 04 | [`04-lightning-stroke`](04-lightning-stroke/) | Blitzortung `LightningStroke` | A geolocated instant. The position is a `calculated` time-of-arrival solution qualified by an `estimated` accuracy and by the contributing detector set. |
| 05 | [`05-earthquake-report`](05-earthquake-report/) | JMA Bosai `EarthquakeReport` | Three temporal positions on one bulletin: origin time, issue time, distribution handover. Computed hypocentre and magnitude, with the maximum reported intensity as a `maximum` statistic. |
| 06 | [`06-solar-xray-flare`](06-solar-xray-flare/) | NOAA SWPC GOES `XrayFlare` | A non-terrestrial observation. Flattened `phenomenonTimeStart`/`phenomenonTimeEnd` over the flare, peak flux as a `maximum`, and an explicit temporal reference system in place of any spatial one. |
| 07 | [`07-grid-carbon-intensity`](07-grid-carbon-intensity/) | National Grid ESO `RegionalIntensity` | Forecast against outturn for one settlement period: `modeled` beside `calculated`, `forecastIssueTime` and `forecastLeadDuration`, and a half-hourly fixed cadence. |
| 08 | [`08-public-power-generation`](08-public-power-generation/) | Energy-Charts `PublicPower` | Interval-integrated energy. Per-production-type `mean` power over the quarter-hourly market time unit, contrasted with a `sum` over metered load. |
| 09 | [`09-orbit-mean-elements`](09-orbit-mean-elements/) | CelesTrak `OrbitMeanElements` | The one sample whose temporal reference system is not civil time. The TLE epoch is modelled as a meta-type and bound through `position` and `referenceRole`; the elements are `modeled`, not measured. |
| 10 | [`10-transit-vehicle-position`](10-transit-vehicle-position/) | SIRI `VehiclePosition` | `scheduledTime` against `actualTime`, which is what a real-time transit feed exists to carry, with the position fix bound to CRS84. |
| 11 | [`11-route-travel-time`](11-route-travel-time/) | NDW `TravelTimeObservation` and `RouteMeasurementSite` | `linearReferenceSystem` of kind `lrs-network` over a road identifier, start and end offsets, and a carriageway direction, with a mean travel time over an explicit window. |
| 12 | [`12-bikeshare-station-status`](12-bikeshare-station-status/) | GBFS `StationStatus` | `cadence` of kind `onChange` and `count` statistics over dock and vehicle inventories, with POSIX second counts carrying their temporal reference system. |
| 13 | [`13-weather-alert`](13-weather-alert/) | US NWS `WeatherAlert` (CAP 1.2) | The two independent temporal axes of a public warning: the hazard window against the period the bulletin is in force. |
| 14 | [`14-marine-water-quality`](14-marine-water-quality/) | King County `WaterQualityReading` | The three-tier feature-of-interest chain — mooring, sampled water parcel, marine basin — across CTD, optical, and nutrient channels. |
| 15 | [`15-pollen-forecast`](15-pollen-forecast/) | DWD Pollenflug `PollenForecast` | A flat today/tomorrow/day-after record restructured into a bulletin plus per-lead entries, so that `forecastLeadDuration` has something to attach to. |

## Validation

These samples are covered by
[`../validate-characteristics.ps1`](../validate-characteristics.ps1), which walks
every `schema.struct.json` under `samples/`.

## Fidelity

The upstream property names, types, descriptions, units, and enumerations are
preserved wherever the annotation model allowed it. The samples depart from
their sources in four ways, each of which is stated in the affected schema's own
`description` or in the description of the affected property:

- Properties that carry no observational interest were dropped — transport
  routing axes, duplicate encodings of a value that appears elsewhere, and
  housekeeping channels — to keep each sample readable.
- A few properties were added where the upstream extraction omits something the
  publisher's own API carries and the sample needs. These are named in the
  schema descriptions.
- Members that carry a `unit` were narrowed from a nullable union to the plain
  numeric type and left out of `required`, because a unit may not be attached to
  a union. An unreported channel is therefore absent rather than null.
- `altenums`, `altnames`, `identity`, and `$root` were removed, because the
  Alternate Names and Relations extensions are not enabled by the Characteristics
  meta-schema.

Reference URIs that point at `example.org` are placeholders for composite
observable properties that no public catalogue publishes. The rest cite real
vocabularies and reference systems.
