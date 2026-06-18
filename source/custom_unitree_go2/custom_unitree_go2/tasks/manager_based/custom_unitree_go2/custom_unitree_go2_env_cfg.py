# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

# custom_unitree_go2_env_cfg.py


import math

import isaaclab.sim as sim_utils
from isaaclab.assets import ArticulationCfg, AssetBaseCfg
from isaaclab.envs import ManagerBasedRLEnvCfg
from isaaclab.managers import CurriculumTermCfg as CurrTerm
from isaaclab.managers import EventTermCfg as EventTerm
from isaaclab.managers import ObservationGroupCfg as ObsGroup
from isaaclab.managers import ObservationTermCfg as ObsTerm
from isaaclab.managers import RewardTermCfg as RewTerm
from isaaclab.managers import SceneEntityCfg
from isaaclab.managers import TerminationTermCfg as DoneTerm
from isaaclab.terrains import TerrainImporterCfg
from isaaclab.scene import InteractiveSceneCfg
from isaaclab.utils import configclass
from isaaclab.sensors import ContactSensorCfg, RayCasterCfg, patterns
from isaaclab.utils.noise import AdditiveUniformNoiseCfg as Unoise
from . import mdp
from isaaclab.utils.assets import ISAAC_NUCLEUS_DIR, ISAACLAB_NUCLEUS_DIR


##
# Pre-defined configs
##

# from isaaclab_assets.robots.cartpole import CARTPOLE_CFG 
from custom_unitree_go2.robots import CUSTOM_UNITREE_GO2_CFG
# from custom_unitree_go2.robots import UNITREE_GO2_CFG as CUSTOM_UNITREE_GO2_CFG
# from isaaclab_assets.robots.unitree import UNITREE_GO2_CFG as CUSTOM_UNITREE_GO2_CFG

from isaaclab.terrains.config.rough import ROUGH_TERRAINS_CFG

##
# Scene definition
##


