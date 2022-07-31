const { Sequelize } = require('sequelize');

const Database = require('../database/db');

const databaseClient = Database.client;

const reply = databaseClient.define('reply_message', {
    response: Sequelize.STRING,
})

module.exports = {
    name: 'messageCreate',
    async execute(message) {
        reply.findOne({
            where: {
                guild_id: message.guild.id,
                request: message.content
            }
        }).then(msg => {
            if (msg.response !== null) {
                message.reply(msg.response);
                console.log(`${message.content} ===> ${msg.response}`);
            }
        }).catch(err => { });
    },
};
