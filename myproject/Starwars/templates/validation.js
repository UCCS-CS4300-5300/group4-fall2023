

document.getElementById("myform").addEventListener("submit", function(event)
{
		
	
	const username = document.getElementById("username").value
	const password = document.getElementById("password").value
	const validate = document.getElementById("validate")
	// const form = document.getElementById("myform")

	if (username === "admin" && password === "admin") {
			//window.location.href = "selection.html"
		window.location.href = "selection.html"
	}
	else if (username === "user" && password === "user") {
		window.location.href = "selection.html"
	}
	else if (username === "user2" && password === "user2") {
		window.location.href = "selection.html"
	}
	else {
			
		validate.innerHTML = "invalid credentials"

	}
});





	
	





