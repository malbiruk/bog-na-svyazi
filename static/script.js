function animateRays(gospod) {
  // Get the position of #gospod
  var gospodRect = gospod.getBoundingClientRect();
  var gospodX = gospodRect.left + (gospodRect.width / 2);
  var gospodY = gospodRect.top + (gospodRect.height / 2);

  // Calculate positions for rays on both sides
  var rayLeft = document.getElementById("ray-left");
  var rayLeftRect = rayLeft.getBoundingClientRect();
  var rayRight = document.getElementById("ray-right");
  var rayRightRect = rayRight.getBoundingClientRect();

  // Calculate transformations to make rays point towards #gospod
  rayLeft.style.width = gospodRect.height + "px";
  var deltaLeftY = gospodY - rayLeftRect.top;
  var deltaLeftX = gospodX - (rayLeftRect.left + rayLeftRect.right) / 2;
  rayLeft.style.width = gospodRect.height + "px";
  rayLeft.style.height = Math.sqrt(deltaLeftX * deltaLeftX + deltaLeftY * deltaLeftY) * 1.5 + "px";
  var angleRad = Math.atan2(deltaLeftY, deltaLeftX);
  var angleLeftDeg = angleRad * (180 / Math.PI) - 90;
  rayRight.style.width = gospodRect.height + "px";
  var deltaRightY = gospodY - rayRightRect.top;
  var deltaRightX = gospodX - (rayRightRect.left + rayRightRect.right) / 2;
  rayRight.style.width = gospodRect.height + "px";
  rayRight.style.height = Math.sqrt(deltaRightX * deltaRightX + deltaRightY * deltaRightY) * 1.5 + "px";
  var angleRad = Math.atan2(deltaRightY, deltaRightX);
  var angleRightDeg = angleRad * (180 / Math.PI) - 90;

  // Aniamte rays 
  rayLeft.style.transition = "transform 1s ease-in-out, opacity 0.8s ease-in-out 1.5s";
  rayRight.style.transition = "transform 1s ease-in-out, opacity 0.8s ease-in-out 1.5s";

  rayLeft.style.transform = `rotate(${angleLeftDeg}deg)`;
  rayRight.style.transform = `rotate(${360+angleRightDeg}deg)`;
  rayLeft.style.opacity = 0;
  rayRight.style.opacity = 0;
}

window.onload = function() {
  // initializing element constants
  const gospod = document.getElementById("gospod");
  const searchButton = document.getElementById("searchButton");
  const searchDisabler = document.getElementById("searchDisabler");
  const searchBox = document.getElementById("searchBox");
  const searchInput = document.getElementById("searchInput");
  const searchImg = document.getElementById("searchImg");
  const quote = document.getElementById("quote");
  const from = document.getElementById("from");
  const prompt = document.getElementById("prompt");
  const neboNad = document.getElementById("neboNad");
  const neboPod = document.getElementById("neboPod");
  const thumbs = document.getElementById("thumbs");
  const thumbsUp = document.getElementById("thumbsUp");
  const thumbsDown = document.getElementById("thumbsDown");
  const container = document.getElementById("container");
  const answerText = document.getElementById("answerText");

  quote.style.display = "none";
  container.style.marginTop = "-12%";

  // start animations
  const urlParams = new URLSearchParams(window.location.search);
  const restart = urlParams.get('restart');
  if (!restart) {
    animateRays(gospod)
    gospod.classList.add("light-anim");
    searchBox.classList.add("search-fade-in");
    prompt.classList.add("search-fade-in");
    neboNad.classList.add("nebo2-slide-in");
    neboPod.classList.add("nebo1-slide-in");
  } else {
    gospod.style.opacity = "100%";
    searchBox.style.opacity = "100%";
    prompt.style.opacity = "100%";
    neboNad.style.bottom = "-3%";
    neboPod.style.bottom = "-3%";
  }

  // trigger search
  searchButton.addEventListener("click", function() {
    processSearch();
  });
  searchInput.addEventListener("keyup", function(event) {
    if (event.keyCode === 13) {
      searchButton.click();
    }
  });

  function processSearch() {
    const userInput = document.getElementById("searchInput").value;

    // change Jesus state
    document.getElementById("JesusWebp").srcset = "/static/imgs/jesus2.webp";
    document.getElementById("JesusPng").src = "/static/imgs/jesus2.png";

    // disable search
    searchDisabler.style.display = "inline";
    searchInput.disabled = true;
    searchButton.disabled = true;

    // remove clouds
    neboNad.style.display = "none";
    neboPod.style.display = "none";

    // receive response from backend
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/process", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function() {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 200) {
          const response = JSON.parse(xhr.responseText);
          // change Jesus state
          document.getElementById("JesusWebp").srcset = "/static/imgs/jesus3.webp";
          document.getElementById("JesusPng").src = "/static/imgs/jesus3.png";
          gospod.style.maxWidth = "35%";
          gospod.style.paddingBottom = "0%";

          // hide search box
          searchImg.style.display = "none";
          prompt.style.display = "none";

          // display quote
          quote.textContent = response.quote;
          from.textContent = response.from;
          quote.style.display = "block";
          from.style.display = "block";

          // display thumbs
          container.style.marginTop = "0%";
          thumbs.style.display = "flex";

          // record feedback
          thumbsUp.addEventListener("click", function(event) {
            event.preventDefault();
            recordFeedback("good");
          });
          thumbsDown.addEventListener("click", function(event) {
            event.preventDefault();
            recordFeedback("bad");
          });

          // click outside thumbs moves to support page
          document.body.addEventListener("click", function(event) {
            if (!thumbs.contains(event.target) && !answerText.contains(event.target)) {
              window.location.href = "/support";
            }
          });

          // change cursor to pointer when hovering
          document.body.addEventListener("mouseover", function(event) {
            if (!thumbs.contains(event.target) && !answerText.contains(event.target)) {
              document.body.style.cursor = "pointer";
            }
          });
          document.body.addEventListener("mouseout", function(event) {
            document.body.style.cursor = "auto";
          });

        } else {
          window.location.href = "/error";
          console.error("Error:", xhr.status);
        }
      }
    };
    // send user query to backend
    xhr.send(JSON.stringify({
      query: userInput
    }));
  }

  function recordFeedback(feedback) {
    const userInput = document.getElementById("searchInput").value;
    const quoteText = quote.textContent;

    window.location.href = "/support";

    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/record-feedback", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({
      query: userInput,
      quote: quoteText,
      feedback: feedback
    }));
  }
};
