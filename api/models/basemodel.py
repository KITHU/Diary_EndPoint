"""Module for Base Model"""
from datetime import datetime

from .modeloperations import ModelOperations
from .database import db


class BaseModel(db.Model, ModelOperations):
    """ Base model for all database models.
    attributes:
        id (string, reserved):
             a unique identifier for each instance. Autogenerated.
        deleted (bool, required):
            a flag for soft deletion of model instances.
    """

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, nullable=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted = db.Column(db.Boolean, nullable=True, default=False)
