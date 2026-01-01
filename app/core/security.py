from passlib.context import CryptContext
# Password hashing context using bcrypt algorithm
# This context will be used to hash and verify passwords securely
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# plain_password: The password the user entered (e.g., on login).
# hashed_password: The password stored in the database (hashed).
# pwd_context.verify():
  # Takes the plain password and the hashed password.
  # Checks if the plain password matches the hash.
  # Returns True if it matches, False otherwise
def verify_password(plain_password, hashed_password):
    """Verify a plain password against its hashed version."""
    return pwd_context.verify(plain_password, hashed_password)

# Takes a plain password and returns a secure hashed version.
# The hash is what you store in your database, never the plain password.
def get_password_hash(password):
    """Hash a plain password for secure storage."""
    return pwd_context.hash(password) # output example : $2b$12$K9jHq1l9v5YfD3EjGQvAxeB0w4h3Q.Kxk1X0h8uCzF6R0L5w1FZzK

# Example 
plain_password = "mysecretpassword"
hashed_password = get_password_hash(plain_password)

print(hashed_password)