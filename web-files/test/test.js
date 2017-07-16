openWebSocket = function() {
	socket = new WebSocket('ws://localhost:8888');
}

socket.onopen = function() {
	document.getElementById('socket_state').innerHTML = "| socket open";
};

socket.onmessage = function(evt) {
	document.getElementById('test_result').innerHTML = "| " + evt.data;
};

socket.onclose = function() {
	document.getElementById('socket_state').innerHTML = "| socket closed";
	setTimeout(openWebSocket, 1000);
};

window.onload = function() {
	
	openWebSocket();	
};


	
function test_button() {
	str = document.getElementById('input_text').value;
	console.log(str);
	socket.send(str);
};