@configclass
class MySceneCfg(InteractiveSceneCfg):
    """Configuration for a cart-pole scene."""

    # ground plane
    # ground = AssetBaseCfg(
    #     prim_path = "/World/ground",
    #     spawn     = sim_utils.GroundPlaneCfg(size = (100.0, 100.0)),
    # )

    terrain = TerrainImporterCfg(
        collision_group        = -1,
        prim_path              = "/World/ground",
        # num_envs               = 1, # defaults to 1
        terrain_type           = "generator",  # available optiona are ['generator', 'plane', 'usd']
        terrain_generator      = ROUGH_TERRAINS_CFG,  # Only used if terrain_type is set to “generator”.
        usd_path               = None,                # Only used if terrain_type is set to “usd”.
        env_spacing            = None,                # This parameter is used only when the terrain_type is “plane” or “usd” or if use_terrain_origins is False.
        use_terrain_origins    = True,     # defaults to True 
        physics_material       = sim_utils.RigidBodyMaterialCfg(
            friction_combine_mode    = "multiply",
            restitution_combine_mode = "multiply",
            static_friction          = 1.0,
            dynamic_friction         = 1.0,
        ),
        visual_material        = sim_utils.MdlFileCfg(
            mdl_path      = f"{ISAACLAB_NUCLEUS_DIR}/Materials/TilesMarbleSpiderWhiteBrickBondHoned/TilesMarbleSpiderWhiteBrickBondHoned.mdl",
            project_uvw   = True,
            texture_scale = (0.25, 0.25),
        ),
        max_init_terrain_level = 5,
        debug_vis              = False,
    )

    # lights
    # dome_light = AssetBaseCfg(
    #     prim_path = "/World/DomeLight",
    #     spawn     = sim_utils.DomeLightCfg(color = (0.9, 0.9, 0.9), intensity = 500.0),
    # )

    sky_light = AssetBaseCfg(
        prim_path = "/World/skyLight",
        spawn     = sim_utils.DomeLightCfg(
            intensity    = 750.0,
            texture_file = f"{ISAAC_NUCLEUS_DIR}/Materials/Textures/Skies/PolyHaven/kloofendal_43d_clear_puresky_4k.hdr",
        ),
    )

    # robot
    robot: ArticulationCfg = CUSTOM_UNITREE_GO2_CFG.replace(
    # robot: ArticulationCfg = UNITREE_GO2_CFG.replace(
        prim_path = "{ENV_REGEX_NS}/Robot"
    )

    # height_scanner = RayCasterCfg(
    #     mesh_prim_paths = ["/World/ground"],
    #     offset          = RayCasterCfg.OffsetCfg(
    #         pos = (0.0, 0.0, 20.0),      # from go2 eg z = 20.0
    #         rot = (1.0, 0.0, 0.0, 0.0),  # default
    #     ),
    #     # attach_yaw_only = None,     # depricated and will be removed. Please use ray_alignment instead.
    #     prim_path            = "{ENV_REGEX_NS}/Robot/go2_description/base",
    #     # prim_path            = "{ENV_REGEX_NS}/Robot/base",  # UNITREE_GO2_CFG has flat structure, no go2_description
    #     # update_period        = 0.0, # defaults to 0.0 (update evry step)
    #     # history_length       = 0, # defaults to 0 
    #     debug_vis            = True, # defaults to False
    #     ray_alignment        = "yaw", # Default is “base”. |  Literal['base', 'yaw', 'world']
    #     pattern_cfg          = patterns.GridPatternCfg(
    #         resolution = 0.1,
    #         size       = [1.6, 1.0]
    #     ),
    #     # max_distance         = 2.0,  # Defaults to 1e6.  | Maximum distance (in meters) from the sensor to ray cast to
    #     # drift_range          = [],   #  Defaults to (0.0, 0.0).
    #     # ray_cast_drift_range = ,
    #     # visualizer_cfg       = ,
        
    # )

    contact_forces = ContactSensorCfg(
        track_pose                      = False, # default False | we dont need where the foot sensor is in space , we only care if its touching anything or not | we might need it for manipulation to track gripper pose 
        track_contact_points            = False, # default False | records the 3D position of each contact point
        track_friction_forces           = False, # default False | Records Friction force vectors at each contact point
        max_contact_data_count_per_prim = 4, # default 4 | Increase only for contact rich environment (rough terrain)
        prim_path                       = "{ENV_REGEX_NS}/Robot/go2_description/.*", # * which body gets the contact sesor attached
        # prim_path                       = "{ENV_REGEX_NS}/Robot/.*",  # flat structure
        update_period                   = 0.0,     # default 0.0 (for every physics step) | how often sensor data updates in seconds
        history_length                  = 3,       # default 0 | why 3 ncs min 2 is need 1 is buffer  | why not 4 unnecesaty GPU usage
        debug_vis                       = False,   # default False | shows colour markers at contact points
        track_air_time                  = True,    # default False | * It is needed for reward function
        force_threshold                 = 1.0      # default 1.0 | Only change when sensro thinks foot is touching but it isn't

        # filter_prim_paths_expr: list[str] = list(),
        # leave empty default
        # When to use filter_prim_paths_expr:
        # "is hand touching THIS specific cup?"
        # → filter_prim_paths_expr=["{ENV_REGEX_NS}/Cup"]

        # visualizer_cfg: VisualizationMarkersCfg = CONTACT_SENSOR_MARKER_CFG.replace(prim_path="/Visuals/ContactSensor"),
        # Leave at default CONTACT_SENSOR_MARKER_CFG

    )


##
# MDP settings
##

@configclass
class CommandsCfg:
    """Command specifications for the MDP."""
    
    base_velocity = mdp.UniformVelocityCommandCfg(
        asset_name                = "robot",   # in MySceneCfg robot defined variable name
        heading_command           = True, # default False | two ways to command robot direction | False -> rotate at N rad/s | True -> face this direction
        heading_control_stiffness = 0.5,  # do not set when heading_command is False | it is kp value for that helps to reduce the heading direction error
        rel_standing_envs         = 0.02, # 2% of the commands/environments will be to say robot stop and stand still or else robot wont learn to stop
        rel_heading_envs          = 1.0,  # set it only when heading_command is true | keep it default 1.0 | change it only when ang and lin vel must be tracked
        ranges                    = mdp.UniformVelocityCommandCfg.Ranges(
            lin_vel_x = (-1.0, 1.0),
            lin_vel_y = (-1.0, 1.0),
            ang_vel_z = (-1.0, 1.0),
            heading   = (-math.pi, math.pi), # Use only when heading_command is True
        ),
        # goal_vel_visualizer_cfg: VisualizationMarkersCfg = GREEN_ARROW_X_MARKER_CFG.replace(    # appearance of green arrow above robot showing TARGET velocity in GUI
        #     prim_path="/Visuals/Command/velocity_goal"
        # ), # Never touch this not necessary # if needed | from isaaclab.markers import VisualizationMarkersCfg
        # current_vel_visualizer_cfg: VisualizationMarkersCfg = BLUE_ARROW_X_MARKER_CFG.replace( # appearance of blue arrow above robot showing ACTUAL velocity in GUI
        #     prim_path="/Visuals/Command/velocity_current"
        # ),
        resampling_time_range     = (10.0, 10.0),  # default 10 seconds |  how often a new random command is picked
        debug_vis                 =  True # Defaults to False |  shows velocity arrows above robots in GUI
    )


