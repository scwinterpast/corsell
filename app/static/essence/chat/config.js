// Define app configuration in a single location, but pull in values from
// system environment variables (so we don't check them in to source control!)
module.exports = {
    //flag to get Twilio Account Setting from this file or from environment
    // If set to 'Y' , the values are read from config.js and not from environment
    getTwiliAccountSettingsfromFile: 'Y',


    // Your primary Twilio Account SID
    accountSid: 'ACb1d05881534e908045704e82ccd9d068',

    // API Key/Secret Pair - generate a pair in the console
    apiKey: 'SK562a13905b9663e4fad731620854762f',
    apiSecret: 'hRMKDmXnVLVtCLEY7tAnfYMgJPD0a3UC',

    // Your Chat service instance SID
    serviceSid: 'IS74325d311623459e9e6dee02174cdf5e',

    // Defines whether or not this application is deployed in a production
    // environment
    nodeEnv: process.env.NODE_ENV || 'development',

    // In production, this is the base host name for web app on the public
    // internet, like "jimmysbbq.herokuapp.com".  This should be the same host
    // you use in your Twilio Number config for voice or messaging URLs
    host: process.env.HOST || 'localhost',

    // The port your web application will run on
    port: process.env.PORT || 7000

};
