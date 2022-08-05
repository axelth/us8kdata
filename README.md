# Data analysis
- Document here the project: us8kdata
- Description: This package holds tools for converting the data of the Urban Sounds 8K data set, and provides a data loader class to provide the cleaned data to other packages.
- Data Source: https://urbansounddataset.weebly.com/urbansound8k.html
- Type of analysis: Sound event classification and detection

# Install

Go to `https://github.com/axelth/us8kdata` to see the project, manage issues,

Install ffmpeg and make sure it is on the path. 
```bash
brew install ffmpeg
```

Create virtualenv 
```bash
pyenv virtualenv usk8data; pyenv activate usk8data;
```

and install the project in either development mode

```bash
pip install -e .
```

or as a regular package.

```bash
pip install .
```

