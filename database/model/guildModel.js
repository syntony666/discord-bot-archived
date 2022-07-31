const { Sequelize } = require('sequelize');

const Database = require('../db');

const databaseClient = Database.client;

module.exports =
    databaseClient.define('guilds', {
        guild_id: { type: Sequelize.STRING, primaryKey: true }
    })
