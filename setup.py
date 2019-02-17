#! /usr/bin/env python

from distutils.core import setup

import pystsup

setup (
        name = pystsup.__name__,
        version = pystsup.__version__,
        packages = [ 'pystsup','pystsup/data','pystsup/evolutionary', 'pystsup/evolutionary/metrics', 'pystsup/evolutionary/selection', 'pystsup/evolutionary/crossover', 'pystsup/evolutionary/mutation', 'pystsup/utilities']

)





