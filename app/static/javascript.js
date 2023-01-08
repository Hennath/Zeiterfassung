function goToRoute(element) {
  const route = element.getAttribute('data-route');
  window.location = route;
}

function displayMessage(message) {
  document.getElementById("message").style.display = "block";
  document.getElementById("message").innerHTML = message;
}
