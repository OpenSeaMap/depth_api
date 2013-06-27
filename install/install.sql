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
-- UPLOAD_INCOMPLETE(0)
-- UPLOAD_COMPLETE(1)
-- FILE_CORRUPT(2)
-- PREPROCESSED(3)
-- FILE_CONTENT_UNKNOWN(4)
-- FILE_DUPLICATE(5);
----------------------------------------------------------------------------------------------------

CREATE TABLE user_tracks (
    track_id bigint NOT NULL,
    user_name varchar(40) NOT NULL,
    file_ref varchar(255),
    upload_state smallint DEFAULT 0,    
	filetype character varying(80),
    compression character varying(80),
    containertrack integer,
    vesselconfigid character varying
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
    name character varying,
    description character varying,
    user_name character varying,
    "MMSI" character varying(20),
    manufacturer character varying(100),
    model character varying,
    loa numeric(7,2),
    berth numeric(7,2),
    draft numeric(4,2),
    height numeric(4,2),
    displacement numeric(8,1),
    maximumspeed numeric(3,1)
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


--
-- Name: depthsoffset; Type: TABLE; 
-- x: position from ship centerline to left and right
-- y: position from stern (0) to front (max length over all)
-- z: position below water line
-- sensorid: an id to identify the sensor within the recorded data
-- frequency: values in kHz
-- angleofbeam: opening angle in degrees

CREATE TABLE depthsoffset (
    vesselconfigid integer NOT NULL,
    x numeric(5,2) NOT NULL,
    y numeric(5,2) NOT NULL,
    z numeric(5,2) NOT NULL,
    sensorid character varying,
    manufacturer character varying(100),
    model character varying(100),
    frequency numeric(5,0),
    angleofbeam numeric(3,0)
);


--
-- Name: sbasoffset; Type: TABLE; 
-- x: position from ship centerline to left and right
-- y: position from stern (0) to front (max length over all)
-- z: position below water line
-- sensorid: an id to identify the sensor within the recorded data
--

CREATE TABLE sbasoffset (
    vesselconfigid integer NOT NULL,
    x numeric(5,2) NOT NULL,
    y numeric(5,2) NOT NULL,
    z numeric(5,2) NOT NULL,
    sensorid character varying,
    manufacturer character varying(100),
    model character varying(100)
);

