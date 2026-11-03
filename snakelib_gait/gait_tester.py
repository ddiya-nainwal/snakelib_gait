import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

from .gaits import compound_serpenoid
from .gaits import helix
from .gaits import helix_auto
from .gaits import sidewind


def flip_axes(target_angles: np.ndarray):
    """Flips joint angles to reflect the real snake.

    The direction of the target angles has to flip signs after every pair of
    actuators, since the rotation axes of subsequent even or odd joints
    is flipped as the robot is assembled.
    """
    flip_pattern = [1, 1, -1, -1]
    N = len(target_angles)
    full_pattern = np.tile(flip_pattern, int(np.ceil(N / 4)))[:N]
    return target_angles * full_pattern


class GaitTester(Node):

    def __init__(self):
        super().__init__('gait_tester')
        # Set up parameters
        self.declare_parameter('gait_name', 'sidewind')
        self.declare_parameter('gait_speed', 1.0)
        self.gaits = {
            'compound_serpenoid': (compound_serpenoid, {
                'offsets': [0.1, 0.1],
                'amplitudes': [0.2, 0.2],
                'spatial_frequencies': [0.02, 0.02],
                'time_frequencies': [2 ** 0.5, 0.25],
                'phase_shift': 0.25,
            }),
            'helix': (helix, {
                'amplitude': 1,
                'spatial_frequency': 0.01,
                'time_frequency': 0.25,
            }),
            'helix_auto': (helix_auto, {
                'tightness': 0.6,
                'pole_side': 0,
                'time_frequency': 0.25,
            }),
            'sidewind': (sidewind, {
                'amplitude_h': 0.49,
                'amplitude_v': 0.38,
                'spatial_frequency': 0.08,
                'time_frequency': 5/9,
            }),
        }

        for gait_name, (_, parameters) in self.gaits.items():
            for param, value in parameters.items():
                self.declare_parameter(f"{gait_name}.{param}", value)

        self.subscriber_ = self.create_subscription(
            JointState,
            '/snake/joint_states',
            self.feedback_cb,
            10
        )
        self.joint_msg = None
        self.publisher_ = self.create_publisher(JointState, '/snake/joint_commands', 100)
        self.timer_period = 1.0 / 100.0  # seconds
        self.timer = self.create_timer(self.timer_period, self.timer_callback)
        self.gait_phase = 0.0
        self.transition = 1

    def timer_callback(self):
        if self.joint_msg is None:
            return
        gait_name = self.get_parameter('gait_name').get_parameter_value().string_value
        gait_speed = self.get_parameter('gait_speed').get_parameter_value().double_value
        if not gait_name:
            return
        msg = self.joint_msg
        msg.velocity = [0] * len(msg.velocity)
        msg.effort = [0] * len(msg.effort)
        n_modules = len(msg.name)
        params = {}
        for key in self.gaits[gait_name][1].keys():
            params[key] = self.get_parameter(f'{gait_name}.{key}').value
        msg.position = flip_axes(self.gaits[gait_name][0](
            self.gait_phase,
            n_modules,
            **params
        )) * self.transition + np.multiply(msg.position, 1.0 - self.transition)
        print(msg)
        self.publisher_.publish(msg)
        self.gait_phase = (self.timer_period * gait_speed + self.gait_phase)
        # self.transition = min(self.timer_period * gait_speed + self.transition, 1.0)

    def feedback_cb(self, msg):
        self.joint_msg = msg


def main(args=None):
    rclpy.init(args=args)
    gait_tester = GaitTester()
    rclpy.spin(gait_tester)
    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    gait_tester.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
