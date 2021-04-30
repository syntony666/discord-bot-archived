class ConfigModel:
    def __init__(self, guild_id: str, join_channel, join_message, remove_channel, remove_message):
        self.guild_id = guild_id
        self.join_channel = join_channel
        self.join_message = join_message
        self.remove_channel = remove_channel
        self.remove_message = remove_message
