const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed, Permissions } = require('discord.js');

const guild = require('../database/model/guildModel');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('notif')
        .setDescription('設定伺服器成員加入/離開通知')
        .setDefaultMemberPermissions(Permissions.FLAGS.ADMINISTRATOR)
        .addSubcommand(subcommand => {
            return subcommand
                .setName('join')
                .setDescription('加入通知')
                .addChannelOption(option => {
                    return option
                        .setName('channel')
                        .setDescription('設定通知頻道')
                        .setRequired(true)
                })
                .addStringOption(option => {
                    return option
                        .setName('message')
                        .setDescription('設定通知訊息')
                        .setRequired(true)
                })
        })
        .addSubcommand(subcommand => {
            return subcommand
                .setName('leave')
                .setDescription('離開通知')
                .addChannelOption(option => {
                    return option
                        .setName('channel')
                        .setDescription('設定通知頻道')
                        .setRequired(true)
                })
                .addStringOption(option => {
                    return option
                        .setName('message')
                        .setDescription('設定通知訊息')
                        .setRequired(true)
                })

        }),
    async execute(interaction) {
        let embed = new MessageEmbed()
            .setColor('#f58e69')
            .setAuthor({ name: interaction.client.user.username, iconURL: interaction.client.user.avatarURL() })
            .setDescription('事情都我在幫你做 = =')
            .setFooter({ text: interaction.user.tag, iconURL: interaction.user.avatarURL() })
            .setTimestamp();
        if (interaction.options.getSubcommand() == 'join') {
            const channel = interaction.options.get('channel').channel;
            const message = interaction.options.get('message').value;
            guild.update(
                { join_channel_id: channel.id, join_message: message },
                { where: { guild_id: interaction.guild.id } }
            ).then(() => {
                embed.setTitle('成員加入通知已設定')
                    .setFields(
                        { name: '頻道', value: `<#${channel.id}>`, inline: true },
                        { name: '測試訊息', value: message.replace('{m}', `<@${interaction.user.id}>`), inline: true }
                    );
                interaction.reply({ embeds: [embed], ephemeral: false });
            }).catch(err => {
                interaction.reply({ content: '設定成員加入通知失敗，可能是資料庫損壞', ephemeral: true });
                console.log(err);
            })
        } else if (interaction.options.getSubcommand() == 'leave') {
            const channel = interaction.options.get('channel').channel;
            const message = interaction.options.get('message').value;
            guild.update(
                { leave_channel_id: channel.id, leave_message: message },
                { where: { guild_id: interaction.guild.id } }
            ).then(() => {
                embed.setTitle('成員離開通知已設定')
                    .setFields(
                        { name: '頻道', value: `<#${channel.id}>`, inline: true },
                        { name: '測試訊息', value: message.replace('{m}', `${interaction.user.tag}`), inline: true }
                    );
                interaction.reply({ embeds: [embed], ephemeral: false });
            }).catch(err => {
                interaction.reply({ content: '設定成員離開通知失敗，可能是資料庫損壞', ephemeral: true });
                console.log(err);
            })
        }
    }
}