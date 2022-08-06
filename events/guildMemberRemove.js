const guilds = require('../database/model/guildModel');
const { MessageEmbed } = require('discord.js');

module.exports = {
    name: 'guildMemberRemove',
    async execute(member) {
        guilds.findOne({
            where: {
                guild_id: member.guild.id
            }
        }).then(res => {
            if (res == null) return;
            const embed = new MessageEmbed()
                .setColor('#f58e69')
                .setAuthor({ name: member.guild.name, iconURL: member.guild.iconURL() })
                .setDescription(res.leave_message.replace('{m}', `${member.user.tag}`))
                .setFooter({ text: member.user.tag, iconURL: member.user.avatarURL() })
                .setTimestamp();
            member.guild.channels.cache.get(res.leave_channel_id).send({embeds: [embed]});
        })
    }
}
