import setuptools

with open("README.md", "r") as f:
    description = f.read()

setuptools.setup(
    name="gm2m_relations",
    version="1.0.3",
    author="mojtaba akbari",
    author_email="mojtaba.akbari.221b@gmail.com",
    packages=["gm2m_relations"],
    description="This library implements Django REST Framework serializers to handle generic many to many relations.",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/mojtabaakbari221b/rest-framework-gm2m-relations",
    license='MIT',
    python_requires='>=3.7',
    install_requires=[
        "rest-framework-generic-relations",
    ],
)