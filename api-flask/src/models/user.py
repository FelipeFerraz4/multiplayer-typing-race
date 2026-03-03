from flask_restx import fields
from server import server

user_model = server.api.model(
    "User",
    {
        "id": fields.String(
            required=True,
            description="User UUID",
            example="550e8400-e29b-41d4-a716-446655440001"
        ),

        "name": fields.String(
            required=True,
            description="User name",
            example="Felipe"
        ),

        "is_host": fields.Boolean(
            required=True,
            description="Indicates if the user is the room host",
            example=True
        ),

        "avatar_id": fields.Integer(
            required=True,
            description="Avatar identifier",
            example=1
        ),
    }
)