class User:
    def __init__(self, user_id, name, email, is_verified=False, is_admin=False):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.is_verified = is_verified
        self.is_admin = is_admin

    def to_dict(self):
        """Convert user object to a dictionary."""
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "is_verified": self.is_verified,
            "is_admin": self.is_admin
        }

    @classmethod
    def from_dict(cls, data):
        """Create a user object from a dictionary."""
        return cls(
            user_id=data.get("user_id"),
            name=data.get("name"),
            email=data.get("email"),
            is_verified=data.get("is_verified", False),
            is_admin=data.get("is_admin", False)
        )

    def __str__(self):
        return f"User({self.user_id}, {self.name}, {self.email}, Verified: {self.is_verified}, Admin: {self.is_admin})"
