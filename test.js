var fs = require('fs')
var obj = JSON.parse(fs.readFileSync('./response.json','utf8'))
obj["keyword"].push({"receive":"hohoho","send":"'hahaha'"});
fs.writeFile('response.json',JSON.stringify(obj))
console.log(obj)