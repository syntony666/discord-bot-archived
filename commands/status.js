const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageAttachment, MessageEmbed, MessageButton, MessageActionRow, Formatters } = require('discord.js');

const { version } = require('../package.json');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('status')
        .setDescription('取得相關資訊')
        .addSubcommand(subcommand => {
            return subcommand
                .setName('bot')
                .setDescription('取得機器人資訊')
        })
        .addSubcommand(subcommand => {
            return subcommand
                .setName('server')
                .setDescription('取得伺服器資訊')
        }),
    async execute(interaction) {
        const avatar_bg = new MessageAttachment('./assets/avatar_bg.png');
        const logo = new MessageAttachment('./assets/logo.png');
        const discord_js = new MessageAttachment('./assets/discord_js.png');
        if (interaction.options.getSubcommand() == 'bot') {
            const embed = new MessageEmbed()
                .setColor('#0099ff')
                .setTitle(interaction.client.user.username)
                .setAuthor({ name: '自我介紹', iconURL: 'attachment://logo.png' })
                .setDescription('做這種事才不是為了你呢...!')
                .setThumbnail('attachment://avatar_bg.png')
                .addFields(
                    { name: 'Bot Ping', value: `\`${Date.now() - interaction.createdAt} ms\``, inline: true },
                    { name: 'API Ping', value: `\`${interaction.client.ws.ping} ms\``, inline: true }
                )
                .setTimestamp()
                .setFooter({ text: `ver. ${version}`, iconURL: 'attachment://discord_js.png' });
            const buttons = new MessageActionRow()
                .addComponents(
                    new MessageButton()
                        .setLabel('使用說明').setURL('https://discord-bot.syntony666.com/')
                        .setStyle('LINK')
                )
                .addComponents(
                    new MessageButton()
                        .setLabel('邀請連結').setURL('https://discord.com/api/oauth2/authorize?client_id=995551157151862854&permissions=1644971945463&scope=bot')
                        .setStyle('LINK')
                )
            interaction.reply({ embeds: [embed], files: [avatar_bg, logo, discord_js], components: [buttons], ephemeral: false });
        } else if (interaction.options.getSubcommand() == 'server') {
            interaction.guild.fetchOwner()
                .then(owner => {
                    return owner.user.tag;
                }).then(ownerTag => {
                    const embed = new MessageEmbed()
                        .setColor('#0099ff')
                        .setTitle(interaction.guild.name)
                        .setAuthor({ name: '伺服器資訊', iconURL: 'attachment://logo.png' })
                        .setFields(
                            { name: '伺服器擁有者', value: ownerTag, inline: true },
                            { name: '創立時間', value: Formatters.time(interaction.guild.createdAt), inline: true },
                            { name: '成員數量', value: `${interaction.guild.memberCount}`, inline: false },
                        )
                        .setThumbnail(interaction.guild.iconURL())
                        .setTimestamp()
                        .setFooter({ text: interaction.user.tag, iconURL: interaction.user.avatarURL() });
                    interaction.reply({ embeds: [embed], files: [logo], ephemeral: false });
                })
        } else {
            await interaction.reply({ content: `指令錯誤: ${interaction.option.getContent()}`, ephemeral: true });
        }
    },
};