# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *

class Armpl(Package):
    """Arm performance Libraries provide advanced math functions tuned for Arm processors.  

You must edit your packages.yaml file to point to the system modules and set buildable=false.

See https://spack.readthedocs.io/en/latest/build_settings.html?highlight=buildable%3Dfalse#external-packages for more details."""

    homepage = "https://developer.arm.com/tools-and-software/server-and-hpc/downloads/arm-performance-libraries"
    url = "https://developer.arm.com/tools-and-software/server-and-hpc/downloads/arm-performance-libraries"
    
    version("20.2.0")
    version("20.1.0")
    version("20.0.0")

    variant('sve',default=False, description='Include SVE optimized instructions')
    variant(
        'march',
        default=' ',
        description='Overide native cpu and specify -march flag',
        values=(' ','armv8-a','armv8.1-a','armv8.2-a','armv8.3-a','armv8.4-a'),
        multi=False
    )
    variant('ilp64',default=False, description='use ilp64 specific Armpl library')
    variant('lp64',default=False, description='use  lp64 specific Armpl library')
    variant('int64',default=False, description='use int64 specific Armpl library')
    variant('mp', default=False, description='use OpenMp specific Armpl library')
    variant("shared", default=True, description="enable shared libs")

    provides("blas")
    provides("lapack")
    provides("scalapack")
    provides("fftw-api@3")

    @property
    def blas_libs(self):
        shared = True if "+shared" in self.spec else False
        if "+ilp64" in self.spec and "+mp" in self.spec:
            libname = "libarmpl_ilp64_mp"
        elif  "+ilp64" in self.spec:
            libname = "libarmpl_ilp64"
        elif "+int64" in self.spec and "+mp" in self.spec:
            libname = "libarmpl_int64_mp"
        elif  "+int64" in self.spec:
            libname = "libarmpl_int64"
        elif "+lp64" in self.spec and "+mp" in self.spec:
            libname = "libarmpl_lp64_mp"
        elif  "+ilp64" in self.spec:
            libname = "libarmpl_lp64"
        elif "+mp" in self.spec:
            libname = "libarmpl_mp"
        else:
            libname ="libarmpl"

        return find_libraries(
            libname,
            root=self.prefix,
            shared=shared,
            recursive=False)

    @property
    def lapack_libs(self):
        return self.blas_libs

    @property
    def scalapack_libs(self):
        return self.blas_libs

    @property
    def fftw_libs(self):
        return self.blas_libs

    
    def flag_handler(self, name, flags):
        if name in ['cflags', 'cxxflags', 'cppflags', 'ldflags'] and arm==spec.compiler.name and self.march!=' ':
            flags.append('-march={0} -armpl',self.march)
            return (None, flags, None)
        elif name in ['cflags', 'cxxflags', 'cppflags', 'ldflags'] and arm==spec.compiler.name:
            flags.append('-mcpu=native -armpl')
            return (None, flags, None)
        elif name in ['cflags', 'cxxflags', 'cppflags'] and gcc==spec.compiler.name and self.march!=' ':
            flags.append('-march={0}', self.march)
            return (None, flags, None)
        elif name in ['ldflags'] and gcc==spec.compiler.name:
            flags.append('-lgfortran')
            return (None, flags, None)
        return (flags, None, None)



