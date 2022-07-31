const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed, Permissions } = require('discord.js');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('clear')
        .setDescription('批次刪除訊息')
        .setDefaultMemberPermissions(Permissions.FLAGS.MANAGE_MESSAGES)
        .addSubcommand(subcommand => {
            return subcommand
                .setName('num')
                .setDescription('刪除特定數量訊息')
                .addIntegerOption(option => {
                    return option
                        .setName('num')
                        .setDescription('刪除訊息量')
                        .setRequired(true)
                })
            })
        .addSubcommand(subcommand => {
            return subcommand
                .setName('duration')
                .setDescription('刪除特定期間後的訊息')
                .addIntegerOption(option => {
                    return option
                        .setName('day')
                        .setDescription('天')
                        .setRequired(true)
                })
                .addIntegerOption(option => {
                    return option
                        .setName('hour')
                        .setDescription('時')
                        .setRequired(false)
                })
                .addIntegerOption(option => {
                    return option
                        .setName('minute')
                        .setDescription('分')
                        .setRequired(false)
                })
                .addIntegerOption(option => {
                    return option
                        .setName('second')
                        .setDescription('秒')
                        .setRequired(false)
                })
        }),
    async execute(interaction) { 
        let embed = new MessageEmbed()
            .setColor('#ff26e2')
            .setAuthor({ name: interaction.client.user.username, iconURL: interaction.client.user.avatarURL() })
            .setDescription('事情都我在幫你做 = =')
            .setFooter({ text: interaction.user.tag, iconURL: interaction.user.avatarURL() })
            .setTimestamp();
        if (interaction.options.getSubcommand() == 'num') {
            const num = interaction.options.get('num').value;
            if (num > 100) {
                interaction.reply({content: '無法刪除超過100則訊息', ephemeral: true});
                return;
            }
            const messages = await interaction.channel.messages.fetch({limit: num});
            await interaction.channel.bulkDelete(messages)
            .then(messages => {
                embed.setDescription(`已刪除 **${messages.size}** 則訊息`);
                interaction.reply({embeds: [embed], ephemeral: true});
            });
        } else if (interaction.options.getSubcommand() == 'duration') {
            const day = interaction.options.get('day') == null ? 0 : interaction.options.get('day').value;
            const hour = interaction.options.get('hour') == null ? 0 : interaction.options.get('hour').value;
            const minute = interaction.options.get('minute') == null ? 0 : interaction.options.get('minute').value;
            const second = interaction.options.get('second') == null ? 0 : interaction.options.get('second').value;
            const duration = day * 24 * 60 * 60 * 1000 + hour * 60 * 60 * 1000 + minute * 60 * 1000 + second * 1000;
            if (duration > 14 * 24 * 60 * 60 * 1000) {
                interaction.reply({content: '無法刪除超過14天的訊息', ephemeral: true});
                return;
            }
            const date = interaction.createdAt - duration;
            const messages = await interaction.channel.messages.fetch({limit: 100})
            const filteredMessage = messages.filter(message => message.createdAt.getTime() > date);
            interaction.channel.bulkDelete(filteredMessage)
                .then(messages => {
                    embed.setDescription(`已刪除 **${messages.size}** 則訊息`);
                    interaction.reply({embeds: [embed], ephemeral: true});
                });
        }
    }
}