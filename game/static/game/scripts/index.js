const singlePlayerBtn = document.getElementById("singlePlayerButton");
const multiplayerBtn = document.getElementById("multiplayerButton");

singlePlayerBtn.onclick = function(e) {
  console.log(e);
  window.location.href = "game/"
};
