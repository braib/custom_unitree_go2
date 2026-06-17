# Copyright (c) 2022-2025, The Isaac Lab Project Developers.
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# custom_unitree_go2.py
"""
Unitree Go2 robot configuration — built from our own USD file.

Joint layout (12 actuated DOF):
    FL_hip_joint   FR_hip_joint   RL_hip_joint   RR_hip_joint     (abduction)
    FL_thigh_joint FR_thigh_joint RL_thigh_joint RR_thigh_joint   (hip pitch)
    FL_calf_joint  FR_calf_joint  RL_calf_joint  RR_calf_joint    (knee)
"""


import isaaclab.sim as sim_utils
from isaaclab.actuators import DCMotorCfg
from isaaclab.utils.assets import ISAACLAB_NUCLEUS_DIR
from isaaclab.assets.articulation import ArticulationCfg
# from isaaclab.sim.spawners.materials import PreviewSurfaceCfg


# Path to our own USD file
CUSTOM_UNITREE_GO2_USD_PATH = "/home/multi-robot/learn_isaac/src/custom_unitree_go2/source/custom_unitree_go2/custom_unitree_go2/robots/usd/go2_description.usd"
# CUSTOM_UNITREE_GO2_USD_PATH = "/home/multi-robot/learn_isaac/src/custom_unitree_go2/source/custom_unitree_go2/custom_unitree_go2/robots/usd/go2_description1.usd"
# CUSTOM_UNITREE_GO2_USD_PATH = "/home/multi-robot/learn_isaac/src/custom_unitree_go2/source/custom_unitree_go2/custom_unitree_go2/robots/usd/go2.usd"
# CUSTOM_UNITREE_GO2_USD_PATH = f"{ISAACLAB_NUCLEUS_DIR}/Robots/Unitree/Go2/go2.usd"


