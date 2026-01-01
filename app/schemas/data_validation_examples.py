video_url = "https://www.youtube.com/watch?v=M81pfi64eeM&list=PLAARbO_FynB1_UG1F0rgUMcnHySbSP4Mq&index=22"
# from pydantic import BaseModel

# class User(BaseModel):
#     name: str
#     age: int
#     email: str
#     jop_title: str = "Employee"  # Default value

# user1 = User(name="Tamer", age=22, email="tamerelkot@gmail.com", jop_title="AI Engineer")
# print(user1)

# user2 = User(name="Nada", age=21, email="nadaahmed@gmail.com", jop_title=8)
# print(user2)

from pydantic import (
    BaseModel,
    ValidationError,
    Field,
    EmailStr,
    HttpUrl,
    ValidationInfo,
    field_validator,
    model_validator,
    computed_field,
    SecretStr)
from uuid import UUID, uuid4
from datetime import datetime, timezone
from functools import partial
from typing import Literal, Annotated

class User(BaseModel):
    # uid : Annotated[int, Field(gt=0)]  # uid must be a positive integer
    # Annotated is used to add metadata to the type hint, in this case, we are using Field to specify that uid must be greater than 0.

    # Generate Unique User ID for each user using UUID
    uid: UUID = Field(default_factory=uuid4) # uid is a UUID, default value is generated using uuid4 function 
    # default_factory is used to specify a callable that will be called to generate a default value when no value is provided.
    # uuid4 generates a random UUID.

    username: Annotated[str, Field(min_length=3, max_length=50)] # username must be between 3 and 50 characters long

    email: EmailStr # email must be a valid email address
    website: HttpUrl | None = None # Optional field for user's website, must be a valid URL if provided if not provided, it will be None.
    password: SecretStr # password is stored as a SecretStr to prevent accidental exposure in logs or error messages and hide its value when printed.
    age: Annotated[int, Field(ge=13, le=120)] # age must be between 13 and 120

    verified_at: datetime | None = None # If the user is verified, this field will contain the date and time of verification; otherwise, it will be None.
    is_active: bool = True # By default, the user is active

    # full_name: str | None = None # Optional field for the user's full name
    first_name: str = ""
    last_name: str = ""
    follower_count: int =0

# try:
#     user = User(uid=1, username="tamer", email="tamerelkot@gmail.com")
# except ValidationError as e:
#     print(e)
# user.username = "ahmed"
# print(user.model_dump())
# print(user.model_dump_json(indent=2))

    # Adding a custom validator for username to ensure it does not contain spaces 
    @field_validator("username")   # field-level validator for the username field
    @classmethod # class method decorator to indicate that this method is a class method
    def validate_username(cls, v: str) -> str: # v is the value of the username field
        if not v.replace("_","").isalnum(): # Check if the username is alphanumeric or contains underscores
            raise ValueError("Username must alphanumeric and can contain underscores")
        
        return v.lower() # Convert username to lowercase before storing it
    # Checking that the website starts with "https://"
    @field_validator("website", mode="before") # field-level validator for the website field, mode="before" means the validator is called before any other validation is performed
    @classmethod
    def add_https_prefix(cls, v: HttpUrl | None) -> str | None: # v is the value of the website field
        if v and not  v.startswith(("http://", "https://")): # If the website is provided and does not start with "http://" or "https://"
            return f"https://{v}" # Add "https://" prefix to the website
        return v
    
    @computed_field  # computed field decorator to indicate that this method is a computed field
    @property
    def display_name(self) -> str: # display_name is a computed field that returns the user's full name if available, otherwise returns the username
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    @computed_field
    @property
    def is_influencer(self) -> bool: # is_influencer is a computed field that returns True if the user has more than 1000 followers
        return self.follower_count >= 10000
    
class Comment(BaseModel):
    content: str
    auther_email: EmailStr
    likes: int = 0


class BlogPost(BaseModel):
    title: Annotated[str, Field(min_length=5, max_length=100)] # Title must be between 5 and 100 characters long
    content: Annotated[str, Field(min_length=20)] # Content must be at least 20 characters long
    view_count: int=0
    is_published: bool=True
    auther: User # Nested User model to represent the author of the blog post 
    # Using nested models allows for better organization and validation of related data.

    tags: list[str] = Field(default_factory=list) # Using default_factory to avoid mutable default argument issues
    # Default value for tags is a function that returns a new empty list each time a BlogPost instance is created.

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc)) # Default value is the current date and time in UTC timezone
    # Using a lambda function to ensure a new datetime object is created for each instance.
    # another way to do it is using partial instead of lambda
    # created_at: datetime = Field(default_factory=partial(datetime.now, tz=UTC))

    auther_id: str | int 
    status: Literal["draft", "published", "archived"] = "draft" # Restricting the status field to specific string values

    slug: Annotated[str, Field(pattern=r"^[a-z0-9]+$")]  # Slug must match the given regex pattern (lowercase letters and numbers only)
    # This ensures that the slug is URL-friendly.
    #This Regex Expression r"^[a-z0-9]+$" means the string should start (^) and end ($) with one or more (+) lowercase letters (a-z) or digits (0-9).

class UserRegistration(BaseModel):
    email: EmailStr
    password: SecretStr
    confirm_password: SecretStr

    # Custom model-level validator to ensure password and confirm_password match
    @model_validator(mode="after") # model-level validator, mode="after" means the validator is called after all field-level validation is performed
    def passwords_match(self) -> "UserRegistration": # self is the instance of the UserRegistration model
        if self.password != self.confirm_password: # Check if the passwords match
            raise ValueError("Passwords do not match")
        return self
# try:
#     registration = UserRegistration(
#         email="tamerelkot@gmail.com",
#         password="secret1234",
#         confirm_password="secret1234"
#     )
#     print(registration.email)
# except ValidationError as e:
#     print(e)
user = User(
    username="tamerelkot",
    email="tamerelkot@gmail.com",
    age=22,
    password="secret1234",
    website="tamerelkot.com",
    first_name="Tamer",
    last_name="Elkot",
    follower_count=15000
)
print(user.model_dump_json(indent=2))
# try:
#     user = User(
#         uid= -5,
#         username="ab",
#         email="tamerelkotgmail.com",
#         age=10
#     )

# except ValidationError as e:
#     print(e)

# post = BlogPost(
#     title="My first blog post",
#     content= "this is the content of my first blog post",
#     auther_id=1
# )

# print(post)

import secrets
print(secrets.token_urlsafe(32))