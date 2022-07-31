const guilds = require('../database/model/guildModel');

module.exports = {
    name: 'guildCreate',
    async execute(guild) {
        guilds.findAll({
            where: {
                guild_id: interaction.guild.id
            }
        }).then(res => {
            if (res.length == 0) {
                guild.create({ guild_id: guild });
            }
        })
    }
}
