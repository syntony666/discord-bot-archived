const { SlashCommandBuilder } = require('@discordjs/builders');
const reply = require('../database/model/replyModel');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('reply')
        .setDescription('設定工具人回覆功能')
        .addSubcommand(subcommand => {
            return subcommand
                .setName('add')
                .setDescription('新增回覆內容，如果有存在的關鍵字，會自行覆蓋新的回應內容')
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
                .setName('list')
                .setDescription('列出所有的回應內容')
        }),
    async execute(interaction) {
        if (interaction.options.getSubcommand() == 'add') {
            var input = interaction.options.get('input').value;
            var output = interaction.options.get('output').value;
            reply.create({
                guild_id: interaction.guild.id,
                request: input,
                response: output
            }).then(() => {
                interaction.reply({ content: '回覆內容已新增', ephemeral: true });
            }).catch(err => {
                interaction.reply({ content: '回覆內容新增失敗，可能是關鍵字已重複或工具人資料庫損壞', ephemeral: true });
                console.log(err);
            });
        }
        else {
            await interaction.reply({content: `指令錯誤: ${interaction.option.getContent()}`, ephemeral: true });
        }
    },
};
