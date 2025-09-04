<<<<<<< HEAD
use dochicar;
=======
use dochidb;
>>>>>>> origin

CREATE TABLE car (
	car_id INT auto_increment primary key,
	comp_name VARCHAR(30),
    model_name VARCHAR(100),
    img_url varchar(255),
    launch_date varchar(8),
    model_type VARCHAR(30),
    model_price int,
    resrc_type varchar(20),
    resrc_amount varchar(30),
    efficiency_type varchar(20),
    efficiency_amount varchar(30),
    wait_period varchar(100)
    );

CREATE TABLE fuel(
	fuel_id INT auto_increment primary key,
	model_name varchar(100),
    fuel_type varchar(30)
);
