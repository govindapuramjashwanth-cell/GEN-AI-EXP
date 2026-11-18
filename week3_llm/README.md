# Week 3 - LLM Monitoring

## Features
- Gemini and Ollama providers
- Input/output/total token tracking
- Request latency measurement
- Estimated cost calculation (sample rates only; verify actual pricing)
- Retry for selected temporary errors
- MongoDB logging in database `llm_monitoring`, collection `call_logs`

## Windows / VS Code setup
1. Extract the ZIP and open this folder in VS Code.
2. Open Terminal and run:

```powershell
py -m venv .venv
.venv\\Scripts\\Activate.ps1
py -m pip install -r requirements.txt
```

If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`, then activate again.

3. Copy `.env.example` to `.env`. Add your Gemini API key if selecting Gemini. For MongoDB Atlas, replace `MONGODB_URI` with your Atlas connection string. Keep `.env` private.
4. Ensure MongoDB is running locally, or use a valid Atlas URI.
5. Run:

```powershell
py main.py
```

Choose `1` for Gemini or `2` for Ollama, then enter a question.

For Ollama, install/start Ollama and run `ollama pull llama3.2` in a separate terminal before selecting option 2.

## Test
Run `py -m unittest`. The test uses fake provider and logger objects, so it does not need a live API, Ollama, or MongoDB.

## Notes
The cost rates in `cost_calculator.py` are examples, not verified current Gemini prices. Update them before relying on cost estimates.