@configclass
class ActionsCfg:
    """Action specifications for the MDP."""

    joint_pos = mdp.JointPositionActionCfg(
        use_default_offset = True,    # default True | When True, Isaac Lab reads the init_state.joint_pos values from your ArticulationCfg and uses them as the zero-point of the action. 
        asset_name        = 'robot',  # robot vairable name in InteractiveSceneCfg
        # debug_vis         = True,    # default False |
        # clip              = {                   # Skip when u have soft_joint_pos_limit_factor in robot_config
        #     ".*_hip_joint"   : (-0.5, 0.5),     # Maximum angle the action can command ig
        #     ".*_thigh_joint" : (-0.8, 0.8), 
        #     ".*_calf_joint"  : (-0.8, 0.8),
        # },
        # joint_names       = [".*_hip_joint", ".*_thigh_joint", ".*_calf_joint"], # MUST | can also write [".*"]
        joint_names       = [".*"],
        scale             = 0.5,   # default 1.0   | can also be dictionary
        # offset            = 0.0,   # default 0.0   | can also be dictionary | Since use_default_offset=True, Isaac Lab ignores whatever you write here
        # preserve_order    = False  # default False |  Only set True if you are building a custom action tensor by hand with a specific assumed joint ordering,
    )


# @configclass
# class ObservationsCfg:
#     """Observation specifications for the MDP."""

#     @configclass
#     class PolicyCfg(ObsGroup):
#         """Observations for policy group."""


#         def __post_init__(self) -> None:
#             pass

#     @configclass
#     class CriticCfg(ObsGroup):
#         """Observations for critic group."""


#         def __post_init__(self) -> None:
#             pass

#     # observation groups
#     policy: PolicyCfg = PolicyCfg()
#     critic: CriticCfg = CriticCfg()



@configclass
class ObservationsCfg:
    """Observation specifications for the MDP."""

    @configclass
    class PolicyCfg(ObsGroup):
        """Observations for policy group."""

        # observation terms (order preserved)
        base_lin_vel      = ObsTerm(
            func  = mdp.base_lin_vel,
            noise = Unoise(n_min=-0.1, n_max=0.1),
        )
        base_ang_vel      = ObsTerm(
            func  = mdp.base_ang_vel,
            noise = Unoise(n_min=-0.2, n_max=0.2),
        )
        projected_gravity = ObsTerm(
            func  = mdp.projected_gravity,
            noise = Unoise(n_min=-0.05, n_max=0.05),
        )
        velocity_commands = ObsTerm(
            func   = mdp.generated_commands,
            params = {"command_name": "base_velocity"},
        )
        joint_pos         = ObsTerm(
            func  = mdp.joint_pos_rel,
            noise = Unoise(n_min=-0.01, n_max=0.01),
        )
        joint_vel         = ObsTerm(
            func  = mdp.joint_vel_rel,
            noise = Unoise(n_min=-1.5, n_max=1.5)
        )
        # actions = ObsTerm(func=mdp.last_action)
        last_action = ObsTerm(func=mdp.last_action)
        
        # height_scan = ObsTerm(
        #     func=mdp.height_scan,
        #     params={"sensor_cfg": SceneEntityCfg("height_scanner")},
        #     noise=Unoise(n_min=-0.1, n_max=0.1),
        #     clip=(-1.0, 1.0),
        # )

        def __post_init__(self):
            self.enable_corruption = True
            self.concatenate_terms = True

    # observation groups
    policy: PolicyCfg = PolicyCfg()


