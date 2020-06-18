var Discord = require('discord.io');
var logger = require('winston');
var auth = require('./auth.json');
const MongoDB = require('mongodb').MongoClient;
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
bot.on('guildMemberAdd', function (member) {
    userID = member.id; 
    console.dir("User ID: "+userID); 
    var serverID = member.guild_id;
    MongoDB.connect(auth.uri,function(err,db){
        if(err) throw err;
        db.collection('welcome').find({server : serverID}).toArray(function(err,items){
            if(err) throw err;
            if(items.length!=0){
                eval('var mes='+items[0]["message"]);
                bot.sendMessage({
                    to: items[0]["channel"], 
                    message: mes
                });
            }});
        db.close();
    });
});
bot.on("message", function (user, userID, channelID, message, evt) {
MongoDB.connect(auth.uri,function(err,db){if(err) throw err;
    var serverID = bot.channels[channelID].guild_id;
    console.log('<' + channelID +'> ' + user + '(' + userID + '): ' + message)
    if (message.substring(0, 1) == '>') {
        var args = message.substring(1).split(' ');
        var cmd = args[0];
        switch(cmd) {
            case 'help':
                bot.sendMessage({
                    to: channelID,
                    message: 'https://imgur.com/Qp5kTlp'
                });
                break;
            case 'list':
                if(err) throw err;
                db.collection('keywords').find({server : serverID}).toArray(function(err,items){if(err) throw err;
                    if(items.length!=0){
                        items.forEach(keywords => {
                            bot.sendMessage({
                                to: channelID, 
                                message: '> ' + keywords["receive"] +'\n'+ keywords["send"]
                            }); 
                        });
                    }
                    else
                    bot.sendMessage({
                        to: channelID, 
                        message: '目前沒記任何東西 >_<'
                    }); 

                });
                break;
            case 'draw':            // >draw max min
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
                        message: '後面要放數字我才知道阿 QQ'
                    });
                }
                break;
            case 'teach':
                if(args[1]!=undefined){ 
                    db.collection('keywords').remove({server: serverID, receive: args[1]})
                    let mes =''
                    for(let i=2;i < args.length; i++){
                        if(i!=2)
                            mes+=' ';
                        mes+=args[i];
                    }
                    db.collection('keywords').insert({server: serverID, user: userID, receive: args[1], send: mes})
                    bot.sendMessage({
                        to: channelID,
                        message: '<@'+userID+'> 教我聽到人家說 '+ args[1]+' 要回答 '+ mes
                    });
                }
                else{
                    bot.sendMessage({
                        to: channelID,
                        message: '所以你要教我什麼?????'
                    });
                }
                break;
            case 'delete':
                if(args[1]!=undefined){
                        db.collection('keywords').remove({server: serverID, receive: args[1]})
                        bot.sendMessage({
                            to: channelID,
                            message: '當你說'+ args[1]+'的時候 我不會理你'
                        });
                }
                else{
                    bot.sendMessage({
                        to: channelID,
                        message: '所以你要幹嘛?????'
                    });
                }
        }
    }
    if(userID !== bot.id)
        db.collection('keywords').find({server: serverID, receive: message}).toArray(function(err,items){if(err) throw err;
            if(items.length!=0)
                bot.sendMessage({
                    to: channelID,
                    message: items[0]["send"]
                });
        });  
db.close();
});
});