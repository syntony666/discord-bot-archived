const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageAttachment, MessageEmbed } = require('discord.js');

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
        if (interaction.options.getSubcommand() == 'bot') {
            const avatar_bg = new MessageAttachment('./assets/avatar_bg.png');
            const logo = new MessageAttachment('./assets/logo.png');
            const discord_js = new MessageAttachment('./assets/discord_js.png');
            const embed = new MessageEmbed()
                .setColor('#0099ff')
                .setTitle(interaction.client.user.username)
                .setAuthor({ name: '自我介紹', iconURL: 'attachment://logo.png' })
                .setDescription('做這種事才不是為了你呢...!')
                .setThumbnail('attachment://avatar_bg.png')
                .addFields(
                    { name: 'Bot Ping', value: `\`${Date.now() - interaction.createdAt} ms\``, inline: true },
                    { name: 'API Ping', value: `\`${interaction.client.ws.ping} ms\``, inline: true },
                    { name: '\u200B', value: '\u200B' },
                    { name: '使用說明', value: 'https://discord.com/' },
                    // { name: '使用說明', value: 'https://discord-bot.syntony666.com/' },
                    { name: '人家才沒有很希望進你的伺服器呢!!', value: '[邀請連結](https://discord.com/api/oauth2/authorize?client_id=995551157151862854&permissions=1644971945463&scope=bot)' },
                )
                .setTimestamp()
                .setFooter({ text: `ver. ${version}`, iconURL: 'attachment://discord_js.png' });

            interaction.reply({ embeds: [embed], files: [avatar_bg, logo, discord_js], ephemeral: false });
        }
        else {
            await interaction.reply({ content: `指令錯誤: ${interaction.option.getContent()}`, ephemeral: true });
        }
    },
};