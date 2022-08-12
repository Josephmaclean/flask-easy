"""
test_sql_respository.py

Author: Joseph Maclean Arhin
"""
import pytest

from flask_easy.exc import NotFoundException


def test_create_all(app_with_repository):
    """test create_all method in user_repository"""
    repository_klass = app_with_repository

    repository_klass.create_all([{"name": "maclean"}])
    users = repository_klass.index()
    assert users[0].name == "maclean"


def test_create(app_with_model, app_with_repository):
    """test create method in user repository"""
    repository_klass = app_with_repository
    model_klass = app_with_model
    user = repository_klass.create({"name": "john"})

    saved_user = model_klass.get_by_id(user.id)
    assert saved_user.name == user.name


def test_index(app_with_model, app_with_repository):
    """test index method in user repository"""
    model_klass = app_with_model
    repository_klass = app_with_repository

    user = model_klass.create(name="maclean")
    user.save()

    users = repository_klass.index()
    item_length = len(users)
    assert item_length == 1


def test_find_by_id(app_with_model, app_with_repository):
    """test find by id"""

    model_klass = app_with_model
    repository_klass = app_with_repository
    user = model_klass.create(name="maclean")
    user.save()

    saved_user = repository_klass.find_by_id(user.id)
    assert saved_user.name == user.name


def test_update_by_id(app_with_model, app_with_repository):
    """test update by id"""
    model_klass = app_with_model
    repository_klass = app_with_repository
    user = model_klass.create(name="maclean")
    user.save()

    usr = repository_klass.update_by_id(user.id, {"name": "joe"})
    assert usr.name == "joe"
    updated_user = model_klass.get_by_id(user.id)
    assert updated_user.name == "joe"


def test_delete_by_id(app_with_model, app_with_repository):  # pylint: disable=C0116
    model_klass = app_with_model
    repository_klass = app_with_repository

    user = model_klass.create(name="maclean")
    user.save()

    res = repository_klass.delete_by_id(user.id)
    assert res is True

    with pytest.raises(NotFoundException) as error:
        repository_klass.find_by_id(user.id)

    assert error.value.args[0] == f"Object of id {user.id} not found in model <User>"
