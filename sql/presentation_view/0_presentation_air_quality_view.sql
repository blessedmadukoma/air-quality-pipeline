select * from air_quality.raw.air_quality_data;


CREATE SCHEMA presentation;

CREATE OR REPLACE VIEW presentation.air_quality_data AS (
	WITH ranked_data AS (
		SELECT
			*,
			ROW_NUMBER() OVER (
				PARTITION BY location_id, sensors_id, "datetime", "parameter"
				ORDER BY ingestion_datetime DESC
			) AS rn
		FROM raw.air_quality_data
		WHERE parameter IN ('pm10', 'pm25', 'so2')
	)
	SELECT
		location_id,
		sensors_id,
		"location",
		"datetime",
		lat,
		lon,
		"parameter",
		units,
		"value",
		"month",
		"year",
		ingestion_datetime
	FROM ranked_data
	WHERE rn = 1
);