from distutils.core import setup
from Cython.Build import cythonize

setup(name = "Anomaly_Speed",
      version = "0.3",
      license= "MIT",
      description = "Detect anomaly cars in a given video and calculate speed for each car.",
      author = "Aijin Wang",
      author_emial = "aijinw@andrew.cmu.edu",
      maintainer = "aijinw@andrew.cmu.edu",
      classifiers = ["License :: OSI Approved :: MIT License",
                     "Topic :: Scientific/Engineering :: Machine Learning",
                     "Programming Language :: Python :: 3.7",
                     "Programming Language :: Cython"],
      keywords = ["Isolation Forest"],
      packages=["Anomaly_Code"],
      ext_modules = cythonize("anomaly_treec.pyx")
)

# python3 setup.py build_ext --inplace

# import pyximport; pyximport.install()
# import anomaly_tree
