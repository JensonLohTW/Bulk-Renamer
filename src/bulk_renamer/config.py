"""
配置文件解析模块。
"""
import os
import yaml
from dataclasses import dataclass, field


@dataclass
class TaskConfig:
    name: str
    directories: list[str]
    patterns: list[str]
    recursive: bool = True


@dataclass
class AppConfig:
    tasks: list[TaskConfig]
    dry_run: bool = False
    verbose: bool = True
    confirm_before_run: bool = True
    mac_clean: bool = True


def load_config(path: str) -> AppConfig:
    """从 YAML 文件加载配置，返回 AppConfig 实例。"""
    if not os.path.isfile(path):
        raise FileNotFoundError(f"配置文件不存在：{path}")

    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        raise ValueError("配置文件格式错误：顶层必须是 YAML 映射")

    defaults = data.get("defaults", {})
    dry_run = bool(defaults.get("dry_run", False))
    verbose = bool(defaults.get("verbose", True))
    confirm_before_run = bool(defaults.get("confirm_before_run", True))
    mac_clean = bool(defaults.get("mac_clean", True))

    raw_tasks = data.get("tasks", [])
    if not isinstance(raw_tasks, list) or len(raw_tasks) == 0:
        raise ValueError("配置文件中未找到任何任务（tasks 列表为空或不存在）")

    tasks: list[TaskConfig] = []
    for i, task in enumerate(raw_tasks, start=1):
        if not isinstance(task, dict):
            raise ValueError(f"任务 #{i} 格式错误：必须是 YAML 映射")

        name = task.get("name", f"任务 {i}")

        dirs = task.get("directories")
        if not dirs or not isinstance(dirs, list):
            raise ValueError(f"任务 '{name}' 缺少 directories 字段或格式错误")

        patterns = task.get("patterns")
        if not patterns or not isinstance(patterns, list):
            raise ValueError(f"任务 '{name}' 缺少 patterns 字段或格式错误")

        expanded_dirs = [os.path.expanduser(d) for d in dirs]
        recursive = bool(task.get("recursive", True))

        tasks.append(TaskConfig(
            name=name,
            directories=expanded_dirs,
            patterns=patterns,
            recursive=recursive,
        ))

    return AppConfig(
        tasks=tasks,
        dry_run=dry_run,
        verbose=verbose,
        confirm_before_run=confirm_before_run,
        mac_clean=mac_clean,
    )
