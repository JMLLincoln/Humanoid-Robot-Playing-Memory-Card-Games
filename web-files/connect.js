openWebSocket = function() {
	socket = new WebSocket('ws://localhost:8888');
	
	socket.onopen = function() {
		document.getElementById('socket_state').innerHTML = "socket open";
	};

	socket.onmessage = function(evt) {
		parseMessage(evt.data);
		socket.send("received");
	};

	socket.onclose = function() {
		document.getElementById('socket_state').innerHTML = "socket closed";
		console.log("Attempting to open socket ...");
		setTimeout(openWebSocket, 1000);
	};
}

window.onload = function() {

	info0Label = document.getElementById('info0');
	info1Label = document.getElementById('info1');
	pscoreLabel = document.getElementById('pscore');
	bscoreLabel = document.getElementById('bscore');
	canvas = document.getElementById('canvas');
	
	openWebSocket();
}



function hide(id) {
	document.getElementById(id).style.display = "none";
}
function show(id) {
	document.getElementById(id).style.display = "inline-block";
}

function startGame(fps) {
	
	if (document.getElementById('socket_state').innerHTML == "socket open") {
		init();
		updateFunction = setInterval(update, 1000 / fps);
		hide('form');
	} else {
		info0Label.innerHTML = "Socket not open; is the server running?";
		info1Label.innerHTML = "If so, try reloading the page.";
	}
}

function stopGame() {
	
	clearInterval(updateFunction);
	
	if (pscore + bscore == totalCards) {
		if (pscore > bscore) {
			infoTextA = "All cards collected.";
			infoTextB = "You win!";
		} else if (bscore > pscore) {
			infoTextA = "All cards collected.";
			infoTextB = 	"I win!";
		} else {
			infoTextA = "All cards collected.";
			infoTextB = "It's a draw!";
		}
	} else {
		infoTextA = "Game reset.";
		infoTextB = "Play again?";
	}
	
	info0Label.innerHTML = infoTextA;
	info1Label.innerHTML = infoTextB;
	
	show("form");
}
	
function parseMessage(message) {
	
	arr = message.split('|');
	console.log(arr);
	
	card_states = JSON.parse(arr[0]);
	card_values = JSON.parse(arr[1]);
	
	turn = arr[2];
	
	pscore = arr[3];
	bscore = arr[4];
	
	running = arr[5];
}

function init() {
	
	totalCards = card_states.length;
	
	canvas.innerHTML = "";
	canvas.innerHTML += "<ul class='row'>";
	for (i = 0; i < totalCards; i++) {
		id = "'index" + i + "'";
		console.log(id);
		canvas.innerHTML += "<li id=" + id + " class='slot' onclick='clickCard(this)'><div class='card back'></div></li>";
	}
	canvas.innerHTML += "</ul>";
	
	colours = {
		1 : 'blue',
		2 : 'green',
		3 : 'red',
		4 : 'orange',
		5 : 'yellow',
		6 : 'cyan',
		7 : 'purple',
		8 : 'pink',
		9 : 'turquoise'
	};
	
	cards = [];
	for (i = 0; i < totalCards; i++) {
		x = card_values[i];
		cards.push(colours[x]);
		
		id = "index" + i;
		document.getElementById(id).innerHTML = "<div class='card back'></div>"; 
	}
	
	infoTextA = "It's " + turn + "'s turn";
	infoTextB = "";
}

function revealCard(i) {
	
	ele = document.getElementById("index" + i);
	colourClass = cards[i]
	ele.innerHTML = "<div class='card " + colourClass + "'></div>";
}

function hideCard(i) {
	
	ele = document.getElementById("index" + i);
	ele.innerHTML = "<div class='card back'></div>"; 
}

function update() {
	
	for (i = 0; i < card_states.length; i++) {
		if (card_states[i] != 0) {
			revealCard(i);
		} else {
			hideCard(i);
		}
	}
	
	info0Label.innerHTML = infoTextA;
	info1Label.innerHTML = infoTextB;
	
	pscoreLabel.innerHTML = "You have " + pscore + " cards!";
	bscoreLabel.innerHTML = "I have " + bscore + " cards!";
		
	if (running == "False") {
		stopGame();
	}
}