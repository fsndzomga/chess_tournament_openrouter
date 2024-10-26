# Benchmarking the Strategic Planning and Tactical Intelligence of LLMs

This project benchmarks the strategic planning and tactical intelligence of Large Language Models (LLMs) using chess as a case study. The goal is to evaluate how well LLMs perform in a structured, tactical environment like chess, where complex reasoning is required. The code is designed to run a tournament between different models, including various LLMs and the Stockfish chess engine, and provides an Elo-based ranking to assess each model's performance.

## Table of Contents
1. [Features](#features)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Configuration](#configuration)
5. [Citing This Project](#citing-this-project)
6. [License](#license)

## Features
- Competes multiple LLMs and the Stockfish chess engine in a series of chess games.
- Uses the Elo rating system to evaluate and rank the strategic planning and tactical intelligence of each model.
- Logs results and provides a final leaderboard of model performances.
- Easily configurable to add new models or adjust game settings.

## Installation

### Prerequisites
1. **Python**: Ensure you have Python 3.8 or higher installed. You can check your version with:
   ```bash
   python --version
   ```

2. **Stockfish**: Install the Stockfish chess engine, which is required for running the tournament with the Stockfish model.

   - **macOS**: Install Stockfish using Homebrew:
     ```bash
     brew install stockfish
     ```
   - **Linux**: Install Stockfish from your package manager (e.g., `apt` for Ubuntu):
     ```bash
     sudo apt install stockfish
     ```
   - **Windows**: Download the Stockfish executable from the [official site](https://stockfishchess.org/download/) and add it to your system PATH.

3. **API Keys**: If you plan to use LLMs from OpenAI or OpenRouter, make sure to set up the necessary API keys. Create a `.env` file in the project root with the following format:
   ```plaintext
   OPENAI_API_KEY=your_openai_api_key
   OPENROUTER_API_KEY=your_openrouter_api_key
   ```

### Install Python Dependencies

Clone this repository and install the required packages:

```bash
git clone https://github.com/fsndzomga/chess_tournament_openrouter.git
cd chess_tournament_openrouter
pip install -r requirements.txt
```

This will install the following dependencies:
- `openai` - For interacting with OpenAI's API and models available via OpenRouter.
- `instructor` - To parse next moves using structured outputs.
- `python-dotenv` - For loading environment variables.
- `chess` - The `python-chess` library for managing chess rules and moves.
- `pydantic` - For data validation and structured responses.

## Usage

1. **Configure Models**: You can configure the models you want to include in the tournament in the `models.py` file. Each model entry should contain:
   - `name`: Name of the model.
   - `provider`: The provider of the model (e.g., `openai`, `openrouter`, or `stockfish`).
   - `model_id`: The model identifier, required for LLMs.
   - `rating`: Initial Elo rating (default is set to 1500).

2. **Run the Tournament**: Once configured, you can start the tournament by running:
   ```bash
   python main.py
   ```

3. **Results**: After the tournament completes, results are displayed in the console and saved in `tournament_results.csv`, including the final Elo ratings, win/loss counts, and draws for each model.

## Configuration

### Adding New Models
To add new models, modify the `models.py` file and add entries with the required details. For instance:

```python
models = [
    {
        'name': 'anthropic/claude-3.5-sonnet',
        'provider': 'openrouter',
        'model_id': 'anthropic/claude-3.5-sonnet',
        'rating': 1500
    },
    {
        'name': 'gpt-4o',
        'provider': 'openai',
        'model_id': 'gpt-4o',
        'rating': 1500
    },
    {
        'name': 'stockfish',
        'provider': 'stockfish',
        'model_id': '/path/to/stockfish',
        'rating': 1500
    }
]
```

### Adjusting Game Settings
The number of games played between each model can be adjusted in `main.py` by setting `n_games`:

```python
n_games = 3
```

## Citing This Project

If you use this project in your research or reference it in any publication, please cite it as follows:

```plaintext
Franck S. Ndzomga, "Benchmarking the Strategic Planning and Tactical Intelligence of LLMs," 2024. GitHub repository: https://github.com/fsndzomga/chess_tournament_openrouter
```

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

```plaintext
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Contributing

Contributions are welcome! If you spot an issue or have a suggestion, please open an issue or submit a pull request on GitHub. Together, we can enhance this project and build a comprehensive benchmark for strategic planning and tactical intelligence in LLMs.
