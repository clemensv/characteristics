# Five derived metrics for the `BuoyObservation` stream

## 1. The five metrics

1. **Pressure-tendency divergence (hPa/h).** The pressure rate observed between
   two consecutive records, minus the mean rate the record already declares
   (`pressure_tendency / 3`, since the schema defines that member as the signed
   change over the *preceding 3 hours* ending at the observation time). Both
   terms are signed hPa per hour, so the difference says whether the pressure
   change right now is faster or slower than the three-hour average it is being
   folded into. An operator wants this because the carried tendency is a
   three-hour smoother and therefore lags: a system that has begun to deepen
   shows up in the divergence long before it dominates the tendency. It is a
   residual against a reference the schema itself declares, which is the
   strongest kind of derived value this feed supports.

2. **Gust factor (dimensionless).** `gust / wind_speed`, reported as window mean
   and window maximum. The schema states that `gust` is the greatest
   short-interval speed *within the same averaging window that produced*
   `wind_speed`, so the ratio is well defined even though the length of that
   window is left indeterminate — the unknown length cancels. An operator wants
   it because absolute wind speed does not distinguish a steady 7 m/s from a
   squally 7 m/s with 15 m/s peaks, and it is the peaks that part mooring lines
   and knock down small craft.

3. **Cadence completeness and longest gap.** Records received per station per
   window against the number the schema says to expect (one per five-minute
   slot), plus the longest interval between consecutive observations in the
   window. The schema declares the publication cadence explicitly, so a
   shortfall is measurable rather than guessed. An operator wants it first
   because it is the metric that tells them whether to trust the other four:
   every window mean here silently degrades when the platform or the ingest
   thins out, and nothing else in the record reveals that.

4. **Sea-state build rate (m/h).** Signed change in significant wave height per
   hour between consecutive observations, reported as window mean, fastest build
   and fastest decay. The height says how big the sea is; the rate says whether
   it is building or laying down, which is the quantity a departure-or-hold
   decision actually turns on.

5. **Spectral period ratio (dimensionless).** `dominant_wave_period /
   average_wave_period`. The schema defines DPD as the period of the band
   carrying maximum energy and APD as the mean of all wave periods in the
   sampling window; a ratio well above 1 therefore means the energy peak sits at
   periods substantially longer than the typical wave, i.e. long-period energy
   coexisting with shorter ones. An operator wants it because a 1.8 m sea at
   ratio ≈ 1 and a 1.8 m sea at ratio ≈ 2 are different sea states for the same
   reported height.

## 2. The query

