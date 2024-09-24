import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from passlib.context import CryptContext
from app import users_db, verify_password

# Create password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Test password
test_password = "password123"

# Get the stored hash for the test user
stored_hash = users_db["testuser"]["hashed_password"]

# Hash the test password
hashed_test_password = pwd_context.hash(test_password)

# Verify the password
is_password_correct = verify_password(test_password, stored_hash)

print(f"Stored hash: {stored_hash}")
print(f"New hash of 'password123': {hashed_test_password}")
print(f"Password verification result: {'Correct' if is_password_correct else 'Incorrect'}")
