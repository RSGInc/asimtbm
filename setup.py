from setuptools import setup, find_packages
setup(
    name="asimtbm",
    version='0.1',
    description='Trip-based destination choice model',
    author='contributing authors',
    author_email='blake.rosenthal@rsginc.com',
    license='BSD-3',
    url='https://github.com/RSGInc/asimtbm',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Programming Language :: Python :: 3 :: Only',
    ],
    packages=find_packages(exclude=['*.tests']),
    include_package_data=True,
    python_requires=">=3.5.3",
    install_requires=[
        'numpy >= 1.16.1',
        'openmatrix >= 0.3.4.1',
        'pandas >= 0.24.1',
        # 'pyyaml >= 5.1',
        # 'tables >= 3.5.1',
        'activitysim >= 0.9.1',
    ]
)