```sql
-- Dialect: Azure Stream Analytics / Microsoft Fabric Eventstream SQL.
--
-- Event time   : [timestamp] -- the only temporal member the schema carries.
-- Source key   : station_id  -- the only member that identifies an observing platform.
-- Aggregation  : TumblingWindow(minute, 30), non-overlapping, one row per station
--                per window. 30 minutes is six of the five-minute slots the schema
--                says the producer emits, which gives the cadence metric an integer
--                denominator and gives the pressure-rate mean six samples to average.
-- Event-to-event reach: LAG(..., 1) OVER (PARTITION BY station_id
--                LIMIT DURATION(minute, 30)). The LIMIT DURATION is required by the
--                dialect; 30 minutes doubles as the cut-off beyond which no rate of
--                change is emitted at all, so nothing is differenced across an outage.

WITH Observations AS
(
    SELECT
        station_id,
        CAST([timestamp] AS datetime) AS obs_time,
        wind_speed,
        gust,
        pressure,
        pressure_tendency,
        wave_height,
        dominant_wave_period,
        average_wave_period
    FROM input TIMESTAMP BY [timestamp]
),

-- Reach this station's previous observation.
Previous AS
(
    SELECT
        station_id,
        obs_time,
        wind_speed,
        gust,
        pressure,
        pressure_tendency,
        wave_height,
        dominant_wave_period,
        average_wave_period,
        LAG(obs_time,    1) OVER (PARTITION BY station_id LIMIT DURATION(minute, 30)) AS prev_time,
        LAG(pressure,    1) OVER (PARTITION BY station_id LIMIT DURATION(minute, 30)) AS prev_pressure,
        LAG(wave_height, 1) OVER (PARTITION BY station_id LIMIT DURATION(minute, 30)) AS prev_wave_height
    FROM Observations
),

PerEvent AS
(
    SELECT
        station_id,
        obs_time,

        -- Elapsed time since this station's previous record. NULL if there was none
        -- inside the LAG reach, which correctly nulls every rate below.
        DATEDIFF(second, prev_time, obs_time) AS gap_seconds,

        -- METRIC 2. gust and wind_speed share one averaging window per the schema,
        -- so the ratio needs no knowledge of that window's length. Undefined at calm.
        CASE WHEN wind_speed > 0 THEN gust / wind_speed END AS gust_factor,

        -- METRIC 5. Both periods are seconds over the same record's sampling of the sea.
        CASE WHEN average_wave_period > 0
             THEN dominant_wave_period / average_wave_period
        END AS period_ratio,

        -- METRIC 1, first half: pressure rate observed between consecutive records.
        CASE WHEN DATEDIFF(second, prev_time, obs_time) > 0
             THEN (pressure - prev_pressure) * 3600.0
                  / DATEDIFF(second, prev_time, obs_time)
        END AS pressure_rate_hpa_per_h,

        -- METRIC 1, second half: that rate minus the declared 3-hour mean rate.
        -- pressure_tendency is a signed 3-hour change in the same sea-level-reduced
        -- quantity as `pressure`, so /3.0 puts both terms in hPa per hour.
        CASE WHEN DATEDIFF(second, prev_time, obs_time) > 0
             THEN ((pressure - prev_pressure) * 3600.0
                   / DATEDIFF(second, prev_time, obs_time))
                  - (pressure_tendency / 3.0)
        END AS tendency_divergence_hpa_per_h,

        -- METRIC 4. Signed change in significant wave height, per hour.
        CASE WHEN DATEDIFF(second, prev_time, obs_time) > 0
             THEN (wave_height - prev_wave_height) * 3600.0
                  / DATEDIFF(second, prev_time, obs_time)
        END AS wave_rate_m_per_h

    FROM Previous
)

SELECT
    station_id,
    System.Timestamp() AS window_end,

    -- METRIC 1. Averaged over the 30-minute tumbling window to lift the signal above
    -- the quantisation of a five-minute pressure difference (see Assumptions).
    AVG(tendency_divergence_hpa_per_h) AS tendency_divergence_hpa_per_h,
    AVG(pressure_rate_hpa_per_h)       AS observed_pressure_rate_hpa_per_h,

    -- METRIC 2.
    AVG(gust_factor) AS gust_factor_mean,
    MAX(gust_factor) AS gust_factor_max,

    -- METRIC 3. Denominator 6 = 30-minute window / declared 5-minute slot.
    COUNT(*)         AS observations_received,
    COUNT(*) / 6.0   AS cadence_completeness,
    MAX(gap_seconds) AS longest_gap_seconds,

    -- METRIC 4. MAX is the fastest build, MIN the fastest decay; both are signed.
    AVG(wave_rate_m_per_h) AS wave_rate_mean_m_per_h,
    MAX(wave_rate_m_per_h) AS wave_rate_fastest_build_m_per_h,
    MIN(wave_rate_m_per_h) AS wave_rate_fastest_decay_m_per_h,

    -- METRIC 5.
    AVG(period_ratio) AS period_ratio_mean

INTO output
FROM PerEvent
GROUP BY station_id, TumblingWindow(minute, 30)
```

## 3. What I did not compute

* **Angular separation of `wind_direction` and `mean_wave_direction`** (a
  wind-against-sea alignment metric). The schema states that `wind_direction` is
  the direction the wind is coming *from*. It states no convention at all for
  `mean_wave_direction` — from or towards. A separation of 0° therefore means
  either "wind and waves aligned" or "wind and waves exactly opposed", depending
  on a fact the files do not supply. The number would be uninterpretable, so I
  left it out.
* **Any window mean of `wind_direction` or `mean_wave_direction`.** They are
  degrees on a circle: `AVG()` over 350° and 10° returns 180°, which is the
  opposite of the truth. A correct circular mean needs a sine/cosine
  decomposition, and I preferred to omit the value rather than publish a scalar
  average that is wrong precisely at the wrap point.
* **Reconstructing the true three-hour change, `pressure` minus `pressure` three
  hours earlier**, to check `pressure_tendency` directly. `LAG` reaches the
  immediately preceding event, not the event three hours back, and pulling the
  first and last `pressure` out of a three-hour `HoppingWindow` would need
  `FIRST`/`LAST`/`TopOne`, whose availability in this dialect I could not
  confirm from what I was given. Comparing *rates* gets at the same divergence
  using only constructs I was told exist.
