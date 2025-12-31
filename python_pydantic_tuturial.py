from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
    email: str
    jop_title: str = "Employee"  # Default value

user1 = User(name="Tamer", age=22, email="tamerelkot@gmail.com", jop_title="AI Engineer")
print(user1)

user2 = User(name="Nada", age=21, email="nadaahmed@gmail.com", jop_title=8)
print(user2)