const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageAttachment, MessageEmbed } = require('discord.js');

const {version} = require('../package.json');


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
            const exampleEmbed = new MessageEmbed()
                .setColor('#0099ff')
                .setTitle('工具人')
                .setAuthor({ name: '自我介紹', iconURL: 'attachment://logo.png' })
                .setDescription('我是可憐的廉價勞工')
                .setThumbnail('attachment://avatar_bg.png')
                .addFields(
                    { name: '使用說明', value: 'https://discord-bot.syntony666.com/' },
                    { name: '\u200B', value: '\u200B' },
                    { name: 'Bot Ping', value: `${Date.now() - interaction.createdAt} ms`, inline: true },
                    { name: 'API Ping', value: `${interaction.client.ws.ping} ms`, inline: true },
                )
                .setTimestamp()
                .setFooter({ text: `ver. ${version}`, iconURL: 'attachment://discord_js.png' });

            interaction.reply({ embeds: [exampleEmbed], files: [avatar_bg, logo, discord_js], ephemeral: false });
        }
        else {
            await interaction.reply({content: `指令錯誤: ${interaction.option.getContent()}`, ephemeral: true });
        }
    },
};