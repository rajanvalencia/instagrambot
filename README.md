# Instagram bot

## Download chromedriver(macOS)

```
brew install chromedriver
```

## Installation

```
pip3 install selenium
pip3 install python-decouple
```

## Create environment variables
```
touch .env
```
### Inside .env file
```
USERNAME=**********

PASSWORD=**********

LIKE_LIMIT=500

COMMENT=Hello world!!
```

## Run

```python
python3 main.py
```