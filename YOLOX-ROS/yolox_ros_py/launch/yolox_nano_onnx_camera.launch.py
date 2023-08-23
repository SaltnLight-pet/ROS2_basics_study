import launch
import launch_ros.actions
from launch.actions import DeclareLaunchArgument
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

from urllib.request import urlretrieve
import os

def generate_launch_description():
    yolox_ros_share_dir = get_package_share_directory('yolox_ros_py')

    video_device = LaunchConfiguration('video_device', default='/dev/video0')
    video_device_arg = DeclareLaunchArgument(
        'video_device',
        default_value='/dev/video0',
        description='Video device'
    )

    webcam = launch_ros.actions.Node(
        package="v4l2_camera", executable="v4l2_camera_node",
        parameters=[
            {"image_size": [640,480]},
            {"video_device": video_device},
        ],
    )
    yolox_onnx = launch_ros.actions.Node(
        package="yolox_ros_py", executable="yolox_onnx",output="screen",
        parameters=[
            {"input_shape/width": 416},
            {"input_shape/height": 416},

            {"with_p6" : False},
            {"model_path" : yolox_ros_share_dir+"/yolox_nano.onnx"},
            {"conf" : 0.3},
        ],
    )

    rqt_graph = launch_ros.actions.Node(
        package="rqt_graph", executable="rqt_graph",
    )

    return launch.LaunchDescription([
        video_device_arg,
        webcam,
        yolox_onnx,
        # rqt_graph
    ])