# Parse Typescript Node

## 🎯 Project Overview
A lightweight **Node.js/TypeScript** CLI tool that parses HTTP access logs, extracts status codes, categorizes them, and prints concise statistics.

### Features
- **Async line‑by‑line parsing** using `readline` for minimal memory usage.
- Categorizes status codes into the classic ranges (1xx‑5xx).
- Generates two count maps:
  - **Category summary** (e.g. `2xx‑ Success: 10`).
  - **Individual status‑code frequencies** (e.g. `200: 9`).
- Simple zero‑dependency runtime – only built‑in Node modules.

## 📁 Repository Layout
```
Parse_typescript_node/
├─ src/
│  ├─ index.ts      # entry point, orchestrates parsing & stats
│  ├─ parser.ts     # reads a log file and returns an array of numbers
│  ├─ stats.ts      # builds the category & code count objects
│  └─ categorizer.ts# utility that maps a numeric code to a label
├─ logs/
│  └─ sample.log    # tiny demo log (4 lines)
├─ package.json
└─ README.md        # <‑‑ you are reading this file
```

## ⚙️ Setup & Installation
1. **Prerequisites** – Node 18+ (includes native ESM support) and `npm`.
2. Open a terminal at the project root and run:
   ```bash
   npm install            # installs TypeScript as a dev dependency
   npx tsc                # compiles the `src` folder to `dist`
   ```
   This will generate a `dist/` folder containing compiled JavaScript.

## 🚀 Running the CLI
```bash
node dist/index.js <log‑file>
```
Replace `<log‑file>` with the path to any Apache/Nginx‑style log file. Example using the bundled sample:
```bash
node dist/index.js logs/sample.log
```
**Expected output** (from the sample log):
```
=== Category Summary ===
2xx‑ Success: 2
4xx‑ Client Error: 1
5xx‑ Server Error: 1

=== Status Code Counts ===
200: 2
401: 1
500: 1
```

## 📦 Scripts (optional shortcuts)
Add these to `package.json` for convenience:
```json
"scripts": {
  "build": "tsc",
  "start": "npm run build && node dist/index.js"
}
```
Now you can simply run:
```bash
npm start logs/sample.log
```

## 🧪 Testing & Extending
- **Add more logs** to `logs/` and run the CLI against them.
- Extend `categorizer.ts` to support custom ranges or textual descriptions.
- Hook the tool into CI pipelines to automatically verify that your services return expected status‑code distributions.

## 📜 License
This snippet is for personal learning – feel free to adapt or publish under any license you prefer.
