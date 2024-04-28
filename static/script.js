document.addEventListener("DOMContentLoaded", function() {
  // initializing element constants
  const gospod = document.getElementById("gospod");
  const searchButton = document.getElementById("searchButton");
  const searchDisabler = document.getElementById("searchDisabler");
  const searchInput = document.getElementById("searchInput");
  const searchImg = document.getElementById("searchImg");
  const quote = document.getElementById("quote");
  const from = document.getElementById("from");
  const prompt = document.getElementById("prompt");

  // handle search
  searchButton.addEventListener("click", function() {
    // Function to process search
    processSearch();
  });

  // Add event listener for Enter key press on search input
  searchInput.addEventListener("keyup", function(event) {
    if (event.keyCode === 13) {
      // Enter key is pressed, trigger search button click
      searchButton.click();
    }
  });

  // Function to process search
  function processSearch() {
    const userInput = document.getElementById("searchInput").value;

    // change Jesus state
    document.getElementById("JesusWebp").srcset = "/static/imgs/jesus2.webp";
    document.getElementById("JesusPng").src = "/static/imgs/jesus2.png";

    // disable search
    searchDisabler.style.display = "inline";
    searchInput.disabled = true;
    searchButton.disabled = true;

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
        } else {
          console.error("Error:", xhr.status);
        }
      }
    };
    // send user query to backend
    xhr.send(JSON.stringify({
      query: userInput
    }));
  }
});
