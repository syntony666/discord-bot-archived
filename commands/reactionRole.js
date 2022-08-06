const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed, Permissions, Formatters } = require('discord.js');

const reactionRole = require('../database/model/reactionRoleModel');
const MessageUrlService = require('../service/messageUrlService');
const pageService = require('../service/pageService');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('reaction-role')
        .setDescription('按下特定訊息上的表情符號可以得到指定的身份組')
        .setDefaultMemberPermissions(Permissions.FLAGS.MANAGE_ROLES)
        .addSubcommand(subcommand => {
            return subcommand
                .setName('add')
                .setDescription('新增要發派的身份組及指定的訊息與表情符號')
                .addRoleOption(option => {
                    return option
                        .setName('role')
                        .setDescription('選擇身份組')
                        .setRequired(true)
                })
                .addStringOption(option => {
                    return option
                        .setName('emoji')
                        .setDescription('輸入表情符號')
                        .setRequired(true)
                })
                .addStringOption(option => {
                    return option
                        .setName('message-url')
                        .setDescription('輸入訊息連結')
                        .setRequired(true)
                })
        })
        .addSubcommand(subcommand => {
            return subcommand
                .setName('remove')
                .setDescription('移除要發派的身份組')
                .addRoleOption(option => {
                    return option
                        .setName('role')
                        .setDescription('選擇身份組')
                        .setRequired(true)
                })
        })
        .addSubcommand(subcommand => {
            return subcommand
                .setName('remove-message')
                .setDescription('移除指定訊息的所有發派的身份組')
                .addStringOption(option => {
                    return option
                        .setName('message-url')
                        .setDescription('輸入訊息連結')
                        .setRequired(true)
                })
        })
        .addSubcommand(subcommand => {
            return subcommand
                .setName('list')
                .setDescription('列出所有的要發派的身份組')
        }),
    async execute(interaction) {
        let embed = new MessageEmbed()
            .setColor('#fa8d2d')
            .setAuthor({ name: interaction.client.user.username, iconURL: interaction.client.user.avatarURL() })
            .setDescription('事情都我在幫你做 = =')
            .setFooter({ text: interaction.user.tag, iconURL: interaction.user.avatarURL() })
            .setTimestamp();
        if (interaction.options.getSubcommand() == 'add') {
            var messageUrlService = new MessageUrlService(interaction.options.get('message-url').value);
            if (!messageUrlService.isVaild()) {
                let error = new Error('message-url is not valid');
                error.name = 'InvalidMessageUrl';
                interaction.reply({ content: '訊息連結不正確', ephemeral: true });
                return;
            }
            const res = {
                roleId: interaction.options.get('role').value,
                emoji: interaction.options.get('emoji').value,
                messageUrl: interaction.options.get('message-url').value,
            }
            interaction.guild.channels.fetch(messageUrlService.getChannelId())
                .then(channel => {
                    return channel.messages.fetch(messageUrlService.getMessageId())
                        .then(message => {
                            return message.react(res.emoji)
                        })
                }).then(() => {
                    return reactionRole.create({
                        role_id: res.roleId,
                        guild_id: interaction.guild.id,
                        reaction: res.emoji,
                        message_url: res.messageUrl
                    })
                }).then(() => {
                    embed.setTitle('身分組已設定')
                        .setFields(
                            { name: '訊息連結', value: res.messageUrl },
                            { name: '身分組', value: Formatters.roleMention(res.roleId), inline: true },
                            { name: '表情符號', value: res.emoji, inline: true }
                        )
                    interaction.reply({ embeds: [embed], ephemeral: false });
                }).catch((err) => {
                    if (err.name == 'SequelizeUniqueConstraintError') {
                        interaction.reply({ content: '身分組已重複設定', ephemeral: true });
                    } else if (err.name == err.message == 'Invalid Form Body') {
                        interaction.reply({ content: '訊息連結不正確', ephemeral: true });
                    } else if (err.message == 'Unknown Emoji') {
                        interaction.reply({ content: '表情符號必須為此伺服器或預設', ephemeral: true });
                    } else {
                        console.log(err);
                        interaction.reply({ content: '身分組設定失敗，可能是資料庫損壞', ephemeral: true });
                    }
                })
        } else if (interaction.options.getSubcommand() == 'remove') {
            let roleId = interaction.options.get('role').value;
            reactionRole.destroy({
                where: {
                    role_id: roleId,
                    guild_id: interaction.guild.id
                }
            }).then(res => {
                if (res != 0) {
                    embed.setTitle('身分組設定已移除')
                        .setFields(
                            { name: '身分組', value: Formatters.roleMention(roleId) }
                        )
                    interaction.reply({ embeds: [embed], ephemeral: false });
                } else {
                    interaction.reply({ content: '此身分組尚未設定', ephemeral: true });
                }
            }).catch(err => {
                interaction.reply({ content: '身分組設定移除失敗，可能是資料庫損壞', ephemeral: true });
                console.log(err);
            });
        } else if (interaction.options.getSubcommand() == 'remove-message') {
            let messageUrl = interaction.options.get('message-url').value;
            let deletedRoles = [];
            reactionRole.findAll({
                where: {
                    guild_id: interaction.guild.id,
                    message_url: messageUrl
                }
            }).then(res => {
                let index = 0;
                let deletedRoleString = '';
                res.forEach(item => {
                    if (index == 0)
                        deletedRoleString += Formatters.roleMention(item.role_id);
                    else
                        deletedRoleString += `, ${Formatters.roleMention(item.role_id)}`;
                    index++;
                })
                deletedRoles.push({ name: '身分組', value: deletedRoleString });
            }).then(() => {
                reactionRole.destroy({
                    where: {
                        message_url: messageUrl,
                        guild_id: interaction.guild.id
                    }
                }).then(res => {
                    if (res != 0) {
                        embed.setTitle('身分組設定已移除')
                            .setFields(deletedRoles)
                        interaction.reply({ embeds: [embed], ephemeral: false });
                    } else {
                        interaction.reply({ content: '此身分組尚未設定', ephemeral: true });
                    }
                })
            }).catch(err => {
                interaction.reply({ content: '身分組設定移除失敗，可能是資料庫損壞', ephemeral: true });
                console.log(err);
            });
        } else if (interaction.options.getSubcommand() == 'list') {
            reactionRole.findAll({
                where: {
                    guild_id: interaction.guild.id
                }
            }).then(res => {
                let roleEmbed = [], embedFields = [], embedList = [];
                res.forEach(item => {
                    roleEmbed.push({ name: '\u200B', value: Formatters.roleMention(item.role_id) });
                    roleEmbed.push({ name: item.reaction, value: `[訊息連結](${item.message_url})` });
                })
                while (roleEmbed.length > 0) {
                    embedFields.push(roleEmbed.splice(0, 10));
                }
                let page = 1;
                embedFields.forEach(field => {
                    let embed = new MessageEmbed()
                    embed.setTitle('身分組列表')
                        .setColor('#fa8d2d')
                        .setAuthor({ name: interaction.user.username, iconURL: interaction.user.avatarURL() })
                        .setDescription('事情都我在幫你做 = =')
                        .setFooter({ text: `page ${(page++)}/${(embedFields.length)} · total: ${res.length}`, iconURL: interaction.client.user.avatarURL() })
                        .addFields(field);
                    embedList.push(embed);
                })
                pageService(interaction, embedList);
            }).catch(err => {
                interaction.reply({ content: '身分組列表讀取失敗，可能是資料庫損壞', ephemeral: true });
                console.log(err);
            });
        }
    }
}