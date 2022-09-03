const { SlashCommandBuilder } = require("@discordjs/builders");
const { MessageEmbed, Formatters } = require('discord.js');

function getBaseEmbed(interaction) {
    return new MessageEmbed()
        .setColor('#3d3d3d');
}

module.exports = {
    data: new SlashCommandBuilder()
        .setName('say')
        .setDescription('直接叫機器人幫你發話')
        .addStringOption(option => {
            return option
                .setName('input')
                .setDescription('輸入你要叫機器人說的話')
                .setRequired(true)
        })
        .addChannelOption(option => {
            return option
            .setName('channel')
            .setDescription('設定說話頻道')
            .setRequired(true)
        }),
    async execute(interaction) {
        const channelId = interaction.options.get('channel').channel.id
        const message = interaction.options.get('input').value
        let replyEmbed = getBaseEmbed(interaction)
            .setAuthor({ name: interaction.client.user.username, iconURL: interaction.client.user.avatarURL() })
            .setTitle('訊息內容已傳送')
            .setDescription('又在叫我做奇怪的事情...')
            .addFields(
                {name: '訊息內容', value: message},
                {name: '頻道', value: Formatters.channelMention(channelId)}
            )
            .setFooter({ text: interaction.user.tag, iconURL: interaction.user.avatarURL() })
            .setTimestamp();
        let embed = getBaseEmbed(interaction)
            .setDescription(message)
            .setAuthor({ name: interaction.user.tag, iconURL: interaction.user.avatarURL() })
        interaction.reply({ embeds: [replyEmbed], ephemeral: false })
        interaction.guild.channels.cache.get(channelId).send({embeds: [embed]});
    }
}