-- Create user and database

DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE  rolname = 'postgres') THEN

      CREATE ROLE my_user LOGIN PASSWORD 'postgres';
   END IF;
END
$do$;

SELECT 'CREATE DATABASE postgres'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'postgres')\gexec

GRANT ALL PRIVILEGES ON DATABASE postgres TO postgres;

-- Create tables

CREATE TABLE IF NOT EXISTS vehicle_function (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS vehicle_feature (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL UNIQUE,
  function_list INTEGER[]
);

CREATE TABLE IF NOT EXISTS vehicle_subgroup (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL UNIQUE,
  is_set BOOLEAN DEFAULT FALSE,
  feature_list INTEGER[]
);

CREATE TABLE IF NOT EXISTS vehicle_group (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL UNIQUE,
  subgroup_list INTEGER[],
  feature_list INTEGER[]
);

CREATE TABLE IF NOT EXISTS vehicle (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL UNIQUE,
  group_list INTEGER[]
);

CREATE TABLE IF NOT EXISTS vehicle_component (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS feature_component (
  id SERIAL PRIMARY KEY,
  feature_id int REFERENCES vehicle_feature (id),
  component_id int REFERENCES vehicle_component (id)
);

-- Insert data

INSERT INTO vehicle_function (name)
VALUES ('Func1');
INSERT INTO vehicle_function (name)
VALUES ('Func2');
INSERT INTO vehicle_function (name)
VALUES ('Func3');
INSERT INTO vehicle_function (name)
VALUES ('Func4');

INSERT INTO vehicle_feature (name, function_list)
VALUES ('Feature1', '{1, 2}');
INSERT INTO vehicle_feature (name, function_list)
VALUES ('Feature2', '{1}');
INSERT INTO vehicle_feature (name, function_list)
VALUES ('Feature3', '{2, 3}');
INSERT INTO vehicle_feature (name, function_list)
VALUES ('Feature4', '{4}');

INSERT INTO vehicle_subgroup (name, feature_list)
VALUES ('Subgroup1', '{1, 2}');
INSERT INTO vehicle_subgroup (name, feature_list)
VALUES ('Subgroup2', '{2}');
INSERT INTO vehicle_subgroup (name, feature_list, is_set)
VALUES ('Set1', '{3}', True);
INSERT INTO vehicle_subgroup (name, feature_list, is_set)
VALUES ('Set2', '{2, 4}', True);

INSERT INTO vehicle_group (name, subgroup_list)
VALUES ('GroupName1', '{1}');
INSERT INTO vehicle_group (name, feature_list)
VALUES ('GroupName2', '{1, 3}');
INSERT INTO vehicle_group (name, feature_list, subgroup_list)
VALUES ('GroupName3', '{2}', '{4}');

INSERT INTO vehicle (name, group_list)
VALUES ('Vehicle1', '{1, 2, 3}');

INSERT INTO vehicle_component (name)
VALUES ('Component1');
INSERT INTO vehicle_component (name)
VALUES ('Component2');

INSERT INTO feature_component (component_id, feature_id)
VALUES (1, 1);
INSERT INTO feature_component (component_id, feature_id)
VALUES (1, 2);
INSERT INTO feature_component (component_id, feature_id)
VALUES (2, 3);
INSERT INTO feature_component (component_id, feature_id)
VALUES (2, 4);
INSERT INTO feature_component (component_id, feature_id)
VALUES (1, 4);