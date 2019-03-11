'use strict'


var te_client = require('./te_client'),
	Client = new te_client({
		url: 'ws://stream.tradingeconomics.com/',
		key: '59227A99EC24455', //API_CLIENT_KEY
		secret: '98A5977ABBE149C' //API_CLIENT_SECRET
		//reconnect: true
	});


Client.subscribe('EURUSD:CUR');

Client.subscribe('EURGBP:CUR');


//Client.subscribe('CL1');




Client.on('message', function(msg){
	console.log('\n Data from TradingEconomics stream: ', msg.topic);
	console.log(msg);

	//parse/save msg to DB
});

//...


