CREATE PROCEDURE GetUserByUsername
    @username NVARCHAR(50)
AS
BEGIN
    SELECT first_name, last_name, email, username, is_active, password
    FROM users
    WHERE username = @username;
END;