from setuptools import setup, find_packages

setup(name='lemsplc',
      packages=find_packages(),
      install_requires=['pyquery',],
      extras_require={
        'dev': ['ipython', 'ipdb',],
        'web': ['flask',]
      },
      python_requires='>=3',
)
      