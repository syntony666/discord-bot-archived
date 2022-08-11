const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('choose')
        .setDescription('選擇困難症解藥')
        .addStringOption(option => {
            return option
                .setName('choice01')
                .setDescription('選項 1')
                .setRequired(true)
        })
        .addStringOption(option => {
            return option
                .setName('choice02')
                .setDescription('選項 2')
                .setRequired(true)
        })
        .addStringOption(option => {
            return option
                .setName('choice03')
                .setDescription('選項 3')
                .setRequired(false)
        })
        .addStringOption(option => {
            return option
                .setName('choice04')
                .setDescription('選項 4')
                .setRequired(false)
        })
        .addStringOption(option => {
            return option
                .setName('choice05')
                .setDescription('選項 5')
                .setRequired(false)
        }),
    async execute(interaction) {
        let embed = new MessageEmbed()
            .setColor('#bf3b5e')
            .setAuthor({ name: interaction.client.user.username, iconURL: interaction.client.user.avatarURL() })
            .setFooter({ text: interaction.user.tag, iconURL: interaction.user.avatarURL() })
            .setTimestamp();
        const choices = [
            interaction.options.get('choice01') ? interaction.options.get('choice01').value : null,
            interaction.options.get('choice02') ? interaction.options.get('choice02').value : null,
            interaction.options.get('choice03') ? interaction.options.get('choice03').value : null,
            interaction.options.get('choice04') ? interaction.options.get('choice04').value : null,
            interaction.options.get('choice05') ? interaction.options.get('choice05').value : null
        ].filter(choice => choice != null);
        const random = Math.floor(Math.random() * choices.length);
        const choice = choices[random];
        let embedChioceValue = '所有選項:\n\`\`\`';
        let count = 1;
        choices.forEach(s => {embedChioceValue += `${count}. ${s}\n`; count++;});
        embedChioceValue += '\`\`\`';
        embed.setTitle(choice)
            .setFields({ name: '\u200B', value: embedChioceValue });
        interaction.reply({ embeds: [embed] });
    }
}