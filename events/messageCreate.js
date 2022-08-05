const reply = require('../database/model/replyModel');

module.exports = {
    name: 'messageCreate',
    async execute(message) {
        if (!message.author.bot){
            reply.findOne({
                where: {
                    guild_id: message.guild.id,
                    request: message.content
                }
            }).then(msg => {
                if (msg.response !== null) {
                    message.reply(msg.response);
                    console.log(`${message.content} ===> ${msg.response}`);
                }
            }).catch(err => { });
        }
    },
};
