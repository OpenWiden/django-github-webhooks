import setuptools

with open("README.rst", "r") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst", "r") as history_file:
    history = history_file.read()

setuptools.setup(
    name="django-github-webhooks",
    version="0.1.0",
    author="Alexandr Stefanitsky-Mozdor",
    author_email="stefanitsky.mozdor@gmail.com",
    description="Django GitHub webhooks",
    long_description=readme + '\n\n' + history,
    url="https://github.com/OpenWiden/django-github-webhooks",
    packages=["github_webhooks"],
    classifiers=[
        "Framework :: Django :: 2.1",
        "Framework :: Django :: 3.0",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
