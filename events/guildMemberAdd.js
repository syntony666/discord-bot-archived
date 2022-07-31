const guilds = require('../database/model/guildModel');
const { MessageEmbed } = require('discord.js');

module.exports = {
    name: 'guildMemberAdd',
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
                .setDescription(res.join_message.replace('{m}', `<@${member.id}>`))
                .setFooter({ text: member.user.tag, iconURL: member.user.avatarURL() })
                .setTimestamp();
            member.guild.channels.cache.get(res.join_channel_id).send({embeds: [embed]});
        })
    }
}
