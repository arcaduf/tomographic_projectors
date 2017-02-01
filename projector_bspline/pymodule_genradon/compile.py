import os
import shutil


if os.path.exists('build'):
    shutil.rmtree('build')

os.remove( 'genradon.c' )

os.system('python create_genradon_module.py build_ext --inplace')
