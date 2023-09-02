import setuptools

with open('README.md', 'r', encoding='utf-8') as fn:
    long_description = fn.read()

setuptools.setup(
    name='claude_api',
    version='1.0.0',
    author='Duck Dev',
    description='Free Claude AI API.',
    keywords='claude, llm, ai, api',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/duck-web-dev/claude_api',
    project_urls={
        'Documentation': 'https://github.com/duck-web-dev/claude_api',
        'Bug Reports':   'https://github.com/duck-web-dev/claude_api/issues',
        'Source Code':   'https://github.com/duck-web-dev/claude_api',
        # 'Funding': '',
        # 'Say Thanks!': '',
    },
    packages=setuptools.find_packages(),
    install_requires=['curl_cffi'],
)