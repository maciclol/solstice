// Upvote and downvote functionality
function upvote(e) {
	if (e.target.classList.contains("vote")) {
		e.target.classList.remove("vote");
		document.getElementById("d-" + e.target.id.substring(2)).classList.add("vote");
		document.getElementById("s-" + e.target.id.substring(2)).innerHTML = parseInt(document.getElementById("v-" + e.target.id.substring(2)).innerHTML) + 1;
	}
	else {
		e.target.classList.add("vote");
		document.getElementById("s-" + e.target.id.substring(2)).innerHTML = parseInt(document.getElementById("v-" + e.target.id.substring(2)).innerHTML);

	}
}

function downvote(e) {
	if (e.target.classList.contains("vote")) {
		e.target.classList.remove("vote");
		document.getElementById("u-" + e.target.id.substring(2)).classList.add("vote");
		document.getElementById("s-" + e.target.id.substring(2)).innerHTML = parseInt(document.getElementById("v-" + e.target.id.substring(2)).innerHTML) - 1;
	}
	else {
		e.target.classList.add("vote");
		document.getElementById("s-" + e.target.id.substring(2)).innerHTML = parseInt(document.getElementById("v-" + e.target.id.substring(2)).innerHTML);
	}
}