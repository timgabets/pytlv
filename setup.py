from setuptools import setup

setup(name='pytlv',
      version='0.69',
      
      description='TLV(tag length lavue) data parser',
      long_description=open('README.md').read(),
      
      classifiers=[
        'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',
        'Operating System :: OS Independent',
        
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        
        'Topic :: Communications',
        'Intended Audience :: Developers',
      ],
      
      keywords='EMV TLV parse',
      
      url='https://github.com/timgabets/pytlv',
      author='Tim Gabets',
      author_email='tim@gabets.ru',
      
      license='LGPLv2',
      packages=['pytlv'],
      install_requires=[],
      zip_safe=True)