const { Sequelize } = require('sequelize');
const Database = require('../db');

const databaseClient = Database.client;

module.exports = 
databaseClient.define('reply_message', {
    guild_id: Sequelize.STRING,
    request: Sequelize.STRING,
    response: Sequelize.STRING
})