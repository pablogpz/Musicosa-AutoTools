# Musicosa Runner
**Author:** Juan Pablo García Plaza Pérez (@pablogpz)

## Overview

Musicosa Runner is a multi-stage pipeline designed to parse and process Musicosa Contestant Submissions to generate
the final video bits (or stitch the entire final video)

## Requirements

- Python
- pip
- `ffmpeg` binaries in your PATH

## Usage

To run the pipeline, execute the main script:
```sh
python musicosa.py
```

### Environment
See `.env.example` to provide the mandatory env vars

## Configuration

Musicosa Runner can be configured through the `musicosa.config.toml` file

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

© 2024 pablogpz