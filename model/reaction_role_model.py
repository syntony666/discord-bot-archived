class ReactionRoleModel:
    def __init__(self, guild_id: str, role_id: str, message_id: str, emoji: str):
        self.guild = guild_id
        self.role = role_id
        self.message = message_id
        self.emoji = emoji
