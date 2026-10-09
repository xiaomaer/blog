import pytest
from pydantic import ValidationError

from python_backend_scaffold.user import User, check_user


def test_check_user_returns_name_and_uppercase_status_for_admin() -> None:
    user_data = {"name": "Alex", "role": "admin", "status": "active"}

    assert check_user(user_data) == ("Alex", "ACTIVE")


def test_check_user_returns_user_model_for_regular_user() -> None:
    user_data = {"name": "Bob", "role": "user", "status": "active"}

    result = check_user(user_data)

    assert isinstance(result, User)
    assert result.model_dump() == user_data


@pytest.mark.parametrize("role", ["admin", "user"])
def test_check_user_rejects_inactive_user(role: str) -> None:
    user_data = {"name": "Alex", "role": role, "status": "inactive"}

    with pytest.raises(ValueError, match="^User is not active$"):
        check_user(user_data)


@pytest.mark.parametrize("missing_field", ["name", "role", "status"])
def test_check_user_rejects_missing_required_field(missing_field: str) -> None:
    user_data = {"name": "Charlie", "role": "user", "status": "active"}
    del user_data[missing_field]

    with pytest.raises(ValidationError) as exc_info:
        check_user(user_data)

    error = exc_info.value.errors()[0]
    assert error["loc"] == (missing_field,)
    assert error["type"] == "missing"
