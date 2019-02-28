
function onSignIn(googleUser) {
  // var profile = googleUser.getBasicProfile();
  var id_token = googleUser.getAuthResponse().id_token;
  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/users/login');
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.onload = function() {
    window.location = xhr.responseText;
  };
  xhr.send('idtoken=' + id_token);
}

function signOut() {
  var auth2 = gapi.auth2.getAuthInstance();
  auth2.signOut().then(function () {
    window.location = '/users/logout';
  });
}