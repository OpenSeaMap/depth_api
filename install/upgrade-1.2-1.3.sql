----------------------------------------------------------------------------------------------------
-- user_vessels
----------------------------------------------------------------------------------------------------

ALTER TABLE user_vessels ADD COLUMN name character varying;
ALTER TABLE user_vessels ADD COLUMN description character varying;
ALTER TABLE user_vessels ADD COLUMN user_name character varying;
ALTER TABLE user_vessels ADD COLUMN "MMSI" character varying(10);
ALTER TABLE user_vessels ADD COLUMN manufacturer character varying(100);
ALTER TABLE user_vessels ADD COLUMN model character varying;
ALTER TABLE user_vessels ADD COLUMN loa numeric(7,2);
ALTER TABLE user_vessels ADD COLUMN berth numeric(7,2);
ALTER TABLE user_vessels ADD COLUMN draft numeric(4,2);
ALTER TABLE user_vessels ADD COLUMN height numeric(4,2);
ALTER TABLE user_vessels ADD COLUMN displacement numeric(8,1);
ALTER TABLE user_vessels ADD COLUMN maximumspeed numeric(3,1);

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