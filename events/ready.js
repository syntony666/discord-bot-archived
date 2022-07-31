const guilds = require('../database/model/guildModel');

module.exports = {
	name: 'ready',
	once: true,
	async execute(client) {
		guilds.findAll({ attributes: ['guild_id'] }).then(guildsFound => {
			let guildsInDatabase = guildsFound.map(guild => guild.guild_id);
			let guildsInDiscord = client.guilds.cache.map(guild => guild.id);
			let guildsToAdd = guildsInDiscord
				.filter(guild => !guildsInDatabase.includes(guild)).map(guild => { return { guild_id: guild } });
			guilds.bulkCreate(guildsToAdd)
			console.log('Database ready!!');
			console.log(`Ready! Logged in as ${client.user.tag}`);
		});
	},
};