@configclass
class EventCfg:
    """Configuration for events."""

    # startup
    physics_material = EventTerm(
        func=mdp.randomize_rigid_body_material,
        mode="startup",
        params={
            "asset_cfg": SceneEntityCfg("robot", body_names=".*"),
            # "static_friction_range": (0.8, 0.8),
            "static_friction_range": (0.6, 1.2),   # (min, max) coefficient
            # "dynamic_friction_range": (0.6, 0.6),
            "dynamic_friction_range": (0.4, 0.9),
            "restitution_range": (0.0, 0.0),
            "num_buckets": 64,
        },
    )

    add_base_mass = EventTerm(
        func=mdp.randomize_rigid_body_mass,
        mode="startup",
        params={
            "asset_cfg": SceneEntityCfg("robot", body_names="base"),
            # "mass_distribution_params": (-5.0, 5.0),
            "mass_distribution_params": (0.8, 1.2),
            # "operation": "add",
            "operation": "scale",         # "scale" | "add" | "abs"
            "distribution": "uniform",
            "recompute_inertia": True,
        },
    )

    reset_scene = EventTerm(
        func=mdp.reset_scene_to_default,
        mode="reset",
        # No params needed.  It resets everything in the scene.
    )

    randomize_com = EventTerm(
        func=mdp.randomize_rigid_body_com, # USE THIS AFTER: your basic walking policy is stable
        mode="startup",
        params={
            "asset_cfg" : SceneEntityCfg("robot", body_names="base"),
            "com_range": {
                "x": (-0.05, 0.05),  # ±5cm forward/back shift
                "y": (-0.03, 0.03),  # ±3cm left/right shift
                "z": (-0.02, 0.02),  # ±2cm up/down shift
            },
        },
    )

    # reset
    base_external_force_torque = EventTerm(
        func=mdp.apply_external_force_torque, # NA
        mode="reset",
        params={
            "asset_cfg"    : SceneEntityCfg("robot", body_names="base"),
            "force_range":  (-5.0, 5.0),
            "torque_range": (-1.0, 1.0),
        },
    )

    reset_base = EventTerm(
        func=mdp.reset_root_state_uniform,
        mode="reset",
        params={
            "asset_cfg": SceneEntityCfg("robot"),
            "pose_range": {
                "x"   : (-0.5, 0.5),
                "y"   : (-0.5, 0.5),
                "yaw" : (-3.14, 3.14)
            },
            "velocity_range": {
                "x"     : (0.0, 0.0),
                "y"     : (0.0, 0.0),
                "z"     : (0.0, 0.0),
                "roll"  : (0.0, 0.0),
                "pitch" : (0.0, 0.0),
                "yaw"   : (0.0, 0.0),
            },
        },
    )

    reset_robot_joints = EventTerm(     #  PROBLEM: if default_pos is 0.0 (joint at zero), scale does nothing!
        func=mdp.reset_joints_by_scale,
        mode="reset",
        params={
            "asset_cfg": SceneEntityCfg("robot"),
            "position_range": (0.5, 1.5),
            "velocity_range": (0.0, 0.0),
        },
    )

    # # Chose either reset_robot_joints or reset_joints_offset  | Dont select both

    # reset_joints_offset = EventTerm(      #  BETTER WHEN: some joints have default of 0.0 (offset still works)
    #     func=mdp.reset_joints_by_offset,
    #     mode="reset",
    #     params={
    #         "asset_cfg": SceneEntityCfg("robot"),
    #         "position_range": (-0.2, 0.2),  # radians of offset
    #         "velocity_range": (-0.1, 0.1),  # small joint velocity noise
    #     },
    # )

    # interval
    push_robot = EventTerm(
        func=mdp.push_by_setting_velocity,
        mode="interval",
        interval_range_s=(10.0, 15.0),
        params={
            "asset_cfg"      : SceneEntityCfg("robot"),
            "velocity_range" : {
                "x":    (-0.5, 0.5),    # m/s forward/back push
                "y":    (-0.5, 0.5),    # m/s sideways push
                "yaw":  (-0.5, 0.5),    # rad/s spin push
                "z":    (0.0, 0.0),
                "roll": (0.0, 0.0),
                "pitch":(0.0, 0.0),            }
        },
    )


