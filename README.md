# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/JPEWdev/py-spdx-license/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                  |    Stmts |     Miss |   Cover |   Missing |
|-------------------------------------- | -------: | -------: | ------: | --------: |
| src/py\_spdx\_license/\_\_init\_\_.py |        3 |        0 |    100% |           |
| src/py\_spdx\_license/\_\_main\_\_.py |        4 |        0 |    100% |           |
| src/py\_spdx\_license/ast.py          |      492 |       66 |     87% |59, 64, 67, 124, 128, 136, 139-142, 145-163, 170-176, 188, 204, 208, 211, 226, 247-252, 258, 262, 280, 284, 330, 337, 384, 411, 426, 433, 493, 516-525, 539, 555, 605, 727, 772-774 |
| src/py\_spdx\_license/cli.py          |       59 |        0 |    100% |           |
| src/py\_spdx\_license/version.py      |        1 |        0 |    100% |           |
|                             **TOTAL** |  **559** |   **66** | **88%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/JPEWdev/py-spdx-license/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/JPEWdev/py-spdx-license/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/JPEWdev/py-spdx-license/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/JPEWdev/py-spdx-license/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2FJPEWdev%2Fpy-spdx-license%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/JPEWdev/py-spdx-license/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.