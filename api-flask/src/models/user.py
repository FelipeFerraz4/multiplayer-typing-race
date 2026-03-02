from flask_restx import fields
from server import server

user_model = server.api.model(
    "User",
    {
        "id": fields.String(
            required=True,
            description="User identifier",
            example="7392"
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
