USE maxitransfers;

CREATE TABLE users (
    first_name NVARCHAR(50),
    last_name NVARCHAR(50),
    email NVARCHAR(100),
    username NVARCHAR(50),
    password NVARCHAR(255),
    is_active BIT,
    PRIMARY KEY (email, username)
);