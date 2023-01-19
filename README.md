<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://whys.dev/">
    <img src="static/core/img/whys-logo.webp" alt="Logo" width="150">
  </a>

  <h3 align="center">Whys API</h3>

  <p align="center">
    REST API Exercise
      <br />
      <br />
      <a href="https://whys.unar.dev/">View Demo</a>
      ·
      <a href="https://github.com/johnunar/whysapi/issues">Report Bug</a>
      ·
      <a href="https://github.com/johnunar/whysapi/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->

## Table of Contents

* [About the Project](#about-the-project)
    * [Built With](#built-with)
* [Getting Started](#getting-started)
    * [Prerequisites](#prerequisites)
    * [Installation](#installation)
* [Usage](#usage)
    * [Authentication](#authentication)
* [Contact](#contact)

<!-- ABOUT THE PROJECT -->

## About The Project

This is an exercise for the company Whys.

### Built With

* [Python 3.11](https://www.python.org/)
* [Django](https://www.djangoproject.com/)

## Getting Started

### Prerequisites

* [Docker](https://www.docker.com/)


### Installation

1. Clone the repo
```sh
git clone https://github.com/johnunar/whysapi.git
```

2. Run the docker-compose
```sh
docker-compose up
```


## Usage

This is a REST API, so you can use any tool to test it. I recommend [Insomnia](https://insomnia.rest/).

There are 3 endpoints:
### /import/
This endpoint is used to import the data using JSON. You can use the file `data.json` in the root of the project to test it.
### /detail/<model_name>/
This endpoint is used to get a list of model objects from the database. You can use the following models:
* `attributename`
* `attributevalue`
* `attribute`
* `product`
* `productattribute`
* `image`
* `productimage`
* `catalog`
### /detail/<model_name>/\<pk>/
This endpoint is used to get a specific model object from the database, where `pk` is the primary key of the object.

404 Not Found will be returned if the object does not exist.

### Authentication

Authentication has not been implemented for purposes of this exercise.

<!-- CONTACT -->

## Contact

Jan Unar

* [johnny@unar.dev](mailto:johnny@unar.dev)
* [unar.dev](https://unar.dev/)

Project Link: [https://github.com/johnunar/whysapi](https://github.com/johnunar/whysapi)