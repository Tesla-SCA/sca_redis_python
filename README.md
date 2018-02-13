# sca_python
### Supply Chain Automation python packages

**List of available packages:**
1. Redis Client

**Testing Packages in this repository:**
- To run the tests
  1. Do docker-compose build
  1. docker-compose run test

**To deploy latest changes as new version to pypi**
- Change the version number in setup.py
- Run command
  1. python setup.py sdist upload -r pypi

- How does it work?
  1. This repository has a Dockerfile and docker-compose file
  1. Dockerfile defines all necessary python packages needed to run the tests
  1. docker-compose file has all the dependent containers that are needed to run tests
  1. docker-compose run test has a command "nosetests" that runs all the tests found in each package.
        1. Each package must have tests in "tests" folder
        1. Each test file inside such test folder needs to extend unittest framework and tests must start with test_*****
