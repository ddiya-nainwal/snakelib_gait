# Snake gait library

This package contains snake gaits and tools to work with them.

## Gaits supported

### General

* [ ] **Compound serpenoid** - Provides a common interface to the basic gait model,
  a serpenoid curve (sinusoidal curvature) on each axis.
* [ ] **Straight** - Sets all joint angles to zero

### Floor gaits

* [ ] **Bent** - This gait does not move, but provides a stable shape that can be used
  as a "default" shape that looks more "snake-like" than a straight shape. 
  It also provides a stable base from which to lift the head up.
* [ ] **Linear progression** - Gait for moving straight forward that uses a gentle s
  shape horizontally to stop the snake from rolling over while passing a wave
  down the backbone like an inchworm.
* [ ] **Roll** - This gait forms the snake into a constant arc, and rotates this arc
  about the longitudinal axis of the snake, causing the snake to translate
  laterally across the ground.
* [ ] **Sidewind** - Sidewinding is a fast, efficient motion that moves the robot
  laterally inspired by biological sidewinders.
* [ ] **Conical sidewind** - generalizes the basic sidewinding gait and enables the
  robot to turn.
* [ ] **Slither** - This gait moves the snake forward by creating a wave on both the
  vertical and lateral axis.  The snake contacts the ground on the extreme
  lateral modules, which are used to push the snake forward.  The wave is
  tapered to result in a head position which is fairly stable, and a tail
  position which undulates with the highest amplitude.
* [ ] **Spin** - Combines two sidewinding gaits to quickly spin the robot in a circle.
* [ ] **Stairs** - A serpenoid-based stair climbing gait
* [ ] **K stair** - A non-serpenoid stair climbing gait that allows you to climb
  up stairs at regular intervals.

### Pole gaits
* [ ] **Helix** - A helical gait that allows the snake to roll inside and outside poles.
* [ ] **Helix auto** - A helical gait that intelligently combines pitch and diameter.
* [ ] **Spiraling** - Passes a wave through a helical gait that increase the radius
  of the helix in that window, producing an inchworming gait that rotates the
  snake around the pipe axis.
* [ ] **Windowed rolling helix** - Allows a snake to traverse T-shaped junctions
  by making two independent rolling helixes and transitioning between them

### Other
* [ ] **Head look polar** - A head look gait using spherical coordinates.
* [ ] **Tail look polar** - Head look for your tail, useful for untangling the 
  thether and for snakes with tail cameras
* [ ] **Lateral udulation** - pass a sinusoid through the horizontal backbone.
  useful for pushing through rough terrain or swimming.
* [ ] **Roll in shape** - Allows one to 'roll' the shape of the snake along
  the backbone curve