# Secure Authentication Lab

## Objective

This project demonstrates a small local authentication service with defensive authentication controls.

## Security Controls Implemented

### 1. Password Hashing

Passwords are not stored as plain text. The application uses Werkzeug password hashing functions to securely hash passwords before storing them.

### 2. Server-Side Input Validation

The server validates username and password input.

The application checks:

* Username is not empty.
* Username length is between 3 and 30 characters.
* Password length is between 8 and 100 characters.

Invalid input is rejected by the server.

### 3. Secure Session Cookies

The application uses secure session cookie settings:

* HttpOnly
* SameSite=Lax

For this local HTTP lab, the Secure cookie option is disabled because the application is running on localhost without HTTPS. In a real HTTPS deployment, Secure should be enabled.

### 4. Session Expiry

Authenticated sessions expire after 5 minutes.

When the session expires, the user must authenticate again.

### 5. Logout

The logout endpoint clears the current session so that the authenticated user is logged out.

### 6. Rate Limiting

The application limits failed login attempts.

A maximum of 5 failed attempts is allowed within a 60-second period.

This helps reduce brute-force login attacks.

### 7. Generic Authentication Errors

The application uses a generic error message:

"Invalid username or password"

It does not reveal whether a username exists. This helps reduce username enumeration.

## Automated Testing

Automated tests were created using pytest.

The tests verify:

* User registration
* Successful login
* Incorrect password handling
* Protected route access
* Logout
* Invalid password validation

## Test Result

All 6 automated tests passed successfully.

```text
6 passed in 1.04s
```

## Conclusion

The authentication service demonstrates basic defensive security controls including password hashing, server-side validation, secure session handling, logout, session expiry, rate limiting, and generic authentication errors.

These controls help reduce common authentication risks such as password exposure, brute-force attacks, session abuse, and username enumeration.
