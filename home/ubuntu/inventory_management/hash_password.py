from passlib.context import CryptContext

# Create password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Test password
test_password = "password123"

# Hash the test password
hashed_password = pwd_context.hash(test_password)

print(f"Hash of 'password123': {hashed_password}")

# Function to verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Verify the password
is_password_correct = verify_password(test_password, hashed_password)

print(f"Password verification result: {'Correct' if is_password_correct else 'Incorrect'}")
