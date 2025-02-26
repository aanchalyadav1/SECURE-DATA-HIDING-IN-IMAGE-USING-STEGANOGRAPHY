# SECURE-DATA-HIDING-IN-IMAGE-USING-STEGANOGRAPY

# Image-Based Steganography Tool

A secure and efficient steganography application designed to conceal messages within images, ensuring confidentiality and privacy. This project provides a user-friendly interface for encoding and decoding secret messages using password protection.

# Description

This project is a simple steganography application that allows users to hide and retrieve messages within images using a password-protected encoding method. 

The application is built using Python and Tkinter for the GUI, along with OpenCV and PIL for image processing.

# Overview

Steganography is a technique that allows information to be hidden within non-suspicious digital media. This project enables users to embed text messages into image files while maintaining their original appearance. The encoded images can then be shared without raising suspicion, and only authorized users can extract the hidden data.

# Features

Message Encoding: Hide secret messages within image files using steganographic techniques.

Message Decoding: Extract hidden messages from encoded images.

Password Protection: Secure encoding and decoding with a user-defined password.

User-Friendly GUI: Built with Tkinter for ease of use.

Image Processing: Utilizes OpenCV and PIL libraries for handling image files.

Supports Multiple Formats: Works with popular image formats such as PNG and BMP.


# Technology Stack

Python: Core programming language used for development.

Tkinter: GUI framework for user interaction.

PIL (Pillow): Image processing library.

OpenCV: Additional image handling capabilities.


# Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/Akshay-S-Gupta/IBM-Cybersecurity-Internship.git
   ```
2. Navigate to the project directory:
   ```sh
   cd IBM-Cybersecurity-Internship
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```



# Usage

# 1. Encoding a Message

Open the application.

Select an image file.

Enter the secret message and a password.

Click "Encode" to embed the message.

Save the encoded image.



# 2. Decoding a Message

Load the encoded image.

Enter the correct password.

Click "Decode" to reveal the hidden message.

# Security Considerations

The strength of password protection ensures unauthorized users cannot extract hidden messages.

Use high-resolution images to minimize distortion after encoding.

Avoid sharing passwords publicly to maintain confidentiality.
