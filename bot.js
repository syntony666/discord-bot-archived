const Discord = require('discord.js');
var auth = require('./auth.json');
const MongoDB = require('mongodb').MongoClient;

const client = new Discord.Client();

client.login(auth.token);

client.on('ready', () => {
  console.log(`Logged in as ${client.user.tag}!`);
  client.user.setUsername("我是樂高 踩我會痛痛 >..<")
  client.user.setPresence({activity:{name:"Dragalia Lost 失落的龍絆",type:"PLAYING"},status:"online"})
});

client.on("guildMemberAdd", member=>{
    MongoDB.connect(auth.uri,(err,db)=>{    if(err) throw err;
        db.collection('welcome').find({server : member.guild.id}).toArray(function(err,items){ if(err) throw err;
            if(items.length!=0){
                member.guild.channels.cache
                .find(channel=> channel.id ===items[0]["channel"])
                .send(`${member} ${items[0]["message"]}`)
            }});
        db.close();
    });
})

client.on('message', msg => {
console.log(`${msg.author.username}(${msg.guild.name},${msg.channel.name}): `)
console.log(msg.content)
MongoDB.connect(auth.uri,function(err,db){
    if (msg.author.bot) {db.close(); return};

    db.collection('silence').find({server: msg.guild.id, channel: msg.channel.id})
    .toArray((err , items)=>{if(items.length!=0){db.close(); return}

    var serverID = msg.guild.id
    var message = msg.content
    var userID = msg.author.id
    if(message.substring(0, 1) == '>'){
        var args = message.substring(1).split(' ')
        var cmd = args[0].toLowerCase()
        if(cmd == 'help'){
            msg.channel.send('https://gist.github.com/syntony666/d92b170619adfe63857fd8ef3b4c88e3')
        }
        else if(cmd == 'list'){
            db.collection('keywords').find({server : serverID})
            .toArray(function(err,items){if(err) throw err;
                let mes =''
                if(items.length!=0){
                    items.forEach(keywords => {
                        mes += '> ' + keywords["receive"] +'\n'+ keywords["send"] +'\n'
                    });
                    msg.channel.send(mes)
                }
                else
                    msg.channel.send('目前沒記任何東西 >_<')
            });
        }
        else if(cmd == 'silence'){
            if(msg.member.hasPermission(['ADMINISTRATOR'])){
                if(args[1] == 'a' && args.length==3){
                    db.collection('silence').remove({server: serverID, channel: args[2]})
                    db.collection('silence').insert({server: serverID, channel: args[2]})
                    msg.channel.send(`我不會在 <#${args[2]}> 裡說話`)
                }
                if(args[1] == 'd' && args.length==3){
                    db.collection('silence').remove({server: serverID, channel: args[2]})
                    msg.channel.send(`我會在 <#${args[2]}> 裡說話`)
                }
                if(args[1] == 'l' && args.length==2){
                    db.collection('silence').find({server : serverID})
                    .toArray(function(err,items){if(err) throw err;
                        let mes ='我在 '
                        if(items.length!=0){
                            items.forEach(keywords => {
                                mes += '<#' + keywords["channel"] +'> '
                            });
                            msg.channel.send(mes+'裡不能說話')
                        }
                        else
                            msg.channel.send('我在每個頻道都能說話')
                    });
                }
            }
            else
                msg.channel.send('你沒權限給我下去!!!!!')
        }
        else if(cmd == 'teach'){
            if(args.length>=3){ 
                db.collection('keywords').remove({server: serverID, receive: args[1]})
                let mes = ''
                for(let i=2;i < args.length; i++)
                    mes+=args[i]+' ';
                db.collection('keywords').insert({server: serverID, user: userID, receive: args[1], send: mes})
                    msg.channel.send(`<@${msg.author.id}> 教我聽到人家說 ${args[1]} 要回答 ${mes}`)
            }
            else
                msg.channel.send('所以你要教我什麼?????')
        }
        else if(cmd == 'delete'){
            if(args.length>=2){ 
                db.collection('keywords').remove({server: serverID, receive: args[1]})
                msg.channel.send('當你說'+ args[1]+'的時候 我不會理你')
            }
            else
                msg.channel.send('所以你要幹嘛?????')
        }
    }
    else
        db.collection('keywords').find({server: serverID, receive: message})
        .toArray(function(err,items){if(err) throw err;
            if(items.length!=0)     
            msg.channel.send(items[0]["send"])}); 
    db.close();
})});
});