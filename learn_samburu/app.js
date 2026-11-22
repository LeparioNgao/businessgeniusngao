const entryForm = document.getElementById("entryForm");
const entryIdInput = document.getElementById("entryId");
const phraseInput = document.getElementById("phrase");
const meaningInput = document.getElementById("meaning");
const pronunciationInput = document.getElementById("pronunciation");
const contextInput = document.getElementById("context");
const exampleInput = document.getElementById("example");
const speakerInput = document.getElementById("speaker");
const recordingConsent = document.getElementById("recordingConsent");
const audioFileInput = document.getElementById("audioFile");
const audioPreview = document.getElementById("audioPreview");
const recordingStatus = document.getElementById("recordingStatus");
const recordButton = document.getElementById("recordButton");
const stopButton = document.getElementById("stopButton");
const saveButton = document.getElementById("saveButton");
const cancelEditButton = document.getElementById("cancelEdit");
const formMessage = document.getElementById("formMessage");
const searchInput = document.getElementById("searchInput");
const entriesElement = document.getElementById("entries");
const entryCount = document.getElementById("entryCount");
const emptyState = document.getElementById("emptyState");

let pendingAudio = null;
let previewUrl = null;
let mediaRecorder = null;
let recordingStream = null;
let recordingChunks = [];
let searchTimer = null;

function showMessage(message, isError = false) {
  formMessage.textContent = message;
  formMessage.classList.toggle("error", isError);
}

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, (character) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
  })[character]);
}

function setPendingAudio(file) {
  if (previewUrl) URL.revokeObjectURL(previewUrl);
  pendingAudio = file;
  previewUrl = file ? URL.createObjectURL(file) : null;
  audioPreview.hidden = !file;
  audioPreview.removeAttribute("src");
  if (file) {
    audioPreview.src = previewUrl;
    recordingStatus.textContent = `${file.name || "Recording ready"} · ${Math.max(1, Math.round(file.size / 1024))} KB`;
  } else {
    recordingStatus.textContent = "No audio added";
  }
}

async function requestJson(url, options = {}) {
  const response = await fetch(url, { cache: "no-store", ...options });
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.error || `Request failed (${response.status}).`);
  return payload;
}

async function loadEntries() {
  const query = searchInput.value.trim();
  try {
    const payload = await requestJson(`/api/entries?q=${encodeURIComponent(query)}`);
    renderEntries(payload.entries);
  } catch (error) {
    entriesElement.replaceChildren();
    emptyState.hidden = false;
    emptyState.querySelector("h3").textContent = "Could not load your wordbook.";
    emptyState.querySelector("p").textContent = error.message;
  }
}

function detail(label, value) {
  if (!value) return "";
  return `<p class="entry-detail"><strong>${label}:</strong> ${escapeHtml(value)}</p>`;
}

function renderEntries(entries) {
  entriesElement.innerHTML = entries.map((entry) => `
    <article class="entry-card" data-entry-id="${entry.id}">
      <div class="entry-topline">
        <h3>${escapeHtml(entry.phrase)}</h3>
        <span class="review-badge">${escapeHtml(entry.review_status)}</span>
      </div>
      <p class="entry-meaning">${escapeHtml(entry.meaning)}</p>
      ${detail("Pronunciation", entry.pronunciation)}
      ${detail("When to use it", entry.context)}
      ${detail("Example or reply", entry.example)}
      ${entry.audio_url ? `<audio controls preload="none" src="${escapeHtml(entry.audio_url)}"></audio>` : ""}
      ${entry.speaker ? `<p class="entry-meta">Voice: ${escapeHtml(entry.speaker)}</p>` : ""}
      <div class="entry-actions">
        <button class="button button-quiet" type="button" data-action="edit" data-id="${entry.id}">Edit</button>
        <button class="button button-quiet" type="button" data-action="delete" data-id="${entry.id}">Delete</button>
      </div>
    </article>
  `).join("");
  entryCount.textContent = entries.length;
  emptyState.hidden = entries.length !== 0;
  if (entries.length === 0) {
    emptyState.querySelector("h3").textContent = searchInput.value.trim()
      ? "No matching words yet."
      : "Your wordbook starts here.";
    emptyState.querySelector("p").textContent = searchInput.value.trim()
      ? "Try a different Samburu word, meaning, or context."
      : "Add a word you remember, then record how it sounds.";
  }
}

function entryValues() {
  return {
    phrase: phraseInput.value,
    meaning: meaningInput.value,
    pronunciation: pronunciationInput.value,
    context: contextInput.value,
    example: exampleInput.value,
    speaker: speakerInput.value,
  };
}

