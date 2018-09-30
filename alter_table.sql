ALTER TABLE cabrini_tank_2018 RENAME COLUMN temp_read TO water_temp;
ALTER TABLE cabrini_tank_2018 RENAME COLUMN ph_read TO ph;
ALTER TABLE cabrini_tank_2018 RENAME COLUMN lux_read TO lux;
ALTER TABLE cabrini_tank_2018 ADD COLUMN air_temp FLOAT(2), ADD COLUMN humidity FLOAT(2);
