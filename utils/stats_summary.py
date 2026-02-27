import statistics

def summarize_data(data_list):
    temps = [d["temperature_score"] for d in data_list]
    lights = [d["light_score"] for d in data_list]
    sounds = [d["sound_score"] for d in data_list]

    summary = {
        "temp_avg": round(statistics.mean(temps), 2),
        "temp_min": min(temps),
        "temp_max": max(temps),

        "light_avg": round(statistics.mean(lights), 2),
        "light_min": min(lights),
        "light_max": max(lights),

        "sound_avg": round(statistics.mean(sounds), 2),
        "sound_min": min(sounds),
        "sound_max": max(sounds),
    }

    return summary