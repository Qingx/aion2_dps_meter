class SkillDamageInfo:
    def __init__(self):
        self.damage = []
        self.damage_by_multiplier_type = {}
        self.total_damage = 0


class DamageCalculator:
    def __init__(self):
        self.total = 0
        self.count = 0

        self.last_timestamp_ms = 0
        self.average = 0
        self.moving_average = 0

        self.data = []
        self.by_skills = {}


    def process_damage(self, damage_list, now):
        # data will be cutted by moving average window further
        self.data += damage_list
        self.count += len(damage_list)

        for damage_info in damage_list:
            self.total += damage_info.damage

            if damage_info.skill_name not in self.by_skills:
                self.by_skills[damage_info.skill_name] = SkillDamageInfo()
            skill_damage_info = self.by_skills[damage_info.skill_name]
            skill_damage_info.damage.append(damage_info.damage)
            skill_damage_info.total_damage += damage_info.damage

            if damage_info.multiplier_type not in skill_damage_info.damage_by_multiplier_type:
                skill_damage_info.damage_by_multiplier_type[damage_info.multiplier_type] = {
                    "damage": [],
                    "total_damage": 0
                }
            multiplier_type_damage_info = skill_damage_info.damage_by_multiplier_type[damage_info.multiplier_type]
            multiplier_type_damage_info["damage"].append(damage_info.damage)
            multiplier_type_damage_info["total_damage"] += damage_info.damage

        self.last_timestamp_ms = now
        self.average = self.total / self.count if self.count != 0 else 0
        self.moving_average = self._moving_average_by_time(now)

        print("=", now, ":", round(self.moving_average, 2), round(self.average, 2))


    def _moving_average_by_time(self, now, window_ms=1000):
        self.data = [d for d in self.data if d.timestamp >= now - window_ms]

        window_size = len(self.data)

        if window_size == 0:
            return 0

        total_damage = sum(d.damage for d in self.data)
        return total_damage / window_size