# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Remhos(MakefilePackage):
    """Remhos (REMap High-Order Solver) is a CEED miniapp that performs monotonic
       and conservative high-order discontinuous field interpolation (remap)
       using DG advection-based spatial discretization and explicit high-order
       time-stepping.
    """
    tags = ['proxy-app']

    homepage = "https://github.com/CEED/Remhos"
    url      = "https://github.com/CEED/Remhos/archive/v1.0.tar.gz"
    git      = "https://github.com/CEED/Remhos.git"

    version('develop', branch='master')
    version('1.0', sha256='dec48b432af810ba667b49487a8f7b8ebd16d9fa9d0046c765b9463dbb15d8c6')

    variant('metis', default=True, description='Enable/disable METIS support')

    depends_on('mfem+mpi+metis', when='+metis')
    depends_on('mfem+mpi~metis', when='~metis')

    depends_on('mfem@develop', when='@develop')
    depends_on('mfem@4.1.0:', when='@1.0')

    @property
    def build_targets(self):
        targets = []
        spec = self.spec

        targets.append('MFEM_DIR=%s' % spec['mfem'].prefix)
        targets.append('CONFIG_MK=%s' % spec['mfem'].package.config_mk)
        targets.append('TEST_MK=%s' % spec['mfem'].package.test_mk)

        return targets

    # See lib/spack/spack/build_systems/makefile.py
    def check(self):
        targets = []
        spec = self.spec

        targets.append('MFEM_DIR=%s' % spec['mfem'].prefix)
        targets.append('CONFIG_MK=%s' % spec['mfem'].package.config_mk)
        targets.append('TEST_MK=%s' % spec['mfem'].package.test_mk)

        with working_dir(self.build_directory):
            make('test', *targets)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('remhos', prefix.bin)