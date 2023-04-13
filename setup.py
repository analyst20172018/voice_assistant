from setuptools import setup, find_packages

setup(
    name='voice-assistant',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'google-cloud-texttospeech',
        'numpy',
        'openai',
        'pydub',
        'requests',
        'scipy',
        'sounddevice',
        'winaudio',
	'fire',
    ],
    entry_points={
        'console_scripts': [
            'voice_assistant_pc = voice_assistant_pc:main',
            'voice_assistant_telegram = voice_assistant_telegram:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)