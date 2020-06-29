# Page loader
[![Maintainability](https://api.codeclimate.com/v1/badges/7010a46949e98d9d3c8c/maintainability)](https://codeclimate.com/github/PolyMaG/python-project-lvl3/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/7010a46949e98d9d3c8c/test_coverage)](https://codeclimate.com/github/PolyMaG/python-project-lvl3/test_coverage)
[![Build Status](https://travis-ci.org/PolyMaG/python-project-lvl3.svg?branch=master)](https://travis-ci.org/PolyMaG/python-project-lvl3)

**Page loader** is a utility that downloads URL. 
It downloads resources from the page and changes its routes so they became local.
You can also choose directory where you want to save the page.
## Installation
To install the utility use:
```
pip install --no-cache-dir --index-url https://test.pypi.org/simple --extra-index-url https://pypi.org/simple polymag-page-loader
```
## Usage
To run the utility after installing type:
`page-loader --output=/some_dir --log DEBUG URL_to_download`.

`URL_to_download` - the page you want to save.
`--log` - choose the level or severity of the events you want to track.
`--output` - directory where you want to  the page.


E.g. `page-loader --output=/var/tmp --log INFO https://hexlet.io/courses`

You can always call `page-loader -h` for some __help__ information.


Some examples are shown below:
##### Installation and simple example
[![asciicast](https://asciinema.org/a/DRkGO5JFMhfZTkiHHOyYsTXVc.svg)](https://asciinema.org/a/DRkGO5JFMhfZTkiHHOyYsTXVc)
##### Downloaded some resources
[![asciicast](https://asciinema.org/a/EYsnHH7YnVSkXmJ8yhkcmbNAI.svg)](https://asciinema.org/a/EYsnHH7YnVSkXmJ8yhkcmbNAI)
##### Logging
[![asciicast](https://asciinema.org/a/cR1L9reQIyVAepWwjOpMSAi05.svg)](https://asciinema.org/a/cR1L9reQIyVAepWwjOpMSAi05)
##### Handling exceptions
[![asciicast](https://asciinema.org/a/xusObcQPFtix3pLUXkzMsYlN2.svg)](https://asciinema.org/a/xusObcQPFtix3pLUXkzMsYlN2)
##### Progress bar
[![asciicast](https://asciinema.org/a/3fQmJyXqxdB3wRjVmJC2yPjZD.svg)](https://asciinema.org/a/3fQmJyXqxdB3wRjVmJC2yPjZD)