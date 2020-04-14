============
Contributing
============

Creating your environment
-------------------------

There are several ways to create your isolated environment. I recommend using virtualenvwrapper_\ . The example below assumes you have it installed.

::

    git clone git@github.chrobinson.com:DataScienceSourceCode/rules.git
    cd rules
    mkvirtualenv -a $(pwd) rules

The ``mkvirtualenv`` command creates a isolated Python environment (virtualenv) called ``bloggingforhumans`` and sets its working directory to your current working directory.

.. _virtualenvwrapper: http://virtualenvwrapper.readthedocs.io/en/latest/

Installing Requirements
-----------------------

If your virtualenv is created and activated, you can install the parts you need for development::

    pip install -r requirements/dev.txt

Installing Pre-commit Hooks
---------------------------

Pre-commit hooks are scripts that run every time you make a commit. If any of the scripts fail, it stops the commit. You can see a listing of the checks in the ``.pre-commit-config.yaml`` file.

::

    pre-commit install


Testing
-------

This template sets up the use of PyTest_, Tox_, Coverage_, and Flake8_. When you install the ``dev.txt`` requirements, the production and testing requirements are also installed. Tox_ is used to run the test suite.

Tests go in the appropriately named ``tests`` directory, and must start with ``test_`` for pytest to recognize them.

There are several ways to run your tests, depending on what you are doing. The simplest is to use the commands in the ``Makefile``\ .

``make lint`` will run Flake8 and lint your code.

``make test`` will run pytest using the default Python.

``make coverage`` will run pytest and generate HTML and terminal output of the test coverage. The HTML coverage report is available in the ``htmlcov`` directory.

``make test-all`` runs tox, which runs all the above, and will also test against multiple versions of Python (if configured). You should ensure that this command passes before releasing a version.

.. _Tox: https://tox.readthedocs.io/en/latest/
.. _Pytest: https://docs.pytest.org/en/latest/
.. _Coverage: https://coverage.readthedocs.io/en/latest/
.. _Flake8: http://flake8.pycqa.org/en/latest/

Setting Requirements
--------------------

Your requirements are split into parts: dev, prod, and test. They exist in the directory ``requirements``\ . ``Prod`` requirements are required for your app to work properly. ``Dev`` requirements are packages used to help develop this package, which include things for building documentation, packaging the app and generating the changelog. ``Test`` requirements are the libraries required to run tests.

As you develop, you will likely only modify ``requirements/prod.txt``\ .


Releasing your app
------------------

Once you have developed and tested your app, or revisions to it, you need to release new version.

Deciding the version
--------------------

First decide how to increase the version. Using `semantic versioning`_:

> Given a version number MAJOR.MINOR.PATCH, increment the:
>
> 1. MAJOR version when you make incompatible API changes,
> 2. MINOR version when you add functionality in a backwards-compatible manner, and
> 3. PATCH version when you make backwards-compatible bug fixes.

This is a judgement call, but here are some guidelines:

1. A database change should be a MINOR version bump at least.
2. If the PATCH version is getting above ``10``\ , as in ``1.0.14``\ , it is acceptable to do a MINOR version.
3. Dropping or adding support of a version of Python or another dependency should be at least a MINOR version.

.. _semantic versioning: https://semver.org/

Versioning and releasing
------------------------

Once you've decided how much of a version bump you are going to do, you will run one of three commands:

``make release-patch`` will automatically change the patch version, e.g. ``1.1.1`` to ``1.1.2``\ .

``make release-minor`` will automatically change the minor version, e.g. ``1.1.1`` to ``1.2.0``\ .

``make release-major`` will automatically change the major version, e.g. ``1.1.1`` to ``2.0.0``\ .

Each of these commands do several things:

1. Update the ``CHANGELOG.md`` file with the changes made since the last version, using the Git commit messages.
2. Increments the appropriate version number in the appropriate way.
3. Commits all the changes.
4. Creates a Git tag with the version number.
5. Pushes the repository and tags to the GitHub server.
6. Jenkins recognizes the new tag and publishes the package on PyPI