async function startRecording() {
  if (!recordingConsent.checked) {
    showMessage("Confirm you have permission before recording someone’s voice.", true);
    recordingConsent.focus();
    return;
  }
  if (!navigator.mediaDevices?.getUserMedia || !window.MediaRecorder) {
    showMessage("Recording is not supported here. Choose an audio file instead.", true);
    return;
  }

  try {
    recordingStream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const preferredType = ["audio/webm;codecs=opus", "audio/webm", "audio/mp4", "audio/ogg"]
      .find((type) => MediaRecorder.isTypeSupported(type));
    mediaRecorder = preferredType
      ? new MediaRecorder(recordingStream, { mimeType: preferredType })
      : new MediaRecorder(recordingStream);
    recordingChunks = [];
    mediaRecorder.addEventListener("dataavailable", (event) => {
      if (event.data.size) recordingChunks.push(event.data);
    });
    mediaRecorder.addEventListener("stop", () => {
      const audio = new Blob(recordingChunks, { type: mediaRecorder.mimeType || "audio/webm" });
      const extension = audio.type.includes("mp4") ? "m4a" : audio.type.includes("ogg") ? "ogg" : "webm";
      setPendingAudio(new File([audio], `samburu-recording.${extension}`, { type: audio.type }));
      recordingStream?.getTracks().forEach((track) => track.stop());
      recordingStream = null;
      recordButton.disabled = false;
      stopButton.disabled = true;
      showMessage("Recording ready. Play it back, then save the entry.");
    }, { once: true });
    mediaRecorder.start();
    recordButton.disabled = true;
    stopButton.disabled = false;
    recordingStatus.textContent = "Recording…";
    showMessage("Speak naturally. Select Stop when you’re done.");
  } catch (error) {
    recordingStream?.getTracks().forEach((track) => track.stop());
    recordingStream = null;
    showMessage(`Could not access the microphone: ${error.message}`, true);
  }
}

function resetForm() {
  entryForm.reset();
  entryIdInput.value = "";
  setPendingAudio(null);
  cancelEditButton.hidden = true;
  saveButton.textContent = "Save entry";
  showMessage("Entries stay on this device.");
}

async function editEntry(entryId) {
  const payload = await requestJson("/api/entries");
  const entry = payload.entries.find((item) => item.id === entryId);
  if (!entry) throw new Error("That entry is no longer available.");
  entryIdInput.value = entry.id;
  phraseInput.value = entry.phrase;
  meaningInput.value = entry.meaning;
  pronunciationInput.value = entry.pronunciation;
  contextInput.value = entry.context;
  exampleInput.value = entry.example;
  speakerInput.value = entry.speaker;
  recordingConsent.checked = false;
  audioFileInput.value = "";
  setPendingAudio(null);
  cancelEditButton.hidden = false;
  saveButton.textContent = "Update entry";
  showMessage(entry.audio_url ? "Save text edits without changing the existing recording." : "Update the entry details.");
  phraseInput.focus();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

entryForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (mediaRecorder?.state === "recording") {
    showMessage("Stop the recording before saving.", true);
    return;
  }
  if (pendingAudio && !recordingConsent.checked) {
    showMessage("Confirm you have permission before saving this voice recording.", true);
    recordingConsent.focus();
    return;
  }

  const existingId = entryIdInput.value;
  saveButton.disabled = true;
  showMessage(existingId ? "Updating entry…" : "Saving entry…");
  try {
    const saved = await requestJson(existingId ? `/api/entries/${existingId}` : "/api/entries", {
      method: existingId ? "PUT" : "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(entryValues()),
    });
    if (pendingAudio) {
      const contentType = pendingAudio.type.split(";")[0] || "audio/webm";
      await requestJson(`/api/entries/${saved.entry.id}/audio`, {
        method: "POST",
        headers: {
          "Content-Type": contentType,
          "X-Recording-Consent": "confirmed",
        },
        body: pendingAudio,
      });
    }
    resetForm();
    await loadEntries();
    showMessage("Entry saved. You can add or check another word.");
  } catch (error) {
    showMessage(error.message, true);
    await loadEntries();
  } finally {
    saveButton.disabled = false;
  }
});

recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", () => {
  if (mediaRecorder?.state === "recording") mediaRecorder.stop();
});
audioFileInput.addEventListener("change", () => {
  const [file] = audioFileInput.files;
  if (file) setPendingAudio(file);
});
cancelEditButton.addEventListener("click", resetForm);
searchInput.addEventListener("input", () => {
  window.clearTimeout(searchTimer);
  searchTimer = window.setTimeout(loadEntries, 160);
});

entriesElement.addEventListener("click", async (event) => {
  const button = event.target.closest("button[data-action]");
  if (!button) return;
  const entryId = Number(button.dataset.id);
  try {
    if (button.dataset.action === "edit") {
      await editEntry(entryId);
      return;
    }
    if (button.dataset.action === "delete" && window.confirm("Delete this word and its recording from this device?")) {
      await requestJson(`/api/entries/${entryId}`, { method: "DELETE" });
      await loadEntries();
      showMessage("Entry and recording deleted.");
    }
  } catch (error) {
    showMessage(error.message, true);
  }
});

window.addEventListener("beforeunload", () => {
  if (previewUrl) URL.revokeObjectURL(previewUrl);
  recordingStream?.getTracks().forEach((track) => track.stop());
});

loadEntries();