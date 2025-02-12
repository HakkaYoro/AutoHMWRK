# AutoHMWRK

## Description

This application automates task generation using a graphical user interface (GUI) built with PySimpleGUI. It leverages external APIs, such as OpenRouter, to generate content based on user-defined parameters. The generated content can then be formatted using LaTeX.

## Installation

1.  Clone the repository:

    ```bash
    git clone https://github.com/HakkaYoro/AutoHMWRK.git
    ```
2.  Install the required dependencies:

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

## Usage

1.  Run the application:

    ```bash
    ./run.sh
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
