const { MessageActionRow, MessageButton } = require('discord.js');

const buttonEmojis = {
    'first': '⏪',
    'previous': '◀',
    'next': '▶',
    'last': '⏩'
}

const buttonStyles = {
    first: "PRIMARY",
    previous: "PRIMARY",
    next: "PRIMARY",
    last: "PRIMARY",
}

module.exports = async (interaction, pages, time = 60000) => {
    let index = 0;
    let buttons = new MessageActionRow()
        .addComponents(new MessageButton().setCustomId('first').setEmoji(buttonEmojis.first).setStyle(buttonStyles.first).setDisabled(index == 0))
        .addComponents(new MessageButton().setCustomId('previous').setEmoji(buttonEmojis.previous).setStyle(buttonStyles.previous).setDisabled(index == 0))
        .addComponents(new MessageButton().setCustomId('next').setEmoji(buttonEmojis.next).setStyle(buttonStyles.next).setDisabled(index == pages.length - 1))
        .addComponents(new MessageButton().setCustomId('last').setEmoji(buttonEmojis.last).setStyle(buttonStyles.last).setDisabled(index == pages.length - 1));
    let data = {
        embeds: [pages[index]],
        components: [buttons],
        fetchReply: true,
        ephemeral: true
    }
    const msg = interaction.replied ? await interaction.followUp(data) : await interaction.reply(data);
    console.log(msg);
    const collector = msg.createMessageComponentCollector({
        time: time
    });
    collector.on('collect', res => {
        if (res.customId == 'first') {
            index = 0;
        } else if (res.customId == 'previous') {
            index--;
        } else if (res.customId == 'next') {
            index++;
        } else if (res.customId == 'last') {
            index = pages.length - 1;
        }
        console.log(index);
        buttons = new MessageActionRow()
            .addComponents(new MessageButton().setCustomId('first').setEmoji(buttonEmojis.first).setStyle(buttonStyles.first).setDisabled(index == 0))
            .addComponents(new MessageButton().setCustomId('previous').setEmoji(buttonEmojis.previous).setStyle(buttonStyles.previous).setDisabled(index == 0))
            .addComponents(new MessageButton().setCustomId('next').setEmoji(buttonEmojis.next).setStyle(buttonStyles.next).setDisabled(index == pages.length - 1))
            .addComponents(new MessageButton().setCustomId('last').setEmoji(buttonEmojis.last).setStyle(buttonStyles.last).setDisabled(index == pages.length - 1));
        res.update({
            components: [buttons],
            embeds: [pages[index]],
        })
    });
}