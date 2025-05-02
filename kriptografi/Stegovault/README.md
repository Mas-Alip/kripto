# Stegovault

Stegovault is a secure application designed to hide important files (PDF and DOCX) within images using advanced steganography techniques. The application utilizes AES encryption to ensure that the files are securely embedded and can only be extracted by authorized users.

## Features

- **File Encryption**: Uses AES encryption to secure files before embedding them into images.
- **Steganography**: Hides encrypted files within image files, making them undetectable to the naked eye.
- **File Extraction**: Allows users to extract hidden files from images and decrypt them for access.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/stegovault.git
   ```
2. Navigate to the project directory:
   ```
   cd stegovault
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```
   python src/app.py
   ```
2. Follow the on-screen instructions to either embed a file into an image or extract a file from an image.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.