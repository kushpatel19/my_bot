import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node



def generate_launch_description():


    # Include the robot_state_publisher launch file, provided by my own package. Force sim time to be enabled

    package_name='my_bot'
    package_dir = get_package_share_directory(package_name)

    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','rsp.launch.py'
                )]), launch_arguments={'use_sim_time': 'true'}.items()
    )

    #Rviz configuration file path
    rviz = os.path.join(package_dir,'config' , 'drive_bot.rviz')
    
    node_rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz],
        output='screen'
    )

    # Include the Gazebo launch file, provided by the gazebo_ros package
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
             )


    # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'my_bot'],
                        output='screen')

    # Launch them all!
    return LaunchDescription([
        rsp,
        node_rviz,
        DeclareLaunchArgument(
        'world',
        default_value=[os.path.join(package_dir, 'worlds','obstacles.world'), ''],
        description='SDF world file'),
        gazebo,
        spawn_entity,
    ])