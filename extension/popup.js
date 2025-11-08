const API_URL = "http://127.0.0.1:8010/predict";

async function getActiveTabUrl() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  return tab?.url || "";
}

function setBadge(label) {
  // Color by label
  const color = label === "SAFE" ? [0, 150, 0, 255] :
                label === "PHISHING" ? [255, 165, 0, 255] :
                label === "DEFACEMENT" ? [255, 140, 0, 255] :
                [200, 0, 0, 255]; // MALWARE / default red
  chrome.action.setBadgeText({ text: label[0] }); // S / P / D / M
  chrome.action.setBadgeBackgroundColor({ color });
}

async function checkUrl(url) {
  const res = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url })
  });
  if (!res.ok) throw new Error(`API ${res.status}`);
  return res.json();
}

(async () => {
  const tabUrl = await getActiveTabUrl();
  document.getElementById("tabUrl").textContent = tabUrl || "(no URL)";
  const btn = document.getElementById("checkBtn");
  const out = document.getElementById("result");

  btn.addEventListener("click", async () => {
    if (!tabUrl) { out.textContent = "No active tab URL."; return; }
    out.textContent = "Checking…";
    try {
      const data = await checkUrl(tabUrl);
      out.textContent = `Result: ${data.prediction}`;
      setBadge(data.prediction);
    } catch (e) {
      out.textContent = `Error: ${e.message}`;
      chrome.action.setBadgeText({ text: "!" });
      chrome.action.setBadgeBackgroundColor({ color: [128, 128, 128, 255] });
    }
  });
})();
