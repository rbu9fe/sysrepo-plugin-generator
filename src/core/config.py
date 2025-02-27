from typing import Dict, Any, List, Optional


class YangMainModuleConfiguration:
    def __init__(self, name, prefix, disable, skip_prefix_mode) -> None:
        self.name: str = name
        self.prefix: str = prefix
        self.disable: bool = disable
        self.skip_prefix_mode: bool = skip_prefix_mode

    def get_name(self) -> str:
        return self.name

    def get_prefix(self) -> str:
        return self.prefix

    def get_disable(self) -> bool:
        return self.disable

    def get_skip_prefix_mode(self) -> bool:
        return self.skip_prefix_mode


class YangModulesConfiguration:
    def __init__(self, config: Dict[str, Any]) -> None:
        assert ("main" in config)

        self.main_modules: List[YangMainModuleConfiguration] = []
        self.other_modules: List[str] = []
        self.features: Optional[List[str]] = None

        for module in config["main"]:
            self.main_modules.append(YangMainModuleConfiguration(module["name"], module["prefix"], module["disable"] if "disable" in module else False, module["skip_prefix_mode"] if "skip_prefix_mode" in module else None))

        if "other" in config:
            self.other_modules = config["other"]

        if "features" in config:
            self.features = config["features"]

    def get_main_modules(self) -> Dict[str, YangMainModuleConfiguration]:
        return self.main_modules

    def get_other_modules(self) -> List[str]:
        return self.other_modules

    def get_features(self) -> Optional[List[str]]:
        return self.features


class YangPrefixConfiguration:
    def __init__(self, config: Dict[str, Any]) -> None:
        self.cfg: Dict[str, str] = config

    def check_prefix(self, prefix: str) -> bool:
        if prefix in self.cfg:
            return True
        return False

    def get_prefix_value(self, prefix: str) -> str:
        return self.cfg[prefix]


class YangTypesConfiguration:
    def __init__(self, config: Dict[str, Any]) -> None:
        self.types_map: Dict[str, str] = config

    def get_types_map(self) -> Dict[str, str]:
        return self.types_map


class YangConfiguration:
    def __init__(self, config: Dict[str, Any]):
        self.mod_cfg: YangModulesConfiguration = YangModulesConfiguration(config["modules"])
        self.types_cfg: YangTypesConfiguration = YangTypesConfiguration(config["types"])

    def get_modules_configuration(self) -> YangModulesConfiguration:
        return self.mod_cfg

    def get_types_configuration(self) -> YangTypesConfiguration:
        return self.types_cfg


class GeneratorConfiguration:
    def __init__(self, config: Dict[str, Any]):
        self.name: str = config["generator"]["name"]
        self.yang_cfg: YangConfiguration = YangConfiguration(config["yang"])

    def get_name(self) -> str:
        return self.name

    def get_yang_configuration(self) -> YangConfiguration:
        return self.yang_cfg
