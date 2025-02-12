# AutoHMWRK

## Description

This application automates task generation using a graphical user interface (GUI) built with PySimpleGUI. It leverages external APIs, such as OpenRouter, to generate content based on user-defined parameters. The generated content can then be formatted using LaTeX.

Currently, the task generation is programmed for the "Alejandro de Humboldt" University. Future versions will allow for custom university names, sections, and logos.

If you want to modify these things, review `openrouter.py` and `gemini.py` respectively. You can also change the logo located in the `logos` folder.

## Installation (Linux)

This application requires pdflatex to generate PDF documents. These instructions are for Linux.

1.  Clone the repository:

    ```bash
    git clone https://github.com/HakkaYoro/AutoHMWRK.git
    ```
2.  Install the required dependencies:

    ```bash
    sudo apt-get update
    sudo apt-get install -y texlive-latex-base
    ```

    ```bash
    pip install -r requirements.txt
    ```
3.  Set up the environment variables:

    *   Create a `.env` file in the root directory.
    *   Add the necessary API keys and other configuration parameters to the `.env` file.  Example:

        ```
        OPENROUTER_API_KEY=your_openrouter_api_key
        OPENROUTER_MODEL=your/llm
        GOOGLE_GEMINI_API_KEY=your_google_gemini_api_key
        GOOGLE_GEMINI_MODEL=llm-name
        ```

## Installation (Windows)

This application requires Python 3 and pdflatex to generate PDF documents. These instructions are for Windows. This application has not been tested on Windows yet.

1.  Install Python 3:

    *   Download the Python 3 installer from [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/).
    *   Run the installer and follow the instructions. Make sure to check "Add Python to PATH" during installation.
2.  Install Git:

    *   Download the Git installer from [https://git-scm.com/download/windows](https://git-scm.com/download/windows).
    *   Run the installer and follow the instructions. Make sure to check "Add Git to PATH" during installation.
3.  Clone the repository:

    ```bash
    git clone https://github.com/HakkaYoro/AutoHMWRK.git
    ```
4.  Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```
5.  Set up the environment variables:

    *   Create a `.env` file in the root directory.
    *   Add the necessary API keys and other configuration parameters to the `.env` file.  Example:

        ```
        OPENROUTER_API_KEY=your_openrouter_api_key
        OPENROUTER_MODEL=your/llm
        GOOGLE_GEMINI_API_KEY=your_google_gemini_api_key
        GOOGLE_GEMINI_MODEL=llm-name
        ```
6.  Install MiKTeX:

    *   Download the MiKTeX installer from [https://miktex.org/download](https://miktex.org/download).
    *   Run the installer and follow the instructions.
7.  Add MiKTeX to the PATH:

    *   Open the Control Panel.
    *   Go to System and Security > System > Advanced system settings.
    *   Click the "Environment Variables" button.
    *   In the "System variables" section, find the "Path" variable and click "Edit".
    *   Add the path to the MiKTeX bin directory to the end of the "Variable value" field. For example: `C:\Program Files\MiKTeX 2.9\miktex\bin\x64`.
    *   Click "OK" to save the changes.

## Usage

1.  Run the application:

    *   For Linux:

        ```bash
        ./run.sh
        ```
    *   For Windows:

        ```bat
        run.bat
        ```
2.  The GUI will appear, allowing you to input the task parameters.
3.  Click the "Generar" button to generate the task.
4.  The generated task will be displayed in the GUI and saved to the `generated_docs` directory.

## Contributing

Contributions are welcome! Please follow these steps:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes and commit them with descriptive messages.
4.  Submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
