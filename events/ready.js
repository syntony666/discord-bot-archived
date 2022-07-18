const guilds = require('../database/model/guildModel');

module.exports = {
	name: 'ready',
	once: true,
	async execute(client) {
		let guildsInDatabase = [];
		guilds.findAll({ attributes: ['guild_id'] }).then(guilds => {guildsInDatabase = guilds;});
		let guildsInDiscord = client.guilds.cache.map(guild => guild.id);
		let guildsToAdd = guildsInDatabase
			.filter(guild => !guildsInDiscord.includes(guild)).map(function(guild) {return {'guild_id': guild}});
		guilds.bulkCreate(guildsToAdd);
		console.log(`Ready! Logged in as ${client.user.tag}`);
	},
};
