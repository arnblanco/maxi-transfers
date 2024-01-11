USE maxitransfers;
GO

CREATE TABLE users (
    first_name NVARCHAR(50),
    last_name NVARCHAR(50),
    email NVARCHAR(100),
    username NVARCHAR(50),
    password NVARCHAR(255),
    is_active BIT,
    PRIMARY KEY (email, username)
);
GO

CREATE TABLE employee (
    first_name NVARCHAR(50),
    last_name NVARCHAR(50),
    birthday DATE,
    employee_id INT,
    curp NVARCHAR(18),
    ssn NVARCHAR(10),
    phone NVARCHAR(10),
    nationality NVARCHAR(50),

    CONSTRAINT PK_Employee PRIMARY KEY (employee_id)
);
GO

CREATE TABLE beneficiaries (
    first_name NVARCHAR(50),
    last_name NVARCHAR(50),
    birthday DATE,
    curp NVARCHAR(18),
    ssn NVARCHAR(10),
    phone NVARCHAR(10),
    nationality NVARCHAR(50),
    percentage INT,

    employee_id INT,

    CONSTRAINT PK_Beneficiary PRIMARY KEY (employee_id, curp)
);
GO