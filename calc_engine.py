import math

def calculate_flight_plan(
    area_km2: float,          # 测区面积 (km2)
    target_gsd_cm: float,     # 目标 GSD (cm/pixel)
    focal_length_mm: float,   # 镜头焦距 (mm)
    sensor_w_mm: float,       # 感光元件宽 (mm)
    sensor_h_mm: float,       # 感光元件高 (mm)
    pixel_w: int,             # 图像宽度像素 (px)
    pixel_h: int,             # 图像高度像素 (px)
    overlap_heading: float,   # 航向重叠度 (0-1)
    overlap_side: float,      # 旁向重叠度 (0-1)
    flight_speed_ms: float = 10.0 # 飞行速度 (m/s)
):
    # 1. 基础参数转换
    pixel_size_mm = sensor_w_mm / pixel_w
    gsd_m = target_gsd_cm / 100.0
    f_m = focal_length_mm / 1000.0
    
    # 2. 反算航高 H (m)
    flight_height = (gsd_m * f_m) / (pixel_size_mm / 1000.0)
    
    # 3. 地面覆盖宽度与高度 (m)
    ground_width = pixel_w * gsd_m
    ground_height = pixel_h * gsd_m
    
    # 4. 步进距离
    dx = ground_width * (1.0 - overlap_heading)  # 航向拍照间距
    dy = ground_height * (1.0 - overlap_side)    # 旁向航线间距
    
    # 5. 拍照时间间隔 (s)
    photo_interval = dx / flight_speed_ms
    
    # 6. 基于测区面积计算
    area_m2 = max(area_km2, 0.001) * 1_000_000
    side_length = math.sqrt(area_m2)
    
    num_lines = math.ceil(side_length / dy) + 1
    photos_per_line = math.ceil(side_length / dx) + 1
    total_photos = num_lines * photos_per_line
    
    total_distance_m = num_lines * side_length
    flight_time_min = (total_distance_m / flight_speed_ms) / 60.0
    
    return {
        "flight_height_m": round(flight_height, 1),
        "photo_interval_s": round(photo_interval, 2),
        "num_lines": num_lines,
        "photos_per_line": photos_per_line,
        "total_photos": total_photos,
        "flight_time_min": round(flight_time_min, 1),
        "total_distance_km": round(total_distance_m / 1000.0, 2),
        "ground_cover_w": round(ground_width, 1),
        "ground_cover_h": round(ground_height, 1),
        "dx": round(dx, 2),
        "dy": round(dy, 2)
    }