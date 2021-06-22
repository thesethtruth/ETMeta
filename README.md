# ETMeta
### (pronounced: ET-meta)
This project is currently in Alpha development. Precise content and included features are still open to debate. Consider this if you are interested in using this package. 

 * [Getting started](#getting-started)
 * [Excel integration](#excel-integration)
 * [EMA workbench](#ema-workbench)
 * [Tutorials and examples](#tutorials-and-examples)

---
### Getting started

This project is currently being released to work with `pip` for an easy install.
To install ETM-EMA-API use the following command (in your `venv` of choice).

`pip install https://github.com/thesethtruth/ETM-EMA-API/archive/main.zip`

Dependencies are specified in the setup.py without versioning to retain flexibility for users. Please make sure that you have latest versions of the modules listed below.

* `pandas`
* `numpy`
* `requests`
* `beautifulsoup4`
* `openpyxl`
* `seaborn`

If you want to use `ema_workbench`, please use the [documentation](#https://emaworkbench.readthedocs.io/en/latest/) to install this package and optional dependencies. 

### Excel integration
To make give scenario generation more overview, this packages uses Excel worksheets to generate ETM slider values and track sources within the Excel in any way the user sees fit. A collection of scenarios slider settings can be requested from the ETM and listed within a single Excel file. The same Excel can later be used to create new scenarios based on values within the Excel sheet. Just refer to the columns of the to-be-created scenarios as range or list. Column letters will automatically be converted (e.g. `'A' == 0 index`) and column headers will be used as scenario titles, unless titles are explicitly supplied. 

In the tutorials below minimal examples are given with some more comments on specific arguments for various downloads/uploads to/from Excel sheets. Inspect the `sheets` folder to get an idea of how you can work with this function.

### EMA workbench
[Exploratory Modelling and Analysis (EMA) Workbench](#https://emaworkbench.readthedocs.io/en/latest/) is a great tool that allows us to implement parametric experiment on nearly any Python function. Using the package and the ETM API, we can write simple wrappers that use the ET Engine API ([ETE](#https://github.com/quintel/etengine)) to generate higher-level results based on varying inputs. For extended documentation on EMA, please refer to its official documentation. 

In the tutorials below a minimal example is given which varies the ratio of solar to wind for a given total energy production from VRE sources in the KEA scenario. Inspect the `images` to get a glance of possible insight you could gain from using parametric experiments.

### Tutorials and examples

* [EMA solar-to-wind-ratio experiment on KEA scenario](tutorials/example-ema-etm.py)
    * [Example result](images)
* [Excel scenario downloads and uploads](tutorials/tutorial-etm-sheets.py)
    * [Example sheets](sheets)