CREATE PROCEDURE GetUserByUsername
    @username NVARCHAR(50)
AS
BEGIN
    SELECT first_name, last_name, email, username, is_active, password
    FROM users
    WHERE username = @username;
END;

CREATE PROCEDURE InsertUser
    @first_name NVARCHAR(50),
    @last_name NVARCHAR(50),
    @email NVARCHAR(100),
    @username NVARCHAR(50),
    @password NVARCHAR(255),
    @is_active BIT
AS
BEGIN
    INSERT INTO users (first_name, last_name, email, username, password, is_active)
    VALUES (@first_name, @last_name, @email, @username, @password, @is_active);
END;

CREATE PROCEDURE UpdateUser
    @email NVARCHAR(100),
    @username NVARCHAR(50),
    @first_name NVARCHAR(50),
    @last_name NVARCHAR(50),
    @is_active BIT
AS
BEGIN
    UPDATE users
    SET 
        first_name = @first_name,
        last_name = @last_name,
        is_active = @is_active
    WHERE
        email = @email AND
        username = @username;
END;

CREATE PROCEDURE DeleteUser
    @email NVARCHAR(100),
    @username NVARCHAR(50)
AS
BEGIN
    DELETE FROM users
    WHERE email = @email AND username = @username;
END;

CREATE PROCEDURE GetEmployees
AS
BEGIN
    SELECT 
        e.*,
        ISNULL(beneficiary_count, 0) AS beneficiary_count
    FROM employee e
    LEFT JOIN (
        SELECT 
            employee_id, 
            COUNT(*) AS beneficiary_count
        FROM beneficiaries
        GROUP BY employee_id
    ) b ON e.employee_id = b.employee_id;
END;

CREATE PROCEDURE GetEmployeeById
    @employee_id INT
AS
BEGIN
    SELECT 
        e.*,
        ISNULL(beneficiary_count, 0) AS beneficiary_count
    FROM employee e
    LEFT JOIN (
        SELECT 
            employee_id, 
            COUNT(*) AS beneficiary_count
        FROM beneficiaries
        GROUP BY employee_id
    ) b_count ON e.employee_id = b_count.employee_id
    WHERE e.employee_id = @employee_id;
END;

CREATE PROCEDURE InsertEmployee
    @first_name NVARCHAR(50),
    @last_name NVARCHAR(50),
    @birthday DATE,
    @employee_id INT,
    @curp NVARCHAR(18),
    @ssn NVARCHAR(10),
    @phone NVARCHAR(10),
    @nationality NVARCHAR(50)
AS
BEGIN
    INSERT INTO employee (first_name, last_name, birthday, employee_id, curp, ssn, phone, nationality)
    VALUES (@first_name, @last_name, @birthday, @employee_id, @curp, @ssn, @phone, @nationality);
END;

CREATE PROCEDURE UpdateEmployee
    @employee_id INT,
    @first_name NVARCHAR(50),
    @last_name NVARCHAR(50),
    @birthday DATE,
    @curp NVARCHAR(18),
    @ssn NVARCHAR(10),
    @phone NVARCHAR(10),
    @nationality NVARCHAR(50)
AS
BEGIN
    UPDATE employee
    SET
        first_name = @first_name,
        last_name = @last_name,
        birthday = @birthday,
        curp = @curp,
        ssn = @ssn,
        phone = @phone,
        nationality = @nationality
    WHERE
        employee_id = @employee_id;
END;

CREATE PROCEDURE DeleteEmployee
    @employee_id INT
AS
BEGIN
    DELETE FROM employee
    WHERE employee_id = @employee_id;
END;

CREATE PROCEDURE GetBeneficiariesByEmployeeId
    @employee_id INT
AS
BEGIN
    SELECT * 
    FROM beneficiaries
    WHERE employee_id = @employee_id;
END;

CREATE PROCEDURE GetBeneficiary
    @curp NVARCHAR(18),
    @employee_id INT
AS
BEGIN
    SELECT * 
    FROM beneficiaries
    WHERE curp = @curp AND employee_id = @employee_id;
END;

CREATE PROCEDURE InsertBeneficiary
    @first_name NVARCHAR(50),
    @last_name NVARCHAR(50),
    @birthday DATE,
    @curp NVARCHAR(18),
    @ssn NVARCHAR(10),
    @phone NVARCHAR(10),
    @nationality NVARCHAR(50),
    @percentage INT,
    @employee_id INT
AS
BEGIN
    INSERT INTO beneficiaries (
        first_name,
        last_name,
        birthday,
        curp,
        ssn,
        phone,
        nationality,
        percentage,
        employee_id
    )
    VALUES (
        @first_name,
        @last_name,
        @birthday,
        @curp,
        @ssn,
        @phone,
        @nationality,
        @percentage,
        @employee_id
    );
END;

CREATE PROCEDURE UpdateBeneficiary
    @first_name NVARCHAR(50),
    @last_name NVARCHAR(50),
    @birthday DATE,
    @curp NVARCHAR(18),
    @ssn NVARCHAR(10),
    @phone NVARCHAR(10),
    @nationality NVARCHAR(50),
    @percentage INT,
    @employee_id INT
AS
BEGIN
    UPDATE beneficiaries
    SET
        first_name = @first_name,
        last_name = @last_name,
        birthday = @birthday,
        curp = @curp,
        ssn = @ssn,
        phone = @phone,
        nationality = @nationality,
        percentage = @percentage,
        employee_id = @employee_id
    WHERE curp = @curp AND employee_id = @employee_id;
END;

CREATE PROCEDURE DeleteBeneficiary
    @employee_id INT,
    @curp NVARCHAR(18)
AS
BEGIN
    DELETE FROM beneficiaries
    WHERE curp = @curp AND employee_id = @employee_id;
END;