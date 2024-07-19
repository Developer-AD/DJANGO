// <script type="application/json" id="django-messages">
//        [{% for message in messages %}"{{ message }}"{% if not forloop.last %}, {% endif %}{% endfor %}]
// </script>

function showPromptMessage(message) {
    // alert('Prompt message Called');

  const promptMessage = document.createElement("div");
  promptMessage.classList.add("prompt-message");
  promptMessage.innerText = message;
  document.body.appendChild(promptMessage);

  // Show the prompt message
  setTimeout(() => {0
    // alert('Prompt Show Set Timout Called');

    promptMessage.classList.add("show");
}, 100);

// Hide the prompt message after 5 seconds
setTimeout(() => {
    // alert('Prompt Hide Set Timout Called');

    promptMessage.classList.remove("show");
    promptMessage.classList.add("hide");
    // Remove the element from the DOM after the transition
    promptMessage.addEventListener("transitionend", () => {
      promptMessage.remove();
    });
  }, 5000);
}

// Example usage
document.addEventListener("DOMContentLoaded", () => {
    // alert('DOM content loaded');

  const messages = JSON.parse(
    document.getElementById("django-messages").textContent
  );
  messages.forEach((message) => {
    showPromptMessage(message);
  });
});