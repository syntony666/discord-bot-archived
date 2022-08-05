const { Sequelize } = require('sequelize');

const Database = require('../db');

const databaseClient = Database.client;

module.exports =
    databaseClient.define('guilds', {
        guild_id: { type: Sequelize.STRING, primaryKey: true },
        join_channel_id: Sequelize.STRING,
        join_message: Sequelize.STRING,
        leave_channel_id: Sequelize.STRING,
        leave_message: Sequelize.STRING,
        delete_notification_channel_id: Sequelize.STRING,
    })