* **Threshold flags** on `wind_speed`, `gust`, `wave_height` or
  `pressure_tendency` (gale warning, storm-force, dangerous sea). The files
  declare units but no thresholds, no station class and no climatology; any
  cut-off would be a number I invented.
* **Wave steepness** from `wave_height` and `dominant_wave_period`. Converting a
  period to a wavelength requires the deep-water dispersion relation and a value
  of *g*. Neither is in the two files, and the ratio without that conversion is
  not steepness.
* **`air_temperature − water_temperature` and `water_temperature − dewpoint`.**
  Both are arithmetically sound — same units, same platform, same record. I
  ranked them below the five above, and the second one's value rests on
  `dewpoint` being the saturation temperature of the air, which the schema names
  but never states.
* **Anything over `visibility` and `tide`.** Neither is required, neither
  appears in the one example record, and the schema says visibility is generally
  only available on C-MAN stations — a class the record does not carry. A window
  aggregate would be taken over an unknown, station-dependent sample.
* **Position change from `latitude`/`longitude` between records** (mooring watch
  circle, drift). Nothing in the files says the platform moves, and nothing
  gives a position accuracy, so a non-zero displacement could not be told apart
  from sensor jitter.
* **Any cross-station aggregate.** The files establish no region membership, no
  spacing, and no way to tell a deep-ocean buoy from a C-MAN station or a
  partner platform. A mean pressure or wave height across an arbitrary set of
  stations in one window is not a quantity.

## 4. Assumptions

Each of the following is an assumption; the two files do not establish it.

* **Assumption:** `timestamp` is the correct event time for windowing and is
  populated on every record. (The schema does make it required; that it is the
  intended event time rather than, say, a publication time, is my reading.)
* **Assumption:** the producer actually meets the declared cadence closely
  enough that six records per 30-minute window is the right denominator, and
  there are no duplicates or replays. Duplicates would push
  `cadence_completeness` above 1, which is why the raw `observations_received`
  is emitted alongside it.
* **Assumption:** the five-minute gaps are near-uniform, so the mean of
  per-event rates approximates the rate over the whole window. Where gaps are
  irregular the mean is weighted by record count rather than by elapsed time.
* **Assumption:** `pressure` is reported at about 0.1 hPa resolution — I infer
  this from the single value `1016.4` in the one example record. If so, a
  five-minute difference is quantised at roughly ±1.2 hPa/h, and only the
  30-minute mean makes the divergence in metric 1 readable. A finer or coarser
  resolution would change the window size I would choose.
* **Assumption:** `wave_height`, `average_wave_period` and
  `dominant_wave_period` in one record describe the same stretch of sea, ending
  at the observation time. The schema gives 20 minutes for the first two, gives
  no window at all for `dominant_wave_period`, and never says any of these
  windows end at the observation time.
* **Consequence of the above, not an assumption:** consecutive records are ~5
  minutes apart while `wave_height` summarises ~20 minutes, so successive values
  share most of their sampling window. `wave_rate_m_per_h` is therefore a
  smoothed derivative of an already-smoothed quantity, not an independent
  difference. It is still directional and still useful; it is not a measurement
  of how much the sea changed in five minutes.
* **Assumption:** `station_id` is stable and unique per platform for the life of
  the stream, and a station does not change type mid-stream. The schema says it
  identifies the platform; persistence is my reading.
* **Assumption:** the aggregate functions ignore NULLs, so a window mean may be
  taken over fewer rows than `observations_received` when an optional member
  such as `wave_height` or `pressure_tendency` is absent. The count is emitted
  so a consumer can see that the denominators may differ.
* **Not an assumption, stated by the schema and relied on:** `gust` and
  `wind_speed` share one averaging window (metric 2), and `pressure_tendency` is
  a signed change in the same sea-level-reduced pressure over the three hours
  ending at the observation time, negative for falling (metric 1). Both metrics
  would be unsound without those two sentences.
* **Assumption about the dialect:** that multi-step `WITH ... AS` feeding a
  single `SELECT ... INTO`, `LAG` with `LIMIT DURATION`, `DATEDIFF(second, …)`
  and `CASE` inside a windowed `SELECT` are all accepted as written. I stayed
  inside the constructs I was told exist and avoided `FIRST`/`LAST`/`TopOne`,
  `COUNT(DISTINCT …)` and any trigonometric function for that reason.
