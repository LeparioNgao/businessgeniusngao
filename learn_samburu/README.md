# Learn Samburu

A local-first prototype for collecting Samburu words, meanings, usage notes, and speaker recordings.

## Run

From this directory, run:

```bash
python3 server.py
```

Open <http://127.0.0.1:8001>. The app uses only Python's standard library. Microphone recording works in browsers that support `MediaRecorder`; choosing an existing audio file is also supported.

## Data and privacy

Entries are stored in `data/learn_samburu.sqlite3`; audio is stored in `data/audio/`. Both stay on this computer and are excluded from Git. Back up the `data` directory to preserve the wordbook. Ask permission before recording or saving another person's voice. The prototype is bound to this computer and is not designed for public hosting.

Entries are marked **Needs review** until a fluent speaker checks the wording, pronunciation, and context. This prototype does not publish recordings or verify translations.