"""
test_database.py

Author: Joseph Maclean Arhin
"""


def test_sql_initialization(app_with_model):
    """
    test database initialization
    :param app_with_model:
    :return:
    """

    model_klass = app_with_model

    details = model_klass(**{"name": "maclean"})
    details.save()
    user_id = details.id
    saved_user = model_klass.get_by_id(user_id)
    assert saved_user.name == "maclean"
