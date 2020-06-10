var Discord = require('discord.io');
var logger = require('winston');
var auth = require('./auth.json');
var keyword = require('./response.json')["keyword"]
// Configure logger settings
logger.remove(logger.transports.Console);
logger.add(new logger.transports.Console, {
    colorize: true
});
logger.level = "debug";
// Initialize Discord Bot
var bot = new Discord.Client({
   token: auth.token,
   autorun: true
});
bot.on("ready", function (evt) {
    logger.info("Connected");
    logger.info("Logged in as: ");
    logger.info(bot.username + " - (" + bot.id + ")");
    console.log()
});
bot.on("message", function (user, userID, channelID, message, evt) {
    console.log('<' + channelID +'> ' + user + '(' + userID + '): ' + message)
    if (message.substring(0, 1) == '>') {
        var args = message.substring(1).split(' ');
        var cmd = args[0];
        switch(cmd) {
            case 'draw':
                if(args[1]!=undefined){
                    if(args[2]==undefined){args[2]=0;}
                    bot.sendMessage({
                        to: channelID,
                        message: '你骰到 ' + (Math.floor(Math.random() * (args[1]-args[2] + 1)) + parseInt(args[2]))
                    });
                }
                else{
                    bot.sendMessage({
                        to: channelID,
                        message: "後面要放數字我才知道阿 QQ"
                    });
                }
                break;
        }
    }
    for (let index = 0; index < keyword.length; index++) {
        if(message == keyword[index]["receive"]){
            eval('var mes='+ keyword[index]["send"])
            console.log(mes)
            bot.sendMessage({
                to: channelID,
                message: mes
            });
            break;
        }
    }
});