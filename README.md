# Code Init

Initialize your competitive programming template after reading the problems, complete with the details of the problem. This tool is made specially for [uhunt](https://uhunt.onlinejudge.org/). Future updates might include other sites.

![alt text](https://uhunt.onlinejudge.org/images/uva.png "uhunt")

## Getting Started

### Prerequisites

1. Install [ghostscript](https://www.ghostscript.com/download.html), and choose the PDF interpreter/renderer.
2. Have **Python** v3.0 above installed on your machine. Check your version by calling `python --version` in terminal

### Installing

```bash
pip install ghostscript --user
git clone https://github.com/T-kON99/code-init
cd code-init
python init.py -help
```

### Usage

> Initiate uhunt problem 787 as a python file
```bash
python code-init.py -p 787 -lang py
```
> Force overwrite existing file, by default it will skip the file if it exists
```bash
python code-init.py -p 787 -lang py -o
```

### Footnotes

- All problems will be fetched and saved under      location `./problems`
- Code file will be generated based from `./config/config.json`, configurable.
- Enjoy and happy hunting!
