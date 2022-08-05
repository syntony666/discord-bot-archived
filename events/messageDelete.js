const { MessageEmbed } = require('discord.js');
const guild = require('../database/model/guildModel');

module.exports = {
    name: 'messageDelete',
    async execute(message) {
        if (message.author != null && !message.author.bot){
            guild.findOne({
                where: {
                    guild_id: message.guild.id,
                }
            }).then(res => {
                let embed = new MessageEmbed()
                    .setColor('#f58e69')
                    .setAuthor({ name: message.guild.name, iconURL: message.guild.iconURL() })
                    .setDescription('又...又刪!!!')
                    .setTimestamp();
                if (res.delete_notification_channel_id != null && !message.author.bot) {
                    embed.addFields(
                        { name: '傳送者', value: `<@${message.author.tag}>`, inline: true },
                        { name: '頻道', value: `<#${message.channel.id}>`, inline: true },
                        { name: '內容', value: `${message.content}` }
                    );
                    message.guild.channels.cache.get(res.delete_notification_channel_id).send({embeds: [embed]});
                    console.log(`deleted message ===> message.content: ${message.content}`);
                }
            }).catch(err => { });
        }
    },
};