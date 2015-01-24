# pushetta-py

Interface to use Pushetta API with Python

# Gettin started

```python
from pushetta.pushetta import Pushetta

# API Key You get after signup on www.pushetta.com
API_KEY="00112233445566778899aabbccddeeff00112233"
p=Pushetta(API_KEY)
p.pushMessage("raspi", "Hello World"")
```
