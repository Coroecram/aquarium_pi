ALTER TABLE aquarium_data RENAME COLUMN temp_read TO water_temp;
ALTER TABLE aquarium_data RENAME COLUMN ph_read TO ph;
ALTER TABLE aquarium_data RENAME COLUMN lux_read TO lux;
ALTER TABLE aquarium_data ADD COLUMN air_temp FLOAT(2), ADD COLUMN humidity FLOAT(2);
