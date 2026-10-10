const $ = (id) => document.getElementById(id);

const form = $("url-form");
const input = $("url-input");
const button = $("submit-btn");
const errorBox = $("form-error");
const result = $("result");

const SCHEME = /^[a-z][a-z0-9+.\-]*:\/\//i;

// Light mirror of backend/url_cleaning.py so the user sees the same input the
// model will get. The server cleans and validates again: it is the source of truth.
const cleanUrl = (raw) => raw.trim().replace(/^["'<]+|["'>]+$/g, "").replace(SCHEME, "");

function showError(message) {
  errorBox.textContent = message;
  errorBox.hidden = !message;
}

function setLoading(isLoading) {
  button.disabled = isLoading;
  button.textContent = isLoading ? "Analysing…" : "Detect phishing";
}

function renderResult(data) {
  const phishing = data.is_phishing;

  document.body.dataset.state = phishing ? "danger" : "safe";
  result.dataset.verdict = phishing ? "phishing" : "legitimate";

  $("verdict").textContent = phishing ? "Likely phishing" : "Looks legitimate";
  $("verdict-note").textContent = data.borderline
    ? "The model is unsure. Verify this link manually."
    : phishing
      ? "Don't enter passwords or personal details on this site."
      : "No phishing patterns found. Stay careful with unknown links.";

  $("meter-fill").style.width = `${Math.round(data.risk * 100)}%`;
  $("score").textContent = `${Math.round(data.risk * 100)}%`;
  $("cleaned").textContent = data.cleaned_url;
  $("address").textContent = data.cleaned_url;

  // textContent only: the URL is user input and must never be injected as HTML.
  $("tokens").replaceChildren(...data.tokens.map((token) => {
    const chip = document.createElement("span");
    chip.textContent = token;
    return chip;
  }));

  result.hidden = false;
}

async function detect(rawUrl) {
  const url = cleanUrl(rawUrl);
  if (!url) return showError("Enter a URL to check.");

  showError("");
  setLoading(true);
  try {
    const response = await fetch("/api/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Something went wrong. Try again.");
    renderResult(data);
  } catch (error) {
    showError(error.message);
  } finally {
    setLoading(false);
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  detect(input.value);
});

document.querySelectorAll(".chip").forEach((chip) => {
  chip.addEventListener("click", () => {
    input.value = chip.dataset.url;
    detect(input.value);
  });
});
