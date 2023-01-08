function goToRoute(element) {
  const route = element.getAttribute('data-route');
  window.location = route;
}

const button = document.getElementById('button');
button.addEventListener('click', function() {
  // code to display message goes here
    const message = document.getElementById('message');
    message.innerHTML = 'Button was clicked';

});