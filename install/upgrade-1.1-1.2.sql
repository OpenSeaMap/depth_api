----------------------------------------------------------------------------------------------------
-- user_vessels
----------------------------------------------------------------------------------------------------

CREATE SEQUENCE user_vessels_vessel_id_seq;

CREATE TABLE user_vessels (
    vessel_id integer NOT NULL DEFAULT nextval('user_vessels_vessel_id_seq'),
    user_name varchar(40) NOT NULL,
    settings hstore
);

ALTER TABLE user_vessels
    ADD CONSTRAINT user_vessels_pkey PRIMARY KEY (vessel_id);

ALTER TABLE user_vessels
    ADD CONSTRAINT user_vessels_user_name_fkey FOREIGN KEY (user_name) REFERENCES user_profiles(user_name) ON UPDATE CASCADE ON DELETE CASCADE;

CREATE INDEX user_vessels_user_name ON user_vessels (user_name);

CREATE UNIQUE INDEX user_vessels_name ON user_vessels (user_name, (settings -> 'name'));

CREATE INDEX user_vessels_settings ON user_vessels USING gin (settings);
