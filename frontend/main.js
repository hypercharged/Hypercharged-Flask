
var config = {
    apiKey: "AIzaSyC-6Pi--GB4V4RaWP_k419EsEwqssfULSc",
    authDomain: "hypercharged-website.firebaseapp.com",
    databaseURL: "https://hypercharged-website.firebaseio.com",
    projectId: "hypercharged-website",
    storageBucket: "hypercharged-website.appspot.com",
    messagingSenderId: "140399543259"
};

firebase.initializeApp(config);

// Firebase log-in widget
function configureFirebaseLoginWidget() {
  var uiConfig = {
    'signInSuccessUrl': '/',
    'signInOptions': [
      // Leave the lines as is for the providers you want to offer your users.
      firebase.auth.GoogleAuthProvider.PROVIDER_ID,
      firebase.auth.FacebookAuthProvider.PROVIDER_ID,
      //firebase.auth.TwitterAuthProvider.PROVIDER_ID,
      //firebase.auth.GithubAuthProvider.PROVIDER_ID,
      firebase.auth.EmailAuthProvider.PROVIDER_ID
    ],
    // Terms of service url
    //'tosUrl': '<your-tos-url>',
  };

  var ui = new firebaseui.auth.AuthUI(firebase.auth());
  ui.start('#firebaseui-auth-container', uiConfig);
}