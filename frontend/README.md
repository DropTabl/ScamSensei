# ScamSensei – Frontend

**ScamSensei** is a modern, multilingual web interface designed to detect and explain potential scams in text, URLs, and voice messages. It communicates with a FastAPI backend and provides users with a responsive, intuitive UI and clear risk assessments.

---

## ✨ Features

- **Text Analysis**: Scan messages for scam indicators and get detailed insights.
- **URL Analysis**: Check if links are malicious or suspicious using advanced tools.
- **Audio Transcription**: Upload voice messages, transcribe them, and detect scam patterns.
- **Multilingual Support**: Interface and analysis available in English, Spanish, French, German, and Italian.
- **Detailed Reports**: View risk scores, highlighted scam phrases, and explanation cards.
- **Text-to-Speech**: Hear analysis results using built-in voice synthesis.
- **Responsive UI**: Fully optimized for mobile, tablet, and desktop.

---

## 🛠️ Technology Stack

- **React** & **TypeScript** – Component-driven development
- **Vite** – Fast, modern build tool
- **Tailwind CSS** – Utility-first styling
- **shadcn/ui** – Component system based on Radix UI
- **Lucide React** – Icon library
- **React Router** – Page routing
- **Recharts** – Data visualization (score bars, graphs)
- **TanStack Query** – API state management

---

## 🧱 Architecture Highlights

- Component-based layout
- Context-based state management (e.g. language settings)
- Custom hooks for API interaction and feature logic
- Clean, modular folder structure for scalability
- Accessible and responsive design

---


## 🚀 Getting Started

### 1. Clone the repository

```sh
git clone https://github.com/yourusername/scamsensei.git
cd scamsensei/frontend
```

### 2. Install dependencies

```sh
npm install
```

### 3. Start the development server

```sh
npm run dev
```
Open your browser and navigate to `http://localhost:3000` to view the application.


## 📡 Backend Integration

This app depends on a running backend at [http://localhost:8000](http://localhost:8000) or your deployed API.

Ensure the backend exposes:

- `POST /analyze-text` – Analyze text messages
- `POST /analyze-url` – Check if a URL is dangerous
- `POST /analyze-audio` – Upload and analyze voice messages