CUSTOM_UNITREE_GO2_CFG = ArticulationCfg(
    # prim_path = "{ENV_REGEX_NS}/Robot",  # Do not add in the robot config add it in the env config
    spawn = sim_utils.UsdFileCfg(
        usd_path                       = CUSTOM_UNITREE_GO2_USD_PATH,
        # visible                        = True, # default True
        # copy_from_source               = True, # default True
        rigid_props                    = sim_utils.RigidBodyPropertiesCfg(
            disable_gravity                 = False, # No default value must be False
            linear_damping                  = 0.0,
            angular_damping                 = 0.0,
            max_linear_velocity             = 1000.0,
            max_angular_velocity            = 1000.0,
            max_depenetration_velocity      = 1.0,
            retain_accelerations            = False,
            solver_position_iteration_count = 8,
            solver_velocity_iteration_count = 0,
        ),
        # collision_props                = sim_utils.CollisionPropertiesCfg( # Not necessary if the collision is good in robot USD / URDF
        #     collision_enabled          = True,
        #     contact_offset             = 0.001,
        #     rest_offset                = 0.0,
        #     torsional_patch_radius     = 0.0,
        #     min_torsional_patch_radius = 0.05
        # ),
        activate_contact_sensors       = True,             # default False
        # scale                          = (1.0, 1.0, 1.0),  # Use it when the robot's scale is not correct , here the original USD / URDF is correct hence 1.0 for all. If the value is 1.0 it is need not be used
        articulation_props             = sim_utils.ArticulationRootPropertiesCfg( # Always set when it is a robot
            articulation_enabled            = True,   # True When its a robot that needs to be controlled or moved
            enabled_self_collisions         = False,  # Quadruped/biped locomotion training. Self-collision checks are expensive and rarely affect the outcome. Leaving it on can also cause false contact detections between neighbouring links that naturally overlap in the USD mesh. # Must set True: Tasks where self-contact is physically critical — a humanoid catching itself, a hand grasping its own fingers
            solver_position_iteration_count = 8,      # Keep low (4): Standard quadruped/biped locomotion. 4 is the sweet spot — stable enough, fast enough for large-scale RL training.
            solver_velocity_iteration_count = 0,      # Keep at 0: Most locomotion tasks
            # sleep_threshold                 = 0.005,   # standard, robot stays awake during training  # No need
            # stabilization_threshold         = 0.001  # Must set only when a target (eg. Manipulator) needs to hold its position , for robot dog can ignore (Only add when the robot dog has to tand still)
            fix_root_link                   = False   # True for Fixed-base manipulators
        ),
        # fixed_tendons_props            = sim_utils.FixedTendonPropertiesCfg(  # Only needed when one actuator controlls more than one joint here it is not needed
        #     tendon_enabled  = False,                                          # one actuator, many joints, fixed relation
        #     stiffness       = 0.0,
        #     damping         = 0.0,
        #     limit_stiffness = 0.0,
        #     offset          = 0.0,
        #     rest_length     = 0.0,
        # ),
        # spatial_tendons_props          = sim_utils.SpatialTendonPropertiesCfg(  # actual cable path in 3D
        #     tendon_enabled = False,
        #     stiffness = 0.0,
        #     damping         = 0.0,
        #     offset          = 0.0,
        #     limit_stiffness = 0.0,
        # ),
        # joint_drive_props = sim_utils.JointDrivePropertiesCfg( # Use it when you want a quick global setting for many joints and all joints can reasonably share similar behavior. # Do not use it when different joints need different values.
        #     drive_type   = "force", # or acceleration
        #     max_effort   = 0.0,
        #     max_velocity = 0.0,
        #     stiffness    = 0.0,
        #     damping      = 0.0
        # ),
        # visual_material_path = "/path/../../.",
        # visual_material = PreviewSurfaceCfg(
        #     diffuse_color = (0.0, 0.0, 0.0),
        #     emissive_color = (0.0, 0.0, 0.0),
        #     roughness = 0.0,
        #     metallic = 0.0,
        #     opacity = 0.0,
        # ),
    ),
    # collision_group = 0, # default 0 | -1: global collision group (collides with all assets in the scene). | 0: local collision group (collides with other assets in the same environment).
    # debug_vis=True,   # default False | It shows (visually) the data in isaacsim gui
    # articulation_root_prim_path = None, # None = Isaac Lab finds it automatically or when it has one robot | When TO add it: your USD has multiple robots
    # example.usd
    # ├── /robot1    ← ArticulationRootAPI here  (go2)
    # └── /robot2    ← ArticulationRootAPI here  (spot)
    # articulation_root_prim_path="/robot2"
    init_state = ArticulationCfg.InitialStateCfg(
        # lin_vel = (0.0, 0.0, 0.0),
        # ang_vel = (0.0, 0.0, 0.0),
        # joint_pos = {
        #    ".*": 0.0,  # represents all joints
        # },
        joint_pos = {
            ".*_hip_joint"   : 0.15,   # neutral, feet directly below hips — within [-1.047, 1.047] ✓
            ".*_thigh_joint" : 0.0,    # thigh tilted forward for standing height — within [-1.571, 3.491] ✓
            ".*_calf_joint"  : -0.9,   # knee bent to hold body weight — within [-2.723, -0.838] ✓
        },
        # joint_vel = {
        #     ".*": 0.0
        # },
        pos = (0.0, 0.0, 0.4),
        # rot = (1.0, 0.0, 0.0, 0.0) # Quaternion rotation (w, x, y, z) of the root in simulation world frame. Defaults to (1.0, 0.0, 0.0, 0.0). # If your robot's USD "forward" direction doesn't match your task's expected forward direction, rotate here instead of editing the USD.
    ),
    soft_joint_pos_limit_factor = 0.9, # default 1.0
    actuators = {
        "hip_joints"   : DCMotorCfg(
            saturation_effort   = 45.43,
            joint_names_expr    = [".*_hip_joint"],
            # effort_limit      = {
            #     ".*_hip_joint": 23.7
            # },
            effort_limit         = 23.7, # If none taken from usd
            velocity_limit       = 30.1,
            effort_limit_sim     = 23.7,
            velocity_limit_sim   = 30.1,
            stiffness            = 25.0,
            damping              = 0.5,
            armature             = 0.001, # go till 0.0049
            friction             = 0.01,
            dynamic_friction     = 0.005,   # half of static friction
            # viscous_friction     = 0.005,

        ),
        "thigh_joints" : DCMotorCfg(
            saturation_effort    = 45.43,
            joint_names_expr     = [".*_thigh_joint"],
            # effort_limit       = {
            #     ".*_thigh_joint": 23.7
            # },
            effort_limit         = 23.7, # If none taken from usd
            velocity_limit       = 30.1,
            effort_limit_sim     = 23.7,
            velocity_limit_sim   = 30.1,
            stiffness            = 25.0,
            damping              = 0.5,
            armature             = 0.001, # go till 0.0049
            friction             = 0.01,
            dynamic_friction     = 0.005,   # half of static friction
            # viscous_friction     = 0.005,

        ),
        "calf_joint"   : DCMotorCfg(
            saturation_effort    = 45.43,
            joint_names_expr     = [".*_calf_joint"],
            # effort_limit       = {
            #     ".*_calf_joint": 45.43
            # },
            effort_limit         = 45.43, # If none taken from usd
            velocity_limit       = 15.7,
            effort_limit_sim     = 45.43,
            velocity_limit_sim   = 15.7,
            stiffness            = 50.0,
            damping              = 1.0,
            armature             = 0.001, # go till 0.0049
            friction             = 0.01,
            dynamic_friction     = 0.005,   # half of static friction
            # viscous_friction     = 0.005,

        ),
    },
    actuator_value_resolution_debug_print = True  # default false | if the value are different in USD and config then Isaac Lab resolves the conflict silently. This flag makes it print exactly what value was used and why.

)



UNITREE_GO2_CFG = ArticulationCfg(
    spawn=sim_utils.UsdFileCfg(
        # usd_path=f"{ISAACLAB_NUCLEUS_DIR}/Robots/Unitree/Go2/go2.usd",
        usd_path = CUSTOM_UNITREE_GO2_USD_PATH,
        activate_contact_sensors=True,
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            disable_gravity=False,
            retain_accelerations=False,
            linear_damping=0.0,
            angular_damping=0.0,
            max_linear_velocity=1000.0,
            max_angular_velocity=1000.0,
            max_depenetration_velocity=1.0,
        ),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            enabled_self_collisions=False, solver_position_iteration_count=4, solver_velocity_iteration_count=0
        ),
    ),
    init_state=ArticulationCfg.InitialStateCfg(
        pos=(0.0, 0.0, 0.4),
        joint_pos={
            ".*L_hip_joint": 0.1,
            ".*R_hip_joint": -0.1,
            "F[L,R]_thigh_joint": 0.8,
            "R[L,R]_thigh_joint": 1.0,
            ".*_calf_joint": -1.5,
        },
        joint_vel={".*": 0.0},
    ),
    soft_joint_pos_limit_factor=0.9,
    actuators={
        "base_legs": DCMotorCfg(
            joint_names_expr=[".*_hip_joint", ".*_thigh_joint", ".*_calf_joint"],
            effort_limit=23.5,
            saturation_effort=23.5,
            velocity_limit=30.0,
            stiffness=25.0,
            damping=0.5,
            friction=0.0,
        ),
    },
)