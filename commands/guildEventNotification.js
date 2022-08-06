const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed, Permissions, Formatters } = require('discord.js');

const guild = require('../database/model/guildModel');

function off(interaction, embed, title, updateColumn) {
    guild.update(
        updateColumn,
        { where: { guild_id: interaction.guild.id } }
    ).then(() => {
        embed.setTitle(`${title}已關閉`);
        interaction.reply({ embeds: [embed], ephemeral: false });
    }).catch(err => {
        interaction.reply({ content: '關閉成員加入通知失敗，可能是資料庫損壞', ephemeral: true });
        console.log(err);
    })
}

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

        })
        .addSubcommand(subcommand => {
            return subcommand
                .setName('delete-message')
                .setDescription('刪除訊息通知')
                .addChannelOption(option => {
                    return option
                        .setName('channel')
                        .setDescription('設定通知頻道')
                        .setRequired(true)
                })
        })
        .addSubcommand(subcommand => {
            return subcommand
                .setName('off')
                .setDescription('關閉通知')
                .addStringOption(option => {
                    return option
                        .setName('type')
                        .setDescription('選擇要關閉的通知 (關閉後若要重新開啟需重新設定)')
                        .addChoices(
                            {name: '伺服器成員加入通知', value: 'join'},
                            {name: '伺服器成員離開通知', value: 'leave'},
                            {name: '訊息刪除通知', value: 'message-delete'}
                        )
                        .setRequired(true)
                })
        })
        .addSubcommand(subcommand => {
            return subcommand
                .setName('list')
                .setDescription('查看通知設定')
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
                        { name: '頻道', value: Formatters.channelMention(channel.id), inline: true },
                        { name: '測試訊息', value: message.replace('{m}', Formatters.userMention(interaction.user.id)), inline: true }
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
                        { name: '頻道', value: Formatters.channelMention(channel.id), inline: true },
                        { name: '測試訊息', value: message.replace('{m}', `${interaction.user.tag}`), inline: true }
                    );
                interaction.reply({ embeds: [embed], ephemeral: false });
            }).catch(err => {
                interaction.reply({ content: '設定成員離開通知失敗，可能是資料庫損壞', ephemeral: true });
                console.log(err);
            })
        } else if (interaction.options.getSubcommand() == 'delete-message') {
            const channel = interaction.options.get('channel').channel;
            guild.update(
                { delete_notification_channel_id: channel.id },
                { where: { guild_id: interaction.guild.id } }
            ).then(() => {
                embed.setTitle('訊息刪除通知已設定')
                    .setFields(
                        { name: '頻道', value: Formatters.channelMention(channel.id), inline: true }
                    );
                interaction.reply({ embeds: [embed], ephemeral: false });
            }).catch(err => {
                interaction.reply({ content: '設定訊息刪除通知失敗，可能是資料庫損壞', ephemeral: true });
                console.log(err);
            })
        } else if (interaction.options.getSubcommand() == 'off') {
            const type = interaction.options.get('type').value;
            if (type == 'join') {
                off(interaction, embed, '成員加入通知', { join_channel_id: null, join_message: null });
            } else if (type == 'leave') {
                off(interaction, embed, '成員離開通知', { leave_channel_id: null, leave_message: null });
            } else if (type == 'message-delete') {
                off(interaction, embed, '訊息刪除通知', { delete_notification_channel_id: null });
            }
        } else if (interaction.options.getSubcommand() == 'list') {
            guild.findOne({
                where: {
                    guild_id: interaction.guild.id
                }
            }).then(guild => {
                const join = {
                    name: (guild.join_channel_id ? '✅' : '❎') + ' 成員加入通知',
                    value: guild.join_channel_id ? 
                        `**發送頻道:**\n> ${Formatters.channelMention(guild.join_channel_id)}\n**測試訊息:**\n> ${guild.join_message.replace('{m}', Formatters.userMention(interaction.user.id))}` : '\u200B'
                };
                const leave = {
                    name: (guild.leave_channel_id ? '✅' : '❎') + ' 成員離開通知',
                    value: guild.leave_channel_id ? 
                        `**發送頻道:**\n> ${Formatters.channelMention(guild.leave_channel_id)}\n**測試訊息:**\n> ${guild.leave_message.replace('{m}', interaction.user.tag)}` : '\u200B'
                };
                const delete_notification = {
                    name: (guild.delete_notification_channel_id ? '✅' : '❎') + ' 訊息刪除通知',
                    value: guild.delete_notification_channel_id ? `**發送頻道:**\n> ${Formatters.channelMention(guild.delete_notification_channel_id)}` : '\u200B'
                };
                embed.setTitle('通知設定')
                    .setFields(
                        join, leave, delete_notification
                    );
                interaction.reply({ embeds: [embed], ephemeral: false });
            }).catch(err => { 
                console.log(err);
            })
        }
    }
}