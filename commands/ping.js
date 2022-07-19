const { SlashCommandBuilder } = require('@discordjs/builders');
const pageService = require('../service/pageService');
const { MessageEmbed } = require('discord.js');


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
            var embed = []
            for (let i = 0; i < 10; i++) {
                embed.push(new MessageEmbed()
                    .setColor('#f0b01d')
                    .setTitle(i.toString())
                    .setDescription('pong')
                )
            }
            // await interaction.reply({ embeds: embed });
            await pageService(interaction, embed);
        }
        else {
            await interaction.reply('You said: ' + interaction.option.getContent());
        }
    },
};
