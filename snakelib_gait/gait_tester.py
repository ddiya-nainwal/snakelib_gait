import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

from .gaits import compound_serpenoid
from .gaits import helix
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

    def __init__(self, gait, params):
        super().__init__('minimal_publisher')
        self.gait = gait
        self.params = params
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
        self.transition = 0.0

    def timer_callback(self):
        if self.joint_msg is None:
            return
        msg = self.joint_msg
        msg.velocity = [0] * len(msg.velocity)
        msg.effort = [0] * len(msg.effort)
        n_modules = len(msg.name)
        msg.position = flip_axes(self.gait(
            self.gait_phase,
            n_modules,
            **self.params
        )) * self.transition + np.multiply(msg.position, 1.0 - self.transition)
        print(msg)
        self.publisher_.publish(msg)
        self.gait_phase = (self.timer_period + self.gait_phase)
        self.transition = min(self.timer_period + self.transition, 1.0)

    def feedback_cb(self, msg):
        self.joint_msg = msg


def main(args=None):
    import argparse
    rclpy.init(args=args)

    gaits = {
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
        'sidewind': (sidewind, {
            'amplitude_h': 0.49,
            'amplitude_v': 0.38,
            'spatial_frequency': 0.08,
            'time_frequency': 5/9,
        }),
    }

    # Initialize the parser
    parser = argparse.ArgumentParser(description='Gait tester node')
    parser.add_argument(
        'gait',
        type=str,
        choices=list(gaits.keys()),
        help='Gait name.'
    )

    # Collects all remaining positional arguments into a list
    parser.add_argument('extra_inputs', nargs='*', help='Any extra positional arguments')

    # Parse and use the arguments
    args = parser.parse_args()

    minimal_publisher = GaitTester(gaits[args.gait][0], gaits[args.gait][1])
    # minimal_publisher = GaitTester(helix, helix_params)

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
