import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    
    # Path to the xacro file that describes the robot
    xacro_file = PathJoinSubstitution([
        FindPackageShare('questbot_description'),
        'urdf',
        'robot.urdf.xacro'
    ])

    # Path to the RViz configuration file
    rviz_config_file = PathJoinSubstitution([
        FindPackageShare('questbot_description'),
        'rviz',
        'config.rviz'
    ])

    # Robot State Publisher node
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'use_sim_time': True,
            'robot_description': Command([
                'xacro ', xacro_file,
                ' use_gazebo:=false',
                ' use_gzsim:=false',
                ' use_2wd:=true',
            ])
        }]
    )
    
    joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        output='screen',
    )

    # RViz2 node
    rviz2 = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_file]
    )

    return LaunchDescription([
        robot_state_publisher,
        joint_state_publisher,
        rviz2
    ])