from setuptools import setup
import glob, os

package_name = 'cat'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + 'train/', glob.glob(os.path.join('train', 'model_final.pth')))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='chan',
    maintainer_email='chan@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'camera_publisher = cat.node.camera_publisher:main',
            'camera_subscriber = cat.node.camera_subscriber:main',
            'go = cat.node.go:main'
        ],
    },
)
