const reactionRole = require('../database/model/reactionRoleModel');

module.exports = {
    name: 'messageReactionRemove',
    async execute(reaction, user) {
        if (reaction.partial) {
            try {
                await reaction.fetch();
            } catch (error) {
                console.error('Something went wrong when fetching the message:', error);
                return;
            }
        }
        if (user.bot) {
            return;
        }
        reactionRole.findOne({
            where: {
                reaction: reaction.emoji.toString(),
                message_url: reaction.message.url
            }
        }).then(res => {
            if (res) {
                reaction.message.guild.members.cache.get(user.id).roles.remove(res.role_id);
            }
        }).catch(err => {
            console.log(err.message);
        })
    },
};
