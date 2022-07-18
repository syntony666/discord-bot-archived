const { SlashCommandBuilder } = require('@discordjs/builders');


module.exports = {
    data: new SlashCommandBuilder()
        .setName('say')
        .setDescription('Replies with you!')
        .addSubcommand(subcommand =>{
            return subcommand
                .setName('ping')
                .setDescription('Replies with pong!')})
        .addSubcommand(subcommand =>{
            return subcommand
                .setName('pong')
                .setDescription('Replies with ping!')}),
    async execute(interaction) {
        if (interaction.options.getSubcommand() == 'ping') {
            await interaction.reply('pong');
        }
        else {
            await interaction.reply('You said: ' + interaction.option.getContent());
        }
    },
};
