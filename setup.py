import setuptools

with open("README.md") as f:
    ldesc = f.read()

setuptools.setup(
    name="rpc42b2t2",
    version="1.0.0",
    author_email="korochun@list.ru",
    description="An improved Discord RPC for 2b2t.org",
    long_description=ldesc,
    long_description_content_type="text/markdown",
    url="https://github.com/korochun/rpc42b2t",
    author="korochun",
    license="GPLv3",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.5",
        "Topic :: Communications :: Chat",
        "Topic :: Games/Entertainment",
    ],
    keywords="Minecraft RPC Discord",
    packages=setuptools.find_packages(),
    install_requires=["pypresence>=4.0.0"],
    python_requires=">=3.5",
    entry_points={"console_scripts": ["rpc42b2t=rpc42b2t:main"]},
)
