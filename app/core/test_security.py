# Testing the Security Functions after adding the pydanctic validations to the password field in EmployeeCreate schema
from app.schemas.employee_schema import EmployeeCreate
from pydantic import ValidationError, SecretStr
from app.core.security import get_password_hash, verify_password

def test_password_validation():
    try:
        emp = EmployeeCreate(
            first_name="Tamer",
            last_name="Elkot",
            email="tamerelkot@gmail.com",
            department="Engineering",
            username="tamerelkot",
            password=SecretStr("StrongPass124#")

        )
        print("Password validation passed:", emp.model_dump_json(indent=2))

        # Hash the password
        hashed_pwd = get_password_hash(emp.password.get_secret_value())
        print("Hashed Password:", hashed_pwd)

        # Verify the password
        is_correct = verify_password(emp.password.get_secret_value(), hashed_pwd)
        print("Password verification (correct):", is_correct)

    except ValidationError as e:
        print("Password validation failed:", e)
if __name__ == "__main__":
    test_password_validation()
# plain_password = "testpassword"
# hashed_password = get_password_hash(plain_password)
# print(f"hashed_password: {hashed_password}")

# is_correct = verify_password(plain_password, hashed_password)
# print(f"Password verification (correct):" ,is_correct)


# wrong_password = "WrongPassword123!"
# is_correct_wrong = verify_password(wrong_password, hashed_password)
# print("Password verification (wrong):", is_correct_wrong)

