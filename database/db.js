const Sequelize = require('sequelize');
const { database } = require('../config.json');

module.exports = {
    client: new Sequelize(database.database, database.username, database.password, {
        host: database.host,
        dialect: 'mariadb',
        logging: false,
    })
}
