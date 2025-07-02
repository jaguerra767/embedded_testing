const phidget22 = require('phidget22');

async function runExample() {
	const conn = new phidget22.NetworkConnection(5661, 'localhost');
	try {
		await conn.connect();
	} catch(err) {
		console.error('Error during connect', err);
		process.exit(1);
	}

	const voltageRatioInput0 = new phidget22.VoltageRatioInput();

	voltageRatioInput0.onVoltageRatioChange = (voltageRatio) => {
		console.log('VoltageRatio: ' + voltageRatio.toString());
	};

	try {
		await voltageRatioInput0.open(5000);
	} catch(err) {
		console.error('Error during open', err);
		process.exit(1);
	}

	setTimeout(async () => {
		await voltageRatioInput0.close();
		conn.close();
		conn.delete();
	}, 5000);
}

runExample();
