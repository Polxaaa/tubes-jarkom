//const g = document.getElementById('search-bar');
//const h = document.getElementById('txtsearch');

document.getElementById('form').onsubmit = function() {
  window.location = 'http://192.168.56.1:8080/' + document.getElementById('txtsearch').value;
  return false;
}
