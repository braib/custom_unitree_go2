# Copyright (c) 2022-2026, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

# test_custom_unitree_go2.py

import argparse

from isaaclab.app import AppLauncher

# add argparse arguments
parser = argparse.ArgumentParser(
    description="This script demonstrates adding a custom robot to an Isaac Lab environment."
)
parser.add_argument("--num_envs", type=int, default=1, help="Number of environments to spawn.")
# append AppLauncher cli args
AppLauncher.add_app_launcher_args(parser)
# parse the arguments
args_cli = parser.parse_args()

# launch omniverse app
app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app


"""
Unitree Go2 robot configuration — built from our own USD file.

Joint layout (12 actuated DOF):
    FL_hip_joint   FR_hip_joint   RL_hip_joint   RR_hip_joint     (abduction)
    FL_thigh_joint FR_thigh_joint RL_thigh_joint RR_thigh_joint   (hip pitch)
    FL_calf_joint  FR_calf_joint  RL_calf_joint  RR_calf_joint    (knee)
"""

import numpy as np
import torch

import isaaclab.sim as sim_utils
from isaaclab.assets import AssetBaseCfg
from isaaclab.actuators import DCMotorCfg
from isaaclab.utils.assets import ISAACLAB_NUCLEUS_DIR
from isaaclab.assets.articulation import ArticulationCfg
# from isaaclab.sim.spawners.materials import PreviewSurfaceCfg
from isaaclab.scene import InteractiveScene, InteractiveSceneCfg


# Path to our own USD file
# CUSTOM_UNITREE_GO2_USD_PATH = "/home/multi-robot/learn_isaac/src/custom_unitree_go2/source/custom_unitree_go2/custom_unitree_go2/robots/usd/go2_descrizption.usd"
CUSTOM_UNITREE_GO2_USD_PATH = "/home/multi-robot/learn_isaac/src/custom_unitree_go2/source/custom_unitree_go2/custom_unitree_go2/robots/usd/go2_description1.usd"
# CUSTOM_UNITREE_GO2_USD_PATH = "/home/multi-robot/learn_isaac/src/custom_unitree_go2/source/custom_unitree_go2/custom_unitree_go2/robots/usd/go2.usd"
# CUSTOM_UNITREE_GO2_USD_PATH = f"{ISAACLAB_NUCLEUS_DIR}/Robots/Unitree/Go2/go2.usd"
 

