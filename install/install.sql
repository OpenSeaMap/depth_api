----------------------------------------------------------------------------------------------------
-- user_profiles
----------------------------------------------------------------------------------------------------

CREATE TABLE user_profiles (
    user_name varchar(40) NOT NULL,
    password varchar(40),
    salt varchar(10),
    attempts smallint NOT NULL DEFAULT 0,
    last_attempt timestamp
);

ALTER TABLE user_profiles
    ADD CONSTRAINT user_profiles_pkey PRIMARY KEY (user_name);


----------------------------------------------------------------------------------------------------
-- user_tracks
----------------------------------------------------------------------------------------------------
-- The field 'track_id' is not an autoincrement field, because a track id has to be fetched
-- before the user can upload a new track.
--
-- Upload states:
--   0 : not started yet
--   1 : done
----------------------------------------------------------------------------------------------------

CREATE TABLE user_tracks (
    track_id bigint NOT NULL,
    user_name varchar(40) NOT NULL,
    file_ref varchar(255),
    upload_state smallint DEFAULT 0
);

ALTER TABLE user_tracks
    ADD CONSTRAINT user_tracks_pkey PRIMARY KEY (track_id);

CREATE SEQUENCE user_tracks_track_id_seq;


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
