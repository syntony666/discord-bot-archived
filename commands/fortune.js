const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed, MessageAttachment } = require('discord.js');

const cards = [
    "大吉", "中吉", "小吉", "末吉", "凶", "大凶"
];

const cardImage = {
    '大吉': 'fortune1.png',
    '中吉': 'fortune2.png',
    '小吉': 'fortune3.png',
    '末吉': 'fortune4.png',
    '凶': 'fortune5.png',
    '大凶': 'fortune6.png'
}

module.exports = {
    data: new SlashCommandBuilder()
        .setName('fortune')
        .setDescription('運勢占卜')
        .addStringOption(option => {
            return option
                .setName('description')
                .setDescription('你有什麼想說的嗎？')
                .setRequired(false)
        }),
    async execute(interaction) {
        let embed = new MessageEmbed()
            .setColor('#bf3b5e')
            .setAuthor({ name: interaction.client.user.username, iconURL: interaction.client.user.avatarURL() })
            .setFooter({ text: interaction.user.tag, iconURL: interaction.user.avatarURL() })
            .setTimestamp();
        const description = interaction.options.get('description') ? interaction.options.get('description').value : null;
        const random = Math.floor(Math.random() * cards.length);
        const choice = cards[random];
        const image = new MessageAttachment('./assets/' + cardImage[choice]);
        embed.setImage('attachment://' + cardImage[choice])
        if (description) {
            embed.setDescription(description);
        }
        interaction.reply({ embeds: [embed], files: [image] });
    }
}