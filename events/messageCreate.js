module.exports = {
	name: 'messageCreate',
	async execute(message) {
        console.log(message.content);
        if (message.content == "KSP") {
            message.channel.send("7414");
        }
	},
};
