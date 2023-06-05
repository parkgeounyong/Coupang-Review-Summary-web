function sendURL(url) {
  var output = document.getElementById('output');
  output.innerHTML = '<p>Please wait...</p>'; // Display "Please wait"

  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/process_url'); // Flask 앱에서 설정한 경로
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.onload = function() {
    if (xhr.status === 200) {
      var response = JSON.parse(xhr.responseText);
      output.innerHTML = ''; // Remove "Please wait"

      var p = document.createElement('p');
      var text = document.createTextNode(response.result);
      p.appendChild(text);
      output.appendChild(p);
    }
  };
  xhr.send(JSON.stringify({url: url}));
}

var form = document.querySelector('form');
form.addEventListener('submit', function(event) {
  event.preventDefault();
  var url = document.getElementById('URL').value;
  sendURL(url);
});
