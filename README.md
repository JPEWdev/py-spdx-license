# Python SPDX License Parser

A Zero-dependency SPDX License expression parser.

## Installation

```shell
pip install py-spdx-license
```

## Usage

```python
import py_spdx_license

parsed = py_spdx_license.parse("MIT OR (Apache-2.0 AND Apache-2.0)")
print(parsed)         # Output: MIT OR Apache-2.0 AND Apache-2.0
print(parsed.sort())  # Output: Apache-2.0 OR MIT
```

## License

[MIT](./LICENSE)
