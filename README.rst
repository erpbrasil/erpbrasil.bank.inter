========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |coveralls| |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/erpbrasil.bank.inter/badge/?style=flat
    :target: https://readthedocs.org/projects/erpbrasilbankinter
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.org/erpbrasil/erpbrasil.bank.inter.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/erpbrasil/erpbrasil.bank.inter

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/erpbrasil/erpbrasil.bank.inter?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/erpbrasil/erpbrasil.bank.inter

.. |requires| image:: https://requires.io/github/erpbrasil/erpbrasil.bank.inter/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/erpbrasil/erpbrasil.bank.inter/requirements/?branch=master

.. |coveralls| image:: https://coveralls.io/repos/erpbrasil/erpbrasil.bank.inter/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/erpbrasil/erpbrasil.bank.inter

.. |codecov| image:: https://codecov.io/gh/erpbrasil/erpbrasil.bank.inter/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/erpbrasil/erpbrasil.bank.inter

.. |version| image:: https://img.shields.io/pypi/v/erpbrasil.bank.inter.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/erpbrasil.bank.inter

.. |wheel| image:: https://img.shields.io/pypi/wheel/erpbrasil.bank.inter.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/erpbrasil.bank.inter

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/erpbrasil.bank.inter.svg
    :alt: Supported versions
    :target: https://pypi.org/project/erpbrasil.bank.inter

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/erpbrasil.bank.inter.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/erpbrasil.bank.inter

.. |commits-since| image:: https://img.shields.io/github/commits-since/erpbrasil/erpbrasil.bank.inter/v1.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/erpbrasil/erpbrasil.bank.inter/compare/v1.1.0...master



.. end-badges

Integração com o Banco Inter em Python

* Free software: MIT license

Installation
============

::

    pip install erpbrasil.bank.inter

You can also install the in-development version with::

    pip install https://github.com/erpbrasil/erpbrasil.bank.inter/archive/master.zip


Documentation
=============


https://erpbrasilbankinter.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
