const { Sequelize } = require('sequelize');
const Database = require('../db');

const databaseClient = Database.client;

module.exports = 
databaseClient.define('guilds', {
    role_id: {type: Sequelize.STRING, primaryKey: true},
    reaction: DataTypes.STRING,
    guild_id: DataTypes.STRING,
    message_id: DataTypes.STRING
})