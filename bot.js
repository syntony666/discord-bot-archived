var Discord = require('discord.io');
var logger = require('winston');
var auth = require('./auth.json');
var fs = require('fs')
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
    var welcome = JSON.parse(fs.readFileSync('./response.json','utf8'))["welcome"]
    for (let index = 0; index < welcome.length; index++) {
        if(serverID == welcome[index]["server"]){
            eval('var mes='+welcome[index]["message"]);
            bot.sendMessage({
                to: welcome[index]["channel"], 
                message: mes
            }); 
        }
    }
});
bot.on("message", function (user, userID, channelID, message, evt) {
    var serverID = bot.channels[channelID].guild_id;
    console.log('<' + channelID +'> ' + user + '(' + userID + '): ' + message)
    if (message.substring(0, 1) == '>') {
        var args = message.substring(1).split(' ');
        var cmd = args[0];
        switch(cmd) {
            case 'help':
                bot.sendMessage({
                    to: channelID,
                    message: 'https://imgur.com/0VC5Lmu.jpg'
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
            case 'list':
                var keyword = JSON.parse(fs.readFileSync('./response.json','utf8'))["keyword"]
                for (let index = 0; index < keyword.length; index++) {
                    if(serverID == keyword[index]["server"]){
                        bot.sendMessage({
                            to: channelID,
                            message: '> ' + keyword[index]["receive"] +'\n'+ keyword[index]["send"]
                        });
                    }
                }
                break;
            case 'teach':
                if(args[1]!=undefined){
                    fs.readFile('./response.json', 'utf8', 
                        function readFileCallback(err, data){
                            if (err){
                                console.log(err);
                            } 
                            else {
                                obj = JSON.parse(data);
                                for (let index = 0; index < keyword.length; index++) {
                                    if(args[1] == obj["keyword"][index]["receive"])
                                        delete obj["keyword"][index]
                                }
                                mes = ''
                                for(let i=2;i < args.length; i++){
                                    if(i!=2)
                                        mes+=' ';
                                    mes+=args[i];
                                }
                                obj["keyword"].push({server: serverID, user: userID, receive: args[1], send: mes}); //add some data
                                obj["keyword"] = obj["keyword"].filter(function(x) { return x !== null }); 
                                json = JSON.stringify(obj, null, '\t'); //convert it back to json
                                fs.writeFile('./response.json', json, 'utf8',function(err){}); // write it back 
                                bot.sendMessage({
                                    to: channelID,
                                    message: '<@'+userID+'> 教我聽到人家說 '+ args[1]+' 要回答 '+ mes
                                });
                            }
                        }
                    );
                }
                else{
                    bot.sendMessage({
                        to: channelID,
                        message: '所以你要教我什麼?????'
                    });
                }
                break;
        }
    }
    var keyword = JSON.parse(fs.readFileSync('./response.json','utf8'))["keyword"]
    for (let index = 0; index < keyword.length; index++) {
        if(message == keyword[index]["receive"] && serverID == keyword[index]["server"]){
            bot.sendMessage({
                to: channelID,
                message: keyword[index]["send"]
            });
            break;
        }
    }
});