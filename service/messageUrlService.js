let MessageUrlService = class {
    constructor(msgUrl) {
        this.messageUrl = msgUrl;
    }
    getGuildId() {
        return this.messageUrl.split('/')[4];
    }
    getChannelId() {
        return this.messageUrl.split('/')[5];
    }
    getMessageId() {
        return this.messageUrl.split('/')[6];
    }
    isVaild() {
        var reForUrl = new RegExp('(https?:\/\/)?(discord\.com\/channels)[\/][0-9]+[\/][0-9]+[\/][0-9]+');
        return reForUrl.test(this.messageUrl);
    }
}

module.exports = MessageUrlService;
