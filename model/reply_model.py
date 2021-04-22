class ReplyModel:
    def __init__(self, guild_id: str, receive: str, send: str):
        self.guild_id = guild_id
        self.receive = receive
        self.send = send
