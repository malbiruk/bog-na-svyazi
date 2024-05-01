function animateRays(gospod) {
  // Get the position of #gospod
  var gospodRect = gospod.getBoundingClientRect();
  var gospodX = gospodRect.left + (gospodRect.width / 2);
  var gospodY = gospodRect.top + (gospodRect.height / 2);
  var nimbHeight = gospodRect.height * 64 / 294

  var gospodPaddingBottom = parseFloat(window.getComputedStyle(gospod).paddingBottom);
  if (window.matchMedia("(max-aspect-ratio: 2/3) and (orientation: portrait)").matches) {
    gospodY = gospodY - gospodPaddingBottom - nimbHeight / 2;
  } else {
    gospodY = gospodY - gospodPaddingBottom + nimbHeight / 2;
  }


  // Calculate positions for rays on both sides
  var rayLeft = document.getElementById("ray-left");
  var rayLeftRect = rayLeft.getBoundingClientRect();
  var rayRight = document.getElementById("ray-right");
  var rayRightRect = rayRight.getBoundingClientRect();

  // Calculate transformations to make rays point towards #gospod
  rayLeft.style.width = gospodRect.height - nimbHeight + "px";
  var deltaLeftY = gospodY - rayLeftRect.top;
  var deltaLeftX = gospodX - (rayLeftRect.left + rayLeftRect.right) / 2;
  rayLeft.style.height = Math.sqrt(deltaLeftX * deltaLeftX + deltaLeftY * deltaLeftY) * 1.5 + "px";
  var angleRad = Math.atan2(deltaLeftY, deltaLeftX);
  var angleLeftDeg = angleRad * (180 / Math.PI) - 90;
  rayRight.style.width = gospodRect.height - nimbHeight + "px";
  var deltaRightY = gospodY - rayRightRect.top;
  var deltaRightX = gospodX - (rayRightRect.left + rayRightRect.right) / 2;
  rayRight.style.height = Math.sqrt(deltaRightX * deltaRightX + deltaRightY * deltaRightY) * 1.5 + "px";
  var angleRad = Math.atan2(deltaRightY, deltaRightX);
  var angleRightDeg = angleRad * (180 / Math.PI) - 90;

  // Animate rays
  rayLeft.style.transition = "transform 1.3s ease-in-out, opacity 0.8s ease-in-out 1.5s";
  rayRight.style.transition = "transform 1.3s ease-in-out, opacity 0.8s ease-in-out 1.5s";

  rayLeft.style.transform = `rotate(${angleLeftDeg}deg)`;
  rayRight.style.transform = `rotate(${360+angleRightDeg}deg)`;
  rayLeft.style.opacity = 0;
  rayRight.style.opacity = 0;
}

function animateGospodThinking(gospod, gospodImg) {
  const gospodRect = gospod.getBoundingClientRect();
  const initialX = gospodRect.left;
  const initialY = gospodRect.top;
  const width = gospodRect.width;
  const height = gospodRect.height

  setTimeout(function() {
    gospod.style.position = "absolute";
    gospod.style.top = initialY + "px";
    gospod.style.left = initialX + "px";
    gospod.style.width = width + "px";
    gospod.style.height = height + "px";
  }, 500);

  const windowHeight = window.innerHeight;
  const finalY = (windowHeight - height * 5 / 4) / 2 - initialY;

  gospod.style.transition = "transform 1.5s ease-in-out 0.5s";
  gospod.style.transform = `scale(2) translateY(${finalY}px)`;
  gospodImg.style.animation = "rotate_jesus 5.5s linear 0.5s infinite";
}

function animateCiircleRays(img) {
  img.style.scale = ".01";
  const imgWidth = img.width;
  const imgHeight = img.height;
  const viewportWidth = window.innerWidth;
  const viewportHeight = window.innerHeight;
  const scaleX = viewportWidth / imgWidth;
  const scaleY = viewportHeight / imgHeight;
  const scaleFactor = Math.max(scaleX, scaleY);

  img.style.transition = "transform 1.5s ease-out";
  img.style.transform = `scale(${scaleFactor*400})`;

  setTimeout(function() {
    img.style.display = "none";
  }, 1500);
}

