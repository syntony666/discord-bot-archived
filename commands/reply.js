const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed, Formatters } = require('discord.js');
const Sequelize = require('sequelize');

const reply = require('../database/model/replyModel');
const pageService = require('../service/pageService');

function displayReplyResult(embedTitle, queryResult, interaction) {
    if (queryResult.length == 0) {
        interaction.reply({ content: '目前沒有任何回覆內容', ephemeral: true });
    } else {
        let replyList = queryResult.map(item => {
            let last_editor = item.last_editor_id ? `> ${Formatters.userMention(item.last_editor_id)}\n` : '';
            let value = last_editor + item.response;
            return { name: item.request, value: value }
        });
        let embedFields = [], embedList = [];
        while (replyList.length > 0) {
            embedFields.push(replyList.splice(0, 10));
        }
        let page = 1;
        embedFields.forEach(field => {
            let embed = new MessageEmbed()
                .setColor('#f0b01d')
                .setTitle(embedTitle)
                .setAuthor({ name: interaction.user.username, iconURL: interaction.user.avatarURL() })
                .setDescription('這些回答都不是我自願的...')
                .setFooter({ text: `page ${(page++)}/${(embedFields.length)} · total: ${queryResult.length}`, iconURL: interaction.client.user.avatarURL() })
                .addFields(field);
            embedList.push(embed);
        })
        pageService(interaction, embedList);
    }
}

module.exports = {
    data: new SlashCommandBuilder()
        .setName('reply')
        .setDescription('設定回覆功能')
        .addSubcommand(subcommand => {
            return subcommand
                .setName('add')
                .setDescription('新增回覆內容')
                .addStringOption(option => {
                    return option
                        .setName('input')
                        .setDescription('輸入關鍵字')
                        .setRequired(true)
                })
                .addStringOption(option => {
                    return option
                        .setName('output')
                        .setDescription('輸入回覆內容')
                        .setRequired(true)
                })
        })
        .addSubcommand(subcommand => {
            return subcommand
                .setName('edit')
                .setDescription('編輯回覆內容')
                .addStringOption(option => {
                    return option
                        .setName('input')
                        .setDescription('輸入關鍵字')
                        .setRequired(true)
                })
                .addStringOption(option => {
                    return option
                        .setName('output')
                        .setDescription('輸入回覆內容')
                        .setRequired(true)
                })
        })
        .addSubcommand(subcommand => {
            return subcommand
                .setName('remove')
                .setDescription('移除回覆內容')
                .addStringOption(option => {
                    return option
                        .setName('input')
                        .setDescription('輸入關鍵字')
                        .setRequired(true)
                })
        })
        .addSubcommand(subcommand => {
            return subcommand
                .setName('search')
                .setDescription('從關鍵字搜尋回覆內容')
                .addStringOption(option => {
                    return option
                        .setName('input')
                        .setDescription('輸入關鍵字')
                        .setRequired(true)
                })
        })
        .addSubcommand(subcommand => {
            return subcommand
                .setName('list')
                .setDescription('列出所有的回應內容')
        }),
    async execute(interaction) {
        let embed = new MessageEmbed()
            .setColor('#f0b01d')
            .setAuthor({ name: interaction.client.user.username, iconURL: interaction.client.user.avatarURL() })
            .setDescription('又在教我奇怪的東西了...')
            .setFooter({ text: interaction.user.tag, iconURL: interaction.user.avatarURL() })
            .setTimestamp();

        if (interaction.options.getSubcommand() == 'add') {
            const input = interaction.options.get('input').value;
            const output = interaction.options.get('output').value;
            reply.create({
                guild_id: interaction.guild.id,
                last_editor_id: interaction.user.id,
                request: input,
                response: output
            }).then(() => {
                embed.setTitle('回覆內容已新增')
                    .setFields(
                        { name: '關鍵字', value: input, inline: true },
                        { name: '回覆內容', value: output, inline: true },
                    )
                interaction.reply({ embeds: [embed], ephemeral: false });
            }).catch(err => {
                if (err.name == 'SequelizeUniqueConstraintError') {
                    interaction.reply({ content: '關鍵字已重複', ephemeral: true });
                } else {
                    interaction.reply({ content: '回覆內容新增失敗，可能是資料庫損壞', ephemeral: true });
                }
            });
        } else if (interaction.options.getSubcommand() == 'edit') {
            const input = interaction.options.get('input').value;
            const output = interaction.options.get('output').value;
            reply.findOne({
                where: {
                    request: input,
                    guild_id: interaction.guild.id
                }
            }).then(item => {
                if (item) {
                    item.update({
                        last_editor_id: interaction.user.id,
                        response: output
                    }).then(() => {
                        embed.setTitle('回覆內容已修改')
                            .setFields(
                                { name: '關鍵字', value: input, inline: true },
                                { name: '回覆內容', value: output, inline: true },
                            )
                        interaction.reply({ embeds: [embed], ephemeral: false });
                    }).catch(err => {
                        if (err.name == 'SequelizeUniqueConstraintError') {
                            interaction.reply({ content: '關鍵字已重複', ephemeral: true });
                        } else {
                            interaction.reply({ content: '回覆內容新增失敗，可能是資料庫損壞', ephemeral: true });
                        }
                    });
                }
                else {
                    interaction.reply({ content: '找不到該關鍵字', ephemeral: true });
                }
            })
        } else if (interaction.options.getSubcommand() == 'remove') {
            var input = interaction.options.get('input').value;
            reply.destroy({
                where: {
                    guild_id: interaction.guild.id,
                    request: input
                }
            }).then(res => {
                if (res != 0) {
                    embed.setTitle('回覆內容已移除')
                        .setFields(
                            { name: '關鍵字', value: input }
                        )
                    interaction.reply({ embeds: [embed], ephemeral: false });
                } else {
                    interaction.reply({ content: '回覆內容不存在', ephemeral: true });
                }
            }).catch(err => {
                interaction.reply({ content: '回覆內容移除失敗，可能是資料庫損壞', ephemeral: true });
                console.log(err);
            });
        } else if (interaction.options.getSubcommand() == 'search') {
            reply.findAll({
                where: {
                    guild_id: interaction.guild.id,
                    request: { [Sequelize.Op.substring]: interaction.options.get('input').value }
                }
            }).then(res => {
                displayReplyResult(`查詢結果: ${interaction.options.get('input').value}`, res, interaction);
            });
        } else if (interaction.options.getSubcommand() == 'list') {
            reply.findAll({
                where: {
                    guild_id: interaction.guild.id
                }
            }).then(res => {
                displayReplyResult('回覆內容列表', res, interaction);
            });
        }
        else {
            await interaction.reply({ content: `指令錯誤: ${interaction.option.getContent()}`, ephemeral: true });
        }
    },
};
