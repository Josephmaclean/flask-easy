"""
test_database.py

Author: Joseph Maclean Arhin
"""


def test_initialization(app_with_model):
    from flask_easy import db, fields

    User = app_with_model

    details = User(**{"name": "maclean"})
    details.save()
    user_id = details.id
    saved_user = User.get_by_id(user_id)
    assert(saved_user.name, "maclean")
