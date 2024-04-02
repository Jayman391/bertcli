# Large Natural Language Processing

The goal of this package is to be able run several distinct NLP related algorithms in parallel either within users own projects or through a provided CLI, currently a wrapper for the BERTopic topic modeling package. There is also infrastructure to continue adding new features to said CLI as well as use existing components of the CLI within users own projects. 

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation and Usage

- Make sure that you have python 3.9 installed

### clone the repo

<code>git clone https://github.com/Jayman391/lnlp.git </code>

### create and activate virtual environment

<code>python3.9 -m venv venv</code>

<code>source venv/bin/activate</code>

### install requirements

<code>python -m pip install -r requirements.txt</code>

<code>python -m spacy download en </code>

### run CLI

<code>python main.py</code>

*for now only the topic modeling section is functional*

*you might also need to rerun the script a few times to get a good partition of the data, as sometimes the clustering algorithm gets
stuck in a local optimum which has only two clusters*

*there are also some runtime errors that occur somewhat regularly, another cause to rerun the script. There are some bugs already open on the issues page in the repo*

### add an output directory

<code>python main.py --save_dir=output</code>

### add data

#### *can be any number of columns, just has to have a column named text*

<code>python main.py --data=tests/test_data/usa-vaccine-comments.csv</code>

### specify number of samples

<code>python main.py --data=tests/test_data/usa-vaccine-comments.csv --num_samples=1000</code>

### all together now

<code>python main.py --save_dir=output --data=tests/test_data/usa-vaccine-comments.csv --num_samples=1000 </code>

## Contributing

Your contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make LNLP better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

