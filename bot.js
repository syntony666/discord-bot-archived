// var Discord = require('discord.io');
const Discord = require('discord.js');
var logger = require('winston');
var auth = require('./auth.json');
const MongoDB = require('mongodb').MongoClient;
// Configure logger settings
// logger.remove(logger.transports.Console);
// logger.add(new logger.transports.Console, {
//     colorize: true
// });
// logger.level = "debug";
// Initialize Discord Bot

const client = new Discord.Client();

client.on('ready', () => {
  console.log(`Logged in as ${client.user.tag}!`);
});

client.on('message', msg => {
    console.log(msg.content)
MongoDB.connect(auth.uri,{autoIndex: false},function(err,db){
    if(err) throw err;
    var serverID = msg.guild.id
    console.log(msg)
    db.collection('keywords').find({server: serverID, receive: msg}).toArray(function(err,items){if(err) throw err;
        if(items.length!=0)
            msg.reply(items[0]["send"]);
    });  
db.close();
});
});

client.login(auth.token);

// var bot = new Discord.Client({
//    token: auth.token,
//    autorun: true
// });
// bot.on("ready", function (evt) {
//     console.log(bot.username + " - (" + bot.id + ") logged in!!!");
//     bot.setPresence( {  game: {     name:"失落的龍絆"}} );
//     bot.editNickname( { serverID:   '438997365194489856',
//                         userID:     bot.id,
//                         nick:       "我是樂高 踩我會痛痛 >..<"});
// });
// bot.on('guildMemberAdd', function (member) {
//     userID = member.id; 
//     console.dir("User ID: "+userID); 
//     var serverID = member.guild_id;
//     MongoDB.connect(auth.uri,function(err,db){
//         if(err) throw err;
//         db.collection('welcome').find({server : serverID}).toArray(function(err,items){
//             if(err) throw err;
//             if(items.length!=0){
//                 eval('var mes='+items[0]["message"]);
//                 bot.sendMessage({
//                     to: items[0]["channel"], 
//                     message: mes
//                 });
//             }});
//         db.close();
//     });
// });
// bot.on("message", function (user, userID, channelID, message, evt) {
// console.log(user +'(' +'#' + bot.channels[channelID].name+ ', ' + bot.servers[bot.channels[channelID].guild_id].name+'): ' + message)
// MongoDB.connect(auth.uri,function(err,db){if(err) throw err;
//     var serverID = bot.channels[channelID].guild_id;
//     if (message.substring(0, 1) == '>') {
//         var args = message.substring(1).split(' ');
//         var cmd = args[0];
//         switch(cmd) {
//             case 'help':
//                 bot.sendMessage({
//                     to: channelID,
//                     message: 'https://imgur.com/Qp5kTlp'
//                 });
//                 break;
//             case 'list':
//                 if(err) throw err;
//                 db.collection('keywords').find({server : serverID}).toArray(function(err,items){if(err) throw err;
//                     if(items.length!=0){
//                         let mes = ''
//                         items.forEach(keywords => {
//                             mes += '> ' + keywords["receive"] +'\n'+ keywords["send"] +'\n'
//                         });
//                         bot.sendMessage({
//                             to: channelID, 
//                             message: mes
//                         });
//                     }
//                     else
//                     bot.sendMessage({
//                         to: channelID, 
//                         message: '目前沒記任何東西 >_<'
//                     }); 

//                 });
//                 break;
//             case 'draw':            // >draw max min
//                 if(args[1]!=undefined){
//                     if(args[2]==undefined){args[2]=0;}
//                     bot.sendMessage({
//                         to: channelID,
//                         message: '你骰到 ' + (Math.floor(Math.random() * (args[1]-args[2] + 1)) + parseInt(args[2]))
//                     });
//                 }
//                 else{
//                     bot.sendMessage({
//                         to: channelID,
//                         message: '後面要放數字我才知道阿 QQ'
//                     });
//                 }
//                 break;
//             case 'teach':
//                 if(args[1]!=undefined){ 
//                     db.collection('keywords').remove({server: serverID, receive: args[1]})
//                     let mes =''
//                     for(let i=2;i < args.length; i++){
//                         if(i!=2)
//                             mes+=' ';
//                         mes+=args[i];
//                     }
//                     db.collection('keywords').insert({server: serverID, user: userID, receive: args[1], send: mes})
//                     bot.sendMessage({
//                         to: channelID,
//                         message: '<@'+userID+'> 教我聽到人家說 '+ args[1]+' 要回答 '+ mes
//                     });
//                 }
//                 else{
//                     bot.sendMessage({
//                         to: channelID,
//                         message: '所以你要教我什麼?????'
//                     });
//                 }
//                 break;
//             case 'delete':
//                 if(args[1]!=undefined){
//                         db.collection('keywords').remove({server: serverID, receive: args[1]})
//                         bot.sendMessage({
//                             to: channelID,
//                             message: '當你說'+ args[1]+'的時候 我不會理你'
//                         });
//                 }
//                 else{
//                     bot.sendMessage({
//                         to: channelID,
//                         message: '所以你要幹嘛?????'
//                     });
//                 }
//         }
//     }
//     if(userID !== bot.id)
//         db.collection('keywords').find({server: serverID, receive: message}).toArray(function(err,items){if(err) throw err;
//             if(items.length!=0)
//                 bot.sendMessage({
//                     to: channelID,
//                     message: items[0]["send"]
//                 });
//         });  
// db.close();
// });
// });