@configclass
class RewardsCfg:
    """Reward terms for the MDP."""

    #  ── TASK REWARDS (positive weights) 
    track_lin_vel_xy_exp = RewTerm(
        func   = mdp.track_lin_vel_xy_exp,
        weight = 1.0,
        params = {
            "command_name": "base_velocity",
            "std"         : math.sqrt(0.25)
        }
    )
    track_ang_vel_z_exp  = RewTerm(
        func   = mdp.track_ang_vel_z_exp,
        weight = 0.5,
        params = {
            "command_name" : "base_velocity",
            "std"          : math.sqrt(0.25)
        }
    )
    
    #  ── STABILITY PENALTIES (negative weights) ─
    lin_vel_z_l2         = RewTerm(
        func   = mdp.lin_vel_z_l2,
        weight = -2.0
    )
    ang_vel_xy_l2       = RewTerm(
        func   = mdp.ang_vel_xy_l2,
        weight = -0.05
    )
    flat_orientation_l2 = RewTerm(
        func   = mdp.flat_orientation_l2,
        weight = -0.15
    )
    base_height_l2     = RewTerm(
        func   = mdp.base_height_l2,
        weight = -0.15,
        params={
            "target_height": 0.34,   # Go2 nominal standing height in meters
            # "sensor_cfg": SceneEntityCfg("height_scanner"),  # uncomment for rough terrain
        },
    )

    # ── EFFICIENCY PENALTIES ─

    joint_torques_l2 = RewTerm(
        func   = mdp.joint_torques_l2,
        weight =-1.0e-5
    )
    joint_acc_l2     = RewTerm(
        func   = mdp.joint_acc_l2,
        weight =-2.5e-7
    )
    action_rate_l2  = RewTerm(
        func   = mdp.action_rate_l2,
        weight = -0.01
    )
    feet_air_time  = RewTerm(
        func   = mdp.feet_air_time,
        weight = 0.125,
        params = {
            # "sensor_cfg": SceneEntityCfg("contact_forces", body_names=".*FOOT"),
            "sensor_cfg"   : SceneEntityCfg("contact_forces", body_names=".*foot"),
            "command_name" : "base_velocity",
            "threshold"    : 0.5,
        },
    )
    undesired_contacts = RewTerm(
        func=mdp.undesired_contacts,
        weight=-1.0,
        params={
            "threshold": 1.0,   # minimum contact force in Newtons to count as a violation
            "sensor_cfg": SceneEntityCfg(
                "contact_forces",
                body_names=[".*_thigh", ".*_calf", "base"],  # NOT the feet
            ),
        },
    )
    # # -- optional penalties
    # joint_pos_limits      = RewTerm(
    #     func   = mdp.joint_pos_limits,
    #     weight = 0.0
    # )




@configclass
class TerminationsCfg:
    """Termination terms for the MDP."""

    time_out = DoneTerm(
        func=mdp.time_out,
        time_out=True,
    )

    base_contact = DoneTerm(
        func   = mdp.illegal_contact,
        params = {
            "sensor_cfg": SceneEntityCfg(
                "contact_forces",body_names = "base"
            ),
            "threshold": 1.0},
    )


@configclass
class CurriculumCfg:
    """Curriculum terms for the MDP."""

    terrain_levels = CurrTerm(func=mdp.terrain_levels_vel)



##
# Environment configuration
##



@configclass
class CustomUnitreeGo2EnvCfg(ManagerBasedRLEnvCfg):

    # Scene settings
    scene:        MySceneCfg      = MySceneCfg(num_envs=4096, env_spacing=4.0)
    # Basic settings
    observations: ObservationsCfg = ObservationsCfg()
    actions:      ActionsCfg      = ActionsCfg()
    commands:     CommandsCfg     = CommandsCfg()
    # MDP settings
    rewards:      RewardsCfg      = RewardsCfg()
    terminations: TerminationsCfg = TerminationsCfg()
    events:       EventCfg        = EventCfg()
    curriculum:   CurriculumCfg   = CurriculumCfg()


    def __post_init__(self):
        """Post initialization."""

        # Simulation timestep
        self.sim.dt     = 0.005             # 200 Hz physics
        self.decimation = 4             # policy runs at 200/4 = 50 Hz

        # Episode length: 20 seconds * 50 Hz policy = 1000 steps
        self.episode_length_s = 20.0

        # simulation settings
        self.sim.render_interval                 = self.decimation
        self.sim.physics_material                = self.scene.terrain.physics_material
        self.sim.physx.gpu_max_rigid_patch_count = 10 * 2**15
        # update sensor update periods
        # we tick all the sensors based on the smallest update period (physics update period)
        # if self.scene.height_scanner is not None:
        #     self.scene.height_scanner.update_period = self.decimation * self.sim.dt
        if self.scene.contact_forces is not None:
            self.scene.contact_forces.update_period = self.sim.dt

        # check if terrain levels curriculum is enabled - if so, enable curriculum for terrain generator
        # this generates terrains with increasing difficulty and is useful for training
        if getattr(self.curriculum, "terrain_levels", None) is not None:
            if self.scene.terrain.terrain_generator is not None:
                self.scene.terrain.terrain_generator.curriculum = True
        else:
            if self.scene.terrain.terrain_generator is not None:
                self.scene.terrain.terrain_generator.curriculum = False