CUSTOM_UNITREE_GO2_CFG = ArticulationCfg(
    # prim_path = "{ENV_REGEX_NS}/Robot",  # Do not add in the robot config add it in the env config
    spawn = sim_utils.UsdFileCfg(
        usd_path                       = CUSTOM_UNITREE_GO2_USD_PATH,
        visible                        = True, # default True
        copy_from_source               = True, # default True
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
        collision_props                = sim_utils.CollisionPropertiesCfg( # Not necessary if the collision is good in robot USD / URDF
            collision_enabled          = True,
            contact_offset             = 0.001,
            rest_offset                = 0.0,
            torsional_patch_radius     = 0.0,
            min_torsional_patch_radius = 0.05
        ),
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
    articulation_root_prim_path = None, # None = Isaac Lab finds it automatically or when it has one robot | When TO add it: your USD has multiple robots
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
            ".*_hip_joint"   : 0.0,    # neutral, feet directly below hips — within [-1.047, 1.047] ✓
            ".*_thigh_joint" : 0.9,    # thigh tilted forward for standing height — within [-1.571, 3.491] ✓
            ".*_calf_joint"  : -1.8,   # knee bent to hold body weight — within [-2.723, -0.838] ✓
        },
        # joint_vel = {
        #     ".*": 0.0
        # },
        pos = (0.0, 0.0, 0.35),
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
            # effort_limit_sim   = None,
            # velocity_limit_sim = None,
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
            # effort_limit_sim   = None,
            # velocity_limit_sim = None,
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
            # effort_limit_sim   = None,
            # velocity_limit_sim = None,
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



class CustomUnitreeSceneCfg(InteractiveSceneCfg):

    # Ground Plane
    ground = AssetBaseCfg(
        prim_path = "/World/defaultGroundPlane",
        spawn = sim_utils.GroundPlaneCfg()
    )

    # Light
    light = AssetBaseCfg(
        prim_path = "/World/Light",
        spawn = sim_utils.DomeLightCfg(intensity = 3000.0, color = (0.75, 0.75, 0.75))
    )

    custom_unitree_go2 = CUSTOM_UNITREE_GO2_CFG.replace(
        prim_path = "{ENV_REGEX_NS}/custom_unitree_go2"
    )

def run_simulation(sim: sim_utils.SimulationContext, scene: InteractiveScene):
    sim_dt = sim.get_physics_dt()
    sim_time = 0.0
    count = 0

    print("Body names:", scene["custom_unitree_go2"].data.body_names)
    print("Joint names:", scene["custom_unitree_go2"].data.joint_names)

    while simulation_app.is_running():
        # reset every 500 steps
        if count % 500 == 0:
            count = 0

            # reset root state
            root_state = scene["custom_unitree_go2"].data.default_root_state.clone()
            root_state[:, :3] += scene.env_origins

            scene["custom_unitree_go2"].write_root_pose_to_sim(root_state[:, :7])
            scene["custom_unitree_go2"].write_root_velocity_to_sim(root_state[:, 7:])

            # reset joint state
            joint_pos = scene["custom_unitree_go2"].data.default_joint_pos.clone()
            joint_vel = scene["custom_unitree_go2"].data.default_joint_vel.clone()
            scene["custom_unitree_go2"].write_joint_state_to_sim(joint_pos, joint_vel)

            scene.reset()
            print("[INFO]: Resetting Go2 state...")

        # simple trot — move all legs with a sine wave on thigh joints
        joint_pos_target = scene["custom_unitree_go2"].data.default_joint_pos.clone()

        ''' The walking is not good if possible fix it'''

        # trot gait — diagonal pairs in phase, opposite pairs 180° out
        phase_FL_RR = 2 * np.pi * 0.5 * sim_time          # FL and RR together
        phase_FR_RL = 2 * np.pi * 0.5 * sim_time + np.pi  # FR and RL opposite

        # thigh joints
        joint_pos_target[:, 4] = 0.9 + 0.4 * np.sin(phase_FL_RR)  # FL_thigh
        joint_pos_target[:, 5] = 0.9 + 0.4 * np.sin(phase_FR_RL)  # FR_thigh
        joint_pos_target[:, 6] = 0.9 + 0.4 * np.sin(phase_FR_RL)  # RL_thigh
        joint_pos_target[:, 7] = 0.9 + 0.4 * np.sin(phase_FL_RR)  # RR_thigh

        # calf joints — bend more when swinging forward, less when pushing back
        joint_pos_target[:, 8]  = -1.8 + 0.3 * np.sin(phase_FL_RR)  # FL_calf
        joint_pos_target[:, 9]  = -1.8 + 0.3 * np.sin(phase_FR_RL)  # FR_calf
        joint_pos_target[:, 10] = -1.8 + 0.3 * np.sin(phase_FR_RL)  # RL_calf
        joint_pos_target[:, 11] = -1.8 + 0.3 * np.sin(phase_FL_RR)  # RR_calf
        
        ''' The above is the walking action angles fix them ... '''

        scene["custom_unitree_go2"].set_joint_position_target(joint_pos_target)

        scene.write_data_to_sim()
        sim.step()
        sim_time += sim_dt
        count += 1
        scene.update(sim_dt)



def main():
    
    sim_cfg = sim_utils.SimulationCfg(device = args_cli.device)
    sim = sim_utils.SimulationContext(sim_cfg)

    sim.set_camera_view([3.5, 0.0, 3.2], [0.0, 0.0, 0.5])

    # DEsign Scene
    scene_cfg = CustomUnitreeSceneCfg(args_cli.num_envs, env_spacing = 2.0)
    scene = InteractiveScene(scene_cfg)

    sim.reset()

    print("Setup Complete ...")

    run_simulation(sim, scene)



if __name__ == "__main__":
    main()
    simulation_app.close()