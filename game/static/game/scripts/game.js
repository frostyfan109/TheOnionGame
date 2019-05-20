function requestArticles(count,callback) {
  let xhr = new XMLHttpRequest();
  xhr.responseType = "json";
  xhr.open('GET','/getRandomArticles?count='+count);
  xhr.onload = function() {
    let articles = xhr.response;
    console.log("Fetched "+articles.length+" articles");
    callback(articles);
  }
  xhr.send(null);
}

function requestArticlesCallback(articles) {
  requestingArticles = false;
  hideLoadingContainer();
  articles.forEach(article => questionQueue.push(article));
  if (currentArticle === null) setCurrentArticle(questionQueue.shift());
};

function startNextQuestion() {
  if (questionQueue.length !== 0) {
    setCurrentArticle(questionQueue.shift());
    if (questionQueue.length < ARTICLE_TARGET_MIN) {
      if (!requestingArticles) {
        requestingArticles = true;
        console.log("Requesting additional articles");
        requestArticles(ARTICLE_TARGET_MAX - ARTICLE_TARGET_MIN, requestArticlesCallback);
      }

    }
  }
  else {
    console.log("Loading new articles currently (out of questions");
    showLoadingContainer();
    if (!requestingArticles) {
      console.log("Loading new articles");
      requestingArticles = true;
      currentArticle = null;
      requestArticles(ARTICLE_TARGET_MAX,requestArticlesCallback);
    }
  }
}

function setCurrentArticle(article) {
  if (currentArticle === null) {
    questionText.innerText = article.title;
    currentArticle = article;
  }
}

function answerQuestion(answer) {
  if (currentArticle !== null) {
    let correct = answer === currentArticle.real;
    if (correct) {
      streakText.innerText = ++streak;
      streakContainer.classList.add('correctAnimationIn');
      function ev() {
        currentArticle = null;
        startNextQuestion();
        streakContainer.classList.remove('correctAnimationIn');
        streakContainer.removeEventListener("animationend",ev);
        streakContainer.classList.add('correctAnimationOut');
        function ev2() {
          streakContainer.removeEventListener("animationend",ev2);
          streakContainer.classList.remove("correctAnimationOut");
        }
        streakContainer.addEventListener("animationend",ev2);
      }
      streakContainer.addEventListener("animationend",ev);
    }
    else {
      endGame();
    }
  }
}

function endGame() {
  gameOverContainer.style.display = "flex";
  gameOverText.innerHTML = `
    Oh no! You lost...
    <span style="display:block;text-align:center;">Streak: ${streak}</span>
  `
  gameOverContainer.classList.add('fadeIn');
  streakText.innerText = streak = 0;
}

function showLoadingContainer() {
  loadingText.innerText = "Loading";
  clearInterval(loading.interval);
  loading.interval = setInterval(function() {
    loadingText.innerText += '.';
    if (loadingText.innerText.slice(-3) === "...") {
      loadingText.innerText = "Loading";
    }
  },750);
  loading.style.display = "flex";
}

function hideLoadingContainer() {
  clearInterval(loading.interval);
  loading.interval = null;
  loading.style.display = "none";
}

const ARTICLE_TARGET_MAX = 5;
const ARTICLE_TARGET_MIN = 2;
const questionText = document.getElementById('questionText');
const trueButton = document.getElementById('realButton');
const fakeButton = document.getElementById('fakeButton');
const loading = document.getElementById('loading');
const loadingText = document.getElementById('loadingText');
const streakContainer = document.getElementById('streakContainer');
const streakText = document.getElementById('streakText');
const gameOverContainer = document.getElementById('gameOverContainer');
const gameOverText = document.getElementById('gameOverText');
const playAgainBanner = document.getElementById('playAgainBanner');


playAgainBanner.onclick = function(e) {
  currentArticle = null;
  gameOverContainer.style.display = "none";
  gameOverContainer.classList.remove('fadeIn');
  console.log("Restarting game");
  startNextQuestion();
}
trueButton.onclick = function(e) {
  answerQuestion(true);
}
fakeButton.onclick = function(e) {
  answerQuestion(false);
}

let streak = 0;
let requestingArticles = false;
let questionQueue = [];
let currentArticle = null;

showLoadingContainer();
setTimeout(startNextQuestion,500); //artificial load time
