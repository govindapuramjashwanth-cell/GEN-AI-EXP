# LLM Client - VS Code Project

This project lets you send a prompt to either:
- **Gemini** (cloud API)
- **Ollama** (local model running on your computer)

## 1. Open the project

1. Extract the ZIP file.
2. Open VS Code.
3. Select **File → Open Folder**.
4. Choose the extracted `LLM_VS_Code_Project` folder.

## 2. Create and activate a virtual environment (recommended)

Open **Terminal → New Terminal** in VS Code and run:

### Windows PowerShell
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run this once in that terminal:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

## 3. Install the packages

```powershell
py -m pip install -r requirements.txt
```

## 4. Configure Gemini (only if you want to use Gemini)

1. Make a copy of `.env.example`.
2. Rename the copy to `.env`.
3. Replace the example value with your Gemini API key.

Do not share your `.env` file or upload it to GitHub.

## 5. Run the program

```powershell
py main.py
```

When asked, enter `gemini` or `ollama`, then type your question.

### To use Ollama

Install Ollama separately, start it, and download the model:

```powershell
ollama pull llama3.2
```

Then run `py main.py` and select `ollama`. Ollama must be running locally.

## 6. Run the test

```powershell
py -m unittest
```

The included test uses a fake provider, so it does not need an API key or internet access.

## Troubleshooting

- **`py` is not recognized:** install Python 3 and enable the option to add Python to PATH, then reopen VS Code.
- **Gemini API key missing:** check that `.env` is in the same folder as `main.py` and contains `GEMINI_API_KEY=...`.
- **Ollama connection refused:** start Ollama and confirm it is running at `http://localhost:11434`.
- **Package not found:** activate `.venv` and run `py -m pip install -r requirements.txt` again.
