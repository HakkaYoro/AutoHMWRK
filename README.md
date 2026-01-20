# AutoHMWRK

## Description

This application automates task generation using a graphical user interface (GUI) built with **FreeSimpleGUI**. It leverages external APIs (like OpenRouter, Google Gemini, or any OpenAI-compatible provider like Z.ai or DeepSeek) to generate extensive academic content. The content is then formatted into a professional LaTeX document and compiled to PDF automatically.

**Key Features:**
- **Modern GUI**: Simplified interface for quick task generation.
- **Flexible API Support**: Connect to any OpenAI-compatible API (Z.ai, DeepSeek, local LLMs) or use standard OpenRouter / Gemini.
- **DeepSeek Reasoning Support**: Optional filter to remove `<think>` tags from reasoning models.
- **Automatic Image Injection**: Scrapes relevant images based on your topic and embeds them into the final PDF.
- **Smart Launcher**: `run.sh` handles virtual environments and dependencies automatically.

## Installation (Linux)

This application is optimized for Arch Linux but should work on any distro with Python 3.11+ and TeX Live.

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/HakkaYoro/AutoHMWRK.git
    cd AutoHMWRK
    ```

2.  **System Requirements**:
    Ensure you have `python3.11`, `pip`, and `texlive` installed. For Spanish documents, you specifically need `texlive-langspanish`.
    
    *Arch Linux:*
    ```bash
    sudo pacman -S python311 texlive-core texlive-latexextra texlive-langspanish
    ```

3.  **Configuration**:
    Create a `.env` file in the root directory (use `.env.example` as a template).

    ```bash
    cp .env.example .env
    nano .env
    ```
    
    **Example `.env` content:**
    ```ini
    # --- Option A: Custom / OpenAI Compatible (Recommended for Z.ai, DeepSeek, etc) ---
    OPENAI_API_KEY=sk-your-key
    OPENAI_BASE_URL=https://api.yourprovider.com/v1
    OPENAI_MODEL=model-name
    # Set to true if using reasoning models like deepseek-r1 to hide <think> blocks
    REASONING_FILTER=false 

    # --- Option B: OpenRouter ---
    OPENROUTER_API_KEY=sk-or-your-key
    OPENROUTER_MODEL=openai/gpt-3.5-turbo
    ```

## Usage

1.  **Run the Launcher**:
    Simply execute the script. It will set up the virtual environment and install dependencies automatically.
    
    ```bash
    ./run.sh
    ```

2.  **Generate**:
    - Fill in the student data and topic.
    - Select your **API Provider** from the dropdown (matches your `.env` config).
    - Check "Desea añadir imágenes?" to automatically search and add images.
    - Click **Generar**.

3.  **Output**:
    The PDF will be generated in the `generated_docs` folder, automatically renamed with the student's details.

## Troubleshooting

- **LaTeX Error (babel):** If you see `! Package babel Error: Unknown option 'spanish'`, install `texlive-langspanish`.
- **Images not showing:** Ensure you have internet access. The script uses DuckDuckGo/Google to find images.
- **API Errors:** Check `AutoHMWRK.log` for details. Ensure your Base URL is correct in `.env`.

## License

MIT License.
