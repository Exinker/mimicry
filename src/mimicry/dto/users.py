from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class UserDTO(BaseModel):

    nickname: str
    password: str
    email: str
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)
    is_admin: bool = Field(default=False)

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
    )
