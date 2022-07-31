const { Sequelize } = require('sequelize');

const Database = require('../db');

const databaseClient = Database.client;

module.exports =
    databaseClient.define('reaction_roles', {
        role_id: { type: Sequelize.STRING, primaryKey: true },
        reaction: Sequelize.STRING,
        guild_id: Sequelize.STRING,
        message_url: {
            type: Sequelize.STRING,
        }
    })