# csp-citibike

CSP Examples for [Citi Bike Data](https://citibikenyc.com/system-data)

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/timkpaine/csp-citibike/main?urlpath=lab)

## Overview

This repository explores Citi Bike [historical](https://s3.amazonaws.com/tripdata/index.html) and [Realtime](https://gbfs.citibikenyc.com/gbfs/2.3/gbfs.json) data with [`csp`](https://github.com/point72/csp).

## Install Dependencies

```
pip install csp httpx pandas
```

## Example

- [Realtime.ipynb](./Realtime.ipynb)
- [Historical.ipynb](./Historical.ipynb)

## Web App

```bash
python -m csp_citibike.webapp
```

![Picture of citibike availability map and grid](https://raw.githubusercontent.com/csp-community/csp-citibike/main/docs/app.png)