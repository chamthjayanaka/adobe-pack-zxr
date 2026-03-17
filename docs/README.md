# Adobe Acrobat Toolkit Documentation

## Quick Start

```python
from adobe_toolkit import AdobeAcrobatClient

client = AdobeAcrobatClient()
if client.is_installed():
    client.connect()
    print(f"Version: {client.get_version()}")
```

## API Reference

See individual module documentation.
