# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

import gymnasium as gym

from . import agents

##
# Register Gym environments.
##

#__init__.py



gym.register(
    id="Custom-Unitree-Go2-Rough-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.custom_unitree_go2_env_cfg:CustomUnitreeGo2RoughEnvCfg",
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:CustomUnitreeGo2RoughPPORunnerCfg",
    },
)

gym.register(
    id="Custom-Unitree-Go2-Flat-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.custom_unitree_go2_env_cfg:CustomUnitreeGo2FlatEnvCfg",
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:CustomUnitreeGo2FlatPPORunnerCfg",
    },
)




gym.register(
    # ── id ────────────────────────────────────────────────────────────────
    # This is the string you pass to --task on the command line.
    # Convention: <Robot>-<Task>-v<version>
    id="Dog-Walk-v0",
 
    # ── entry_point ───────────────────────────────────────────────────────
    # "python.module.path:ClassName"
    # Isaac Lab's ManagerBasedRLEnv is the standard env class.
    # It reads all behaviour from the Cfg dataclass — you don't need your own
    # env class unless you have custom step/reset logic.
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
 
    # ── disable_env_checker ───────────────────────────────────────────────
    # Gymnasium's env checker can false-alarm on Isaac Lab envs (they use
    # GPU tensors, not numpy arrays).  Always set this to True.
    disable_env_checker=True,
 
    # ── kwargs ────────────────────────────────────────────────────────────
    # env_cfg_entry_point → tells the training script which dataclass to use.
    # rl_games_cfg_entry_point, rsl_rl_cfg_entry_point, etc. → trainer configs.
    kwargs={
        # The main environment config (scene + actions + events + rewards…)
        "env_cfg_entry_point": (
            # "dog_walking.robot_env_cfg:DogWalkingEnvCfg"
            f"{__name__}.robot_env_cfg:DogWalkingEnvCfg"

        ),
 
        # RSL-RL PPO trainer config (you create this separately).
        # See isaaclab/source/extensions/isaaclab_tasks/isaaclab_tasks/
        #     manager_based/locomotion/velocity/config/anymal_c/ for an example.
        "rsl_rl_cfg_entry_point": (
            # "dog_walking.agents.rsl_rl_ppo_cfg:DogWalkingPPORunnerCfg"
            f"{agents.__name__}.rsl_rl_ppo_cfg:DogWalkingPPORunnerCfg"
        ),
 
        # If you use rl_games instead of rsl_rl, add:
        # "rl_games_cfg_entry_point": (
        #     "dog_walking.agents.rl_games_ppo_cfg:DogWalkingAgentCfg"
        # ),
    },
)
 
##############################################################################
# PLAY / EVALUATION environment  (no randomisation, fewer envs)
##############################################################################
gym.register(
    id="Dog-Walk-Play-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": (
            # "dog_walking.robot_env_cfg:DogWalkingEnvCfg_PLAY"
            f"{__name__}.robot_env_cfg:DogWalkingEnvCfg_PLAY"
        ),
        "rsl_rl_cfg_entry_point": (
            # "dog_walking.agents.rsl_rl_ppo_cfg:DogWalkingPPORunnerCfg"
             f"{agents.__name__}.rsl_rl_ppo_cfg:DogWalkingPPORunnerCfg"
        ),
    },
)