window.onload = function() {
  // initializing element constants
  const gospod = document.getElementById("gospod");
  const JesusPng = document.getElementById("JesusPng");
  const JesusWebp = document.getElementById("JesusWebp");
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
  const overlay = document.getElementById("overlay");
  const circleRays = document.getElementById("circle-rays");

  // INIT STATE
  quote.style.display = "none";
  container.classList.add("container-margin-top");

  // start animations
  const urlParams = new URLSearchParams(window.location.search);
  const restart = urlParams.get('restart');
  if (!restart) {
    animateRays(gospod)
    gospod.classList.add("light-anim");
    searchBox.style.animation = "fade_in 1s ease-in-out 1.3s 1 forwards";
    prompt.style.animation = "fade_in 1s ease-in-out 1.3s 1 forwards";
    neboNad.style.animation = "slide_in 2s ease-in-out 0s 1 forwards";
    neboPod.style.animation = "slide_in 1.5s ease-in-out 0s 1 forwards";
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
    // LOADING STATE
    const userInput = document.getElementById("searchInput").value;

    // change Jesus state
    JesusWebp.srcset = "/static/imgs/jesus2.webp";
    JesusPng.src = "/static/imgs/jesus2.png";

    animateGospodThinking(gospod, JesusPng)
    // reduce brightness
    overlay.style.animation = "reduce_brightness 1.7s ease-in-out 0s 1 forwards"

    // disable search
    searchInput.disabled = true;
    searchButton.disabled = true;

    // remove search
    searchBox.style.animation = "fade_out 0.5s ease-in-out 0s 1 forwards";
    prompt.style.animation = "fade_out 0.5s ease-in-out 0s 1 forwards";

    // remove clouds
    neboNad.style.bottom = "-3%";
    neboPod.style.bottom = "-3%";
    neboNad.style.animation = "slide_out 1.5s ease-in-out 0s 1 forwards";
    neboPod.style.animation = "slide_out 2s ease-in-out 0s 1 forwards";

    // receive response from backend
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/process", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function() {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 200) {
          // ANSWER STATE

          const response = JSON.parse(xhr.responseText);
          if (!window.matchMedia("(max-aspect-ratio: 2/3) and (orientation: portrait)").matches) {
            container.style.marginTop = "0%";
          } else{
            container.style.marginTop = "0%";
            container.style.maxWidth = "90%";
          }

          // restore sky brightness
          overlay.style.animation = "none";
          overlay.style.background = "(0,0,0,0)";

          // return Jesus
          JesusPng.style.animation = "none";
          gospod.classList.remove("light-anim")
          gospod.style.position = "relative";
          gospod.style.transform = "none";
          gospod.style.transition = "none";
          gospod.style.width = "auto";
          gospod.style.height = "auto";
          gospod.style.top = "auto";
          gospod.style.left = "auto";
          gospod.style.scale = "0%";
          gospod.style.opacity = "100%";
          gospod.style.MaxWidth = "auto";
          gospod.style.paddingBottom = "auto";
          gospod.classList.add("gospod-3");

          // change Jesus image
          JesusWebp.srcset = "/static/imgs/jesus3.webp";
          JesusPng.src = "/static/imgs/jesus3.png";

          // hide search box
          searchImg.style.display = "none";
          prompt.style.display = "none";

          // display quote
          quote.textContent = response.quote;
          quote.style.display = "block";
          quote.style.opacity = "0%";
          quote.style.scale = "0%";
          from.textContent = response.from;
          from.style.display = "block";
          from.style.opacity = "0%";
          from.style.scale = "0%";




          // display thumbs
          thumbs.style.display = "flex";
          thumbs.style.opacity = "0%";

          // animations
          animateCiircleRays(circleRays)
          gospod.style.animation = "scale_in 0.3s ease-out forwards";
          quote.style.animation = "scale_in 0.3s ease-out forwards, fade_in 0.3s ease-out forwards";
          from.style.animation = "scale_in 0.3s ease-out forwards, fade_in_from 0.3s ease-in-out forwards";
          thumbs.style.animation = "fade_in 0.7s ease-in-out 0.2s forwards";

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