@configclass
class CustomUnitreeGo2RoughEnvCfg(CustomUnitreeGo2EnvCfg):
    def __post_init__(self):
        # post init of parent
        super().__post_init__()

        # self.scene.robot = CUSTOM_UNITREE_GO2_CFG.replace(prim_path="{ENV_REGEX_NS}/Robot")
        # self.scene.height_scanner.prim_path = "{ENV_REGEX_NS}/Robot/base"
        # self.scene.height_scanner.prim_path = "{ENV_REGEX_NS}/Robot/go2_description/base"
        # scale down the terrains because the robot is small
        self.scene.terrain.terrain_generator.sub_terrains["boxes"].grid_height_range = (0.025, 0.1)
        self.scene.terrain.terrain_generator.sub_terrains["random_rough"].noise_range = (0.01, 0.06)
        self.scene.terrain.terrain_generator.sub_terrains["random_rough"].noise_step = 0.01

        # reduce action scale
        # self.actions.joint_pos.scale = 0.25

        # event
        # self.events.push_robot = None
        # self.events.add_base_mass.params["mass_distribution_params"] = (-1.0, 3.0)
        # self.events.add_base_mass.params["asset_cfg"].body_names = "base"
        # self.events.base_external_force_torque.params["asset_cfg"].body_names = "base"
        # self.events.reset_robot_joints.params["position_range"] = (1.0, 1.0)
        # self.events.reset_base.params = {
        #     "pose_range": {"x": (-0.5, 0.5), "y": (-0.5, 0.5), "yaw": (-3.14, 3.14)},
        #     "velocity_range": {
        #         "x": (0.0, 0.0),
        #         "y": (0.0, 0.0),
        #         "z": (0.0, 0.0),
        #         "roll": (0.0, 0.0),
        #         "pitch": (0.0, 0.0),
        #         "yaw": (0.0, 0.0),
        #     },
        # }
        # self.events.base_com = None

        # rewards
        # self.rewards.feet_air_time.params["sensor_cfg"].body_names = ".*_foot"
        # self.rewards.feet_air_time.weight = 0.01
        # self.rewards.undesired_contacts = None
        # self.rewards.dof_torques_l2.weight = -0.0002
        # self.rewards.track_lin_vel_xy_exp.weight = 1.5
        # self.rewards.track_ang_vel_z_exp.weight = 0.75
        # self.rewards.dof_acc_l2.weight = -2.5e-7

        # terminations
        # self.terminations.base_contact.params["sensor_cfg"].body_names = ["base", ".*thigh", ".*calf"]




@configclass
class CustomUnitreeGo2FlatEnvCfg(CustomUnitreeGo2EnvCfg):
    def __post_init__(self):
        # post init of parent
        super().__post_init__()

        # Fewer envs for visualisation
        self.scene.num_envs = 2
        self.scene.env_spacing = 2.5

        # override rewards
        self.rewards.flat_orientation_l2.weight = -2.5
        self.rewards.feet_air_time.weight       = 0.25

        # change terrain to flat
        self.scene.terrain.terrain_type         = "plane"
        self.scene.terrain.terrain_generator    = None
        
        # no height scan
        # self.scene.height_scanner               = None
        # self.observations.policy.height_scan    = None

        # no terrain curriculum
        self.curriculum.terrain_levels          = None

        # Disable observation noise during evaluation
        self.observations.policy.enable_corruption = False