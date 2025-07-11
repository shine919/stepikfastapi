from pydantic import BaseModel, EmailStr


class User(BaseModel):
    username: str
    email: EmailStr = None
    password: str


class UserCreate(User):
    pass


class UserLogin(BaseModel):
    username: str
    password: str


# class UserAgeResponse(User):
#     @computed_field
#     @property
#     async def is_adult(self)->bool:
#         return self.age >= 18

# class Feedback(BaseModel):
#     name : str = Field(min_length=2, max_length=50)
#     message : str = Field(min_length=10, max_length=500)
#     contact : Contact
#
#     @field_validator("message",mode='before')
#     def validate_message(cls,value):
#         forbidden_words = ["редиска", "бяка", "козявка"]
#         pattern = r'\b(?:' + '|'.join(w[:-1] for w in forbidden_words) + '(а|и|е|у|ой|ою)' + r')\w*\b'
#         for word in forbidden_words:
#             if re.search(pattern, value.lower()):
#                 raise ValueError(f"Слово '{word}' запрещено в поле message")
#
#
#         return value
#
