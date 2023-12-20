from setuptools import setup, find_packages

setup(
    name="warp_core",
    packages=find_packages(),
    description="Modular Extensible Training Framework",
    version="0.0.1",
    url="https://github.com/WARP-AI/WarpCore",
    author="Pablo Pernías",
    author_email="pablo@pernias.com",
    keywords=["pip", "pytorch", "tools", "training", "diffusion", "generative", "models"],
    zip_safe=False,
    install_requires=[
        "torch>=1.6",
        "numpy>=1.0",
        "wandb>=0.15.0",
        "safetensors>=0.4.0",
        "gdf @ git+https://github.com/WARP-AI/gdf",
        "munch>=4.0.0",
        "webdataset>=0.2.79"
    ],
    package_data={},
    include_package_data=True,
    entry_points = {
        'console_scripts': ['warp_core=warp_core.scripts.cli:main'],
    }
)
