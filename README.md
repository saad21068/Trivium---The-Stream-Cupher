# Trivium---The-Stream-Cupher

# Trivium Cipher Implementation

## Overview
This repository contains a Python implementation of the **Trivium Cipher**, a lightweight stream cipher designed for hardware efficiency and cryptographic security. It demonstrates the initialization, key stream generation, and efficient state management of the cipher.

## Features
- **Initialization**: Accepts key and IV in hexadecimal format and converts them to binary for internal processing.
- **Warm-Up Phase**: Performs 1152 clock cycles to initialize the cipher's internal state.
- **Key Stream Generation**: Outputs a 64-byte key stream in hexadecimal format.

## How to Use
1. Run the script and provide the **key** and **IV** when prompted:
   - Enter the key in hexadecimal format (e.g., `0x123456789ABCDEF`).
   - Enter the IV in hexadecimal format (e.g., `0xFEDCBA987654321`).
2. The script will output a 64-byte hexadecimal key stream.

### Example
```bash
$ python trivium.py
Enter Key bits in hexadecimal (starting with 0x): 0x123456789ABCDEF
Enter IV bits in hexadecimal (starting with 0x): 0xFEDCBA987654321
Output: 0x<64-byte hexadecimal stream>
