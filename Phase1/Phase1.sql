-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2022-10-28 19:01:14.675

-- tables
-- Table: access_requests
CREATE TABLE access_requests (
    date date  NOT NULL,
    room_number int  NOT NULL,
    building_name varchar(20)  NOT NULL,
    employee_id int  NOT NULL,
    CONSTRAINT access_requests_pk PRIMARY KEY (room_number,building_name,employee_id,date)
);

-- Table: buildings
CREATE TABLE buildings (
    name varchar(20)  NOT NULL,
    CONSTRAINT buildings_pk PRIMARY KEY (name)
);

-- Table: door_name
CREATE TABLE door_name (
    name varchar(10)  NOT NULL,
    CONSTRAINT door_name_pk PRIMARY KEY (name)
);

-- Table: doors
CREATE TABLE doors (
    id serial  NOT NULL,
    building_name varchar(20)  NOT NULL,
    room_number int  NOT NULL,
    door_name varchar(10)  NOT NULL,
    CONSTRAINT doors_uk_01 UNIQUE (building_name, room_number, door_name) NOT DEFERRABLE  INITIALLY IMMEDIATE,
    CONSTRAINT doors_pk PRIMARY KEY (id)
);

-- Table: employees
CREATE TABLE employees (
    id serial  NOT NULL,
    name varchar(40)  NOT NULL,
    CONSTRAINT employees_pk PRIMARY KEY (id)
);

-- Table: hooks
CREATE TABLE hooks (
    id serial  NOT NULL,
    CONSTRAINT hooks_pk PRIMARY KEY (id)
);

-- Table: keys
CREATE TABLE keys (
    id serial  NOT NULL,
    hook_id int  NOT NULL,
    CONSTRAINT keys_pk PRIMARY KEY (id)
);

-- Table: loans
CREATE TABLE loans (
    id serial  NOT NULL,
    employee_id int  NOT NULL,
    key_id int  NOT NULL,
    start_time timestamp  NOT NULL,
    CONSTRAINT loan_uk_01 UNIQUE (employee_id, key_id, start_time) NOT DEFERRABLE  INITIALLY IMMEDIATE,
    CONSTRAINT loans_pk PRIMARY KEY (id)
);

-- Table: losses
CREATE TABLE losses (
    loan_id int  NOT NULL,
    date date  NOT NULL,
    CONSTRAINT losses_pk PRIMARY KEY (loan_id)
);

-- Table: opens
CREATE TABLE opens (
    hook_id int  NOT NULL,
    door_id int  NOT NULL,
    CONSTRAINT opens_pk PRIMARY KEY (hook_id,door_id)
);

-- Table: returns
CREATE TABLE returns (
    loan_id int  NOT NULL,
    date date  NOT NULL,
    CONSTRAINT returns_pk PRIMARY KEY (loan_id)
);

-- Table: rooms
CREATE TABLE rooms (
    building_name varchar(20)  NOT NULL,
    number int  NOT NULL,
    CONSTRAINT rooms_pk PRIMARY KEY (number,building_name)
);

-- foreign keys
-- Reference: Table_11_employees (table: loans)
ALTER TABLE loans ADD CONSTRAINT Table_11_employees
    FOREIGN KEY (employee_id)
    REFERENCES employees (id)
    ON DELETE  RESTRICT 
    ON UPDATE  RESTRICT 
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Table_11_keys (table: loans)
ALTER TABLE loans ADD CONSTRAINT Table_11_keys
    FOREIGN KEY (key_id)
    REFERENCES keys (id)
    ON DELETE  RESTRICT 
    ON UPDATE  RESTRICT 
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Table_7_hooks (table: opens)
ALTER TABLE opens ADD CONSTRAINT Table_7_hooks
    FOREIGN KEY (hook_id)
    REFERENCES hooks (id)
    ON DELETE  RESTRICT 
    ON UPDATE  RESTRICT 
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: access_requests_employees (table: access_requests)
ALTER TABLE access_requests ADD CONSTRAINT access_requests_employees
    FOREIGN KEY (employee_id)
    REFERENCES employees (id)
    ON DELETE  RESTRICT 
    ON UPDATE  RESTRICT 
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: access_requests_rooms (table: access_requests)
ALTER TABLE access_requests ADD CONSTRAINT access_requests_rooms
    FOREIGN KEY (room_number, building_name)
    REFERENCES rooms (number, building_name)
    ON DELETE  RESTRICT 
    ON UPDATE  RESTRICT 
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: doors_door_names (table: doors)
ALTER TABLE doors ADD CONSTRAINT doors_door_names
    FOREIGN KEY (door_name)
    REFERENCES door_name (name)
    ON DELETE  RESTRICT 
    ON UPDATE  RESTRICT 
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: doors_rooms (table: doors)
ALTER TABLE doors ADD CONSTRAINT doors_rooms
    FOREIGN KEY (room_number, building_name)
    REFERENCES rooms (number, building_name)
    ON DELETE  RESTRICT 
    ON UPDATE  RESTRICT 
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: keys_hooks (table: keys)
ALTER TABLE keys ADD CONSTRAINT keys_hooks
    FOREIGN KEY (hook_id)
    REFERENCES hooks (id)
    ON DELETE  RESTRICT 
    ON UPDATE  RESTRICT 
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: losses_loans (table: losses)
ALTER TABLE losses ADD CONSTRAINT losses_loans
    FOREIGN KEY (loan_id)
    REFERENCES loans (id)
    ON DELETE  RESTRICT 
    ON UPDATE  RESTRICT 
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: opens_doors (table: opens)
ALTER TABLE opens ADD CONSTRAINT opens_doors
    FOREIGN KEY (door_id)
    REFERENCES doors (id)
    ON DELETE  RESTRICT 
    ON UPDATE  RESTRICT 
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: returns_loans (table: returns)
ALTER TABLE returns ADD CONSTRAINT returns_loans
    FOREIGN KEY (loan_id)
    REFERENCES loans (id)
    ON DELETE  RESTRICT 
    ON UPDATE  RESTRICT 
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: rooms_buildings (table: rooms)
ALTER TABLE rooms ADD CONSTRAINT rooms_buildings
    FOREIGN KEY (building_name)
    REFERENCES buildings (name)
    ON DELETE  RESTRICT 
    ON UPDATE  RESTRICT 
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- End of file.

