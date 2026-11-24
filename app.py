import json
import streamlit as st
import streamlit.components.v1 as components


# =========================================================
# 1. 데이터 구조: 냉각수와 레이싱 섹터를 리스트로 저장
# =========================================================

coolant_list = [
    "물-에틸렌글리콜",
    "절연 냉각유",
    "액체 질소"
]

track_sectors = [
    {"name": "SECTOR 1", "type": "직선 코스"},
    {"name": "SECTOR 2", "type": "커브 코스"},
    {"name": "SECTOR 3", "type": "울퉁불퉁한 코스"}
]


# =========================================================
# 2. 함수(def): 냉각수 설정에 따른 냉각 효율 계산
# =========================================================

def simulate_race(coolant, flow_rate, battery_output):
    # if-elif-else: 선택한 냉각수에 따라 가상 냉각 효율 결정
    if coolant == "물-에틸렌글리콜":
        cooling_efficiency = 1.0
    elif coolant == "절연 냉각유":
        cooling_efficiency = 0.9
    elif coolant == "액체 질소":
        cooling_efficiency = 1.2
    else:
        cooling_efficiency = 0.0

    # 교육용 게임 모델의 시작 온도 계산
    initial_temperature = (
        38
        + (battery_output - 50) * 0.22
        - (flow_rate - 1) * 0.75 * cooling_efficiency
    )

    # if-elif-else: 배터리 온도 상태 분류
    if initial_temperature < 40:
        temperature_status = "과냉각"
    elif initial_temperature <= 80:
        temperature_status = "적합"
    else:
        temperature_status = "과열"

    return initial_temperature, temperature_status, cooling_efficiency


# =========================================================
# 3. Streamlit 페이지 설정
# =========================================================

st.set_page_config(
    page_title="THERMAL RUSH",
    page_icon="🏎️",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #070d19 0%, #101b32 100%);
    color: #f4f8ff;
}
h1, h2, h3 {
    color: #55d9ff !important;
}
div[data-testid="stMetric"] {
    background: #14243b;
    border: 1px solid #294d70;
    border-radius: 12px;
    padding: 12px;
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# 4. 게임 제목과 안내
# =========================================================

st.title("🏎️ THERMAL RUSH")
st.subheader("F1 HYPERCAR BATTERY COOLING RACE")
st.write(
    "냉각 시스템을 직접 설정하고 세 가지 특수 트랙을 주행하세요. "
    "빠른 기록뿐 아니라 배터리 온도 관리도 중요합니다."
)


# =========================================================
# 5. 냉각 시스템 설정
# =========================================================

st.markdown("### ⚙️ 배터리 냉각 시스템 설정")

setting_col1, setting_col2, setting_col3 = st.columns(3)

with setting_col1:
    coolant = st.selectbox("냉각수 종류", coolant_list)

with setting_col2:
    flow_rate = st.slider(
        "냉각수 유량 (L/min)",
        min_value=1.0,
        max_value=10.0,
        value=5.0,
        step=0.5
    )

with setting_col3:
    battery_output = st.slider(
        "배터리 출력 (%)",
        min_value=50,
        max_value=100,
        value=75,
        step=5
    )


# =========================================================
# 6. 설정값을 바탕으로 초기 냉각 상태 계산
# =========================================================

initial_temperature, initial_status, cooling_efficiency = simulate_race(
    coolant,
    flow_rate,
    battery_output
)

st.markdown("### 📊 선택한 냉각 시스템")

metric_col1, metric_col2, metric_col3 = st.columns(3)
metric_col1.metric("냉각수", coolant)
metric_col2.metric("예상 초기 온도", f"{initial_temperature:.1f} ℃")
metric_col3.metric("초기 배터리 상태", initial_status)

st.caption(
    "※ 냉각 효율과 온도 변화는 실제 F1 차량의 실험값이 아닌 "
    "게임 진행을 위한 교육용 가상 모델입니다."
)


# =========================================================
# 7. for 반복문: 섹터 목록을 게임 데이터로 변환
# =========================================================

sector_data = []

# for 반복문으로 각 섹터의 번호, 이름, 코스 유형을 차례로 저장
for sector_number, sector_info in enumerate(track_sectors):
    sector_data.append({
        "number": sector_number + 1,
        "name": sector_info["name"],
        "type": sector_info["type"]
    })


# =========================================================
# 8. Python 설정을 JavaScript 게임에 전달
# =========================================================

game_config = {
    "coolant": coolant,
    "flow_rate": flow_rate,
    "battery_output": battery_output,
    "initial_temperature": initial_temperature,
    "cooling_efficiency": cooling_efficiency,
    "track_sectors": sector_data
}


# =========================================================
# 9. 레이싱 게임: HTML / CSS / JavaScript
# =========================================================

game_html = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
* { box-sizing: border-box; }

body {
    margin: 0;
    padding: 10px;
    color: #f4f8ff;
    background: #080e1b;
    font-family: Arial, "Malgun Gothic", sans-serif;
}

.game_shell {
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 14px;
    background: linear-gradient(145deg, #111e34, #091321);
    border: 1px solid #285078;
    border-radius: 18px;
    box-shadow: 0 15px 45px rgba(0,0,0,.35);
}

.top_line {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
    margin-bottom: 12px;
}

.game_logo {
    color: #59ddff;
    font-size: 23px;
    font-weight: 900;
    letter-spacing: 2px;
}

.track_badge {
    color: #d7f7ff;
    background: #173752;
    border: 1px solid #31799a;
    border-radius: 20px;
    padding: 7px 13px;
    font-size: 12px;
    font-weight: bold;
}

.hud {
    display: grid;
    grid-template-columns: repeat(7, minmax(0, 1fr));
    gap: 8px;
    margin-bottom: 10px;
}

.hud_card {
    min-width: 0;
    padding: 9px 5px;
    text-align: center;
    background: #172942;
    border: 1px solid #294968;
    border-radius: 10px;
}

.hud_label {
    color: #9bb8d2;
    font-size: 10px;
    letter-spacing: 1px;
}

.hud_value {
    margin-top: 5px;
    color: #5cddff;
    font-size: clamp(15px, 2.4vw, 22px);
    font-weight: 900;
}

.canvas_wrap {
    position: relative;
    overflow: hidden;
    border: 2px solid #3ba8d1;
    border-radius: 13px;
    background: #101c2b;
}

canvas {
    display: block;
    width: 100%;
    height: auto;
    aspect-ratio: 1000 / 620;
    outline: none;
}

.bottom_info {
    display: flex;
    justify-content: space-between;
    gap: 10px;
    flex-wrap: wrap;
    margin-top: 10px;
    padding: 11px 13px;
    color: #c5d8e9;
    background: #172942;
    border-radius: 10px;
    font-size: 12px;
    line-height: 1.7;
}

.key {
    display: inline-block;
    padding: 2px 6px;
    margin: 1px;
    color: #071321;
    background: #65dcff;
    border-radius: 4px;
    font-weight: bold;
}

button {
    border: 0;
    border-radius: 9px;
    padding: 12px 24px;
    color: #06111e;
    background: linear-gradient(90deg, #49d7ff, #8af0ff);
    font-weight: 900;
    font-size: 15px;
    cursor: pointer;
    box-shadow: 0 5px 18px rgba(44, 194, 239, .22);
}

button:hover { filter: brightness(1.12); transform: translateY(-1px); }

.audio_controls {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    flex-wrap: wrap;
    gap: 7px;
}

.sound_button {
    padding: 8px 12px;
    color: #dffaff;
    background: #173752;
    border: 1px solid #31799a;
    box-shadow: none;
    font-size: 11px;
    letter-spacing: 1px;
}

.music_button {
    color: #fff0b8;
    border-color: #8b7542;
    background: #3b3020;
}

.music_volume_label {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 6px 9px;
    color: #a9c8df;
    background: #14243a;
    border: 1px solid #294968;
    border-radius: 8px;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: .7px;
}

#music_volume {
    width: 78px;
    accent-color: #62ddff;
    cursor: pointer;
}

.overlay {
    position: absolute;
    inset: 0;
    z-index: 5;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 22px;
    text-align: center;
    background: rgba(4, 10, 20, .78);
    backdrop-filter: blur(5px);
}

.overlay h2 {
    margin: 0 0 8px;
    color: #65e4ff;
    font-size: clamp(25px, 5vw, 46px);
    letter-spacing: 3px;
    text-shadow: 0 0 22px rgba(62, 207, 255, .45);
}

.overlay p {
    max-width: 620px;
    color: #d6e7f5;
    line-height: 1.8;
    font-size: 13px;
}

.result_overlay {
    display: none;
    position: absolute;
    inset: 0;
    z-index: 10;
    overflow-y: auto;
    align-items: center;
    justify-content: center;
    padding: 16px;
    background: rgba(2, 7, 17, .88);
    backdrop-filter: blur(8px);
}

.result_panel {
    width: min(600px, 96%);
    padding: 22px;
    text-align: center;
    background: linear-gradient(145deg, #172b47, #0b1729);
    border: 2px solid #3c9cc3;
    border-radius: 18px;
    box-shadow: 0 0 45px rgba(35, 177, 225, .22);
}

.result_kicker {
    color: #91c9e5;
    font-size: 12px;
    letter-spacing: 3px;
    font-weight: bold;
}

.result_grade {
    margin: 4px 0;
    color: #ffe17b;
    font-size: clamp(54px, 10vw, 82px);
    line-height: 1.1;
    font-weight: 1000;
    text-shadow: 0 0 28px rgba(255, 211, 86, .25);
}

.result_status {
    margin: 8px 0 3px;
    color: #71e7ff;
    font-size: clamp(27px, 5vw, 39px);
    font-weight: 900;
}

.result_temp {
    color: white;
    font-size: clamp(30px, 6vw, 45px);
    font-weight: 900;
}

.result_description {
    color: #bdd0e1;
    font-size: 12px;
    margin: 7px 0 14px;
}

.result_stats {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
    margin: 14px 0;
}

.result_stat {
    padding: 10px;
    background: #1c3553;
    border: 1px solid #315777;
    border-radius: 9px;
}

.result_stat span {
    display: block;
    color: #9bb8d2;
    font-size: 11px;
}

.result_stat strong {
    display: block;
    margin-top: 4px;
    color: white;
    font-size: 20px;
}

.sector_results {
    margin: 12px 0;
    text-align: left;
    color: #d9e8f5;
    font-size: 12px;
    line-height: 1.8;
}

.sector_result_row {
    display: flex;
    justify-content: space-between;
    gap: 8px;
    padding: 6px 2px;
    border-bottom: 1px solid #2b4966;
}

@media (max-width: 760px) {
    .hud { grid-template-columns: repeat(4, minmax(0, 1fr)); }
    .audio_controls { margin-left: auto; }
    .game_shell { padding: 8px; }
    .bottom_info { font-size: 11px; }
}

@media (max-width: 420px) {
    .hud { grid-template-columns: repeat(3, minmax(0, 1fr)); }
    #music_volume { width: 58px; }
}
</style>
</head>

<body>
<div class="game_shell">

    <div class="top_line">
        <div class="game_logo">THERMAL RUSH</div>
        <div class="track_badge" id="background_name">TRACK LOADING</div>
        <div class="audio_controls">
            <button class="sound_button" id="sound_button">SFX: ON</button>
            <button class="sound_button music_button" id="music_button">MUSIC: ON</button>
            <label class="music_volume_label" for="music_volume">BGM VOL
                <input id="music_volume" type="range" min="0" max="100" value="55">
            </label>
        </div>
    </div>

    <div class="hud">
        <div class="hud_card">
            <div class="hud_label">SPEED</div>
            <div class="hud_value" id="speed_value">0</div>
        </div>
        <div class="hud_card">
            <div class="hud_label">BATTERY TEMP</div>
            <div class="hud_value" id="temp_value">0℃</div>
        </div>
        <div class="hud_card">
            <div class="hud_label">RACE TIME</div>
            <div class="hud_value" id="time_value">0.0s</div>
        </div>
        <div class="hud_card">
            <div class="hud_label">SECTOR</div>
            <div class="hud_value" id="sector_value">1 / 3</div>
        </div>
        <div class="hud_card">
            <div class="hud_label">NITRO</div>
            <div class="hud_value" id="nitro_value">READY</div>
        </div>
        <div class="hud_card">
            <div class="hud_label">DRIFT BOOST</div>
            <div class="hud_value" id="drift_charge_value">READY</div>
        </div>
        <div class="hud_card">
            <div class="hud_label">SCORE</div>
            <div class="hud_value" id="score_value">0</div>
        </div>
    </div>

    <div class="canvas_wrap">
        <canvas id="race_canvas" width="1000" height="620" tabindex="0"></canvas>

        <div class="overlay" id="start_overlay">
            <h2>THERMAL RUSH</h2>
            <p>
                직선 · 커브 · 험로를 통과하고 배터리 온도를 관리하세요.<br>
                콘·방벽·오일 함정을 피하고 부스트 패드를 획득하세요.
            </p>
            <p>
                <b>W / ↑</b> 가속 &nbsp; <b>S / ↓</b> 감속<br>
                <b>A / ←</b> 왼쪽 &nbsp; <b>D / →</b> 오른쪽<br>
                <b>SHIFT + 방향키</b> 드리프트 후 SHIFT 해제 시 미니 부스트 &nbsp; <b>SPACE</b> 니트로<br>
                장애물 충돌은 감속, 오일은 미끄러짐, 청록색 패드는 부스트!<br>
                오리지널 아케이드 배경음은 MUSIC 버튼과 BGM VOL로 따로 조절할 수 있습니다.
            </p>
            <button id="start_button">START RACE</button>
        </div>

        <div class="result_overlay" id="result_overlay">
            <div class="result_panel">
                <div class="result_kicker" id="result_kicker">RACE COMPLETE</div>
                <div class="result_grade" id="result_grade">S</div>
                <div class="result_status" id="result_status">적합</div>
                <div class="result_temp" id="result_temp">65.0℃</div>
                <div class="result_description" id="result_description">
                    배터리 온도 상태와 주행 기록
                </div>
                <div class="result_stats">
                    <div class="result_stat">
                        <span>완주 시간</span>
                        <strong id="result_time">0.0초</strong>
                    </div>
                    <div class="result_stat">
                        <span>선택 냉각수</span>
                        <strong id="result_coolant">-</strong>
                    </div>
                    <div class="result_stat">
                        <span>획득 점수</span>
                        <strong id="result_score">0</strong>
                    </div>
                    <div class="result_stat">
                        <span>장애물 회피</span>
                        <strong id="result_avoided">0개</strong>
                    </div>
                </div>
                <div class="sector_results" id="sector_results"></div>
                <button id="restart_button">RACE AGAIN</button>
            </div>
        </div>
    </div>

    <div class="bottom_info">
        <div>
            <b>CONTROL</b><br>
            <span class="key">W</span>/<span class="key">↑</span> 가속
            <span class="key">S</span>/<span class="key">↓</span> 감속
            <span class="key">A</span>/<span class="key">D</span> 조향
            <span class="key">SHIFT</span> 드리프트
            <span class="key">SPACE</span> 니트로
        </div>
        <div id="game_message">START RACE를 눌러 게임을 시작하세요.</div>
    </div>

</div>

<script>
const game_config = __CONFIG__;

const canvas = document.getElementById("race_canvas");
const ctx = canvas.getContext("2d", { alpha: false });

const canvas_width = canvas.width;
const canvas_height = canvas.height;
const horizon_y = 205;
const road_base_width = 780;
const sector_length = 1300;
const total_distance = sector_length * 3;
const visible_distance = 2050;

const background_themes = [
    { name: "NEON CITY", sky_top: "#101a3c", sky_bottom: "#bd4b78", ground: "#172b35", mountain: "#273653", accent: "#36dfff" },
    { name: "DESERT RUN", sky_top: "#472c48", sky_bottom: "#f0a45c", ground: "#80543c", mountain: "#bd7951", accent: "#ffe08a" },
    { name: "ALPINE CIRCUIT", sky_top: "#173b60", sky_bottom: "#a9d5e4", ground: "#244c43", mountain: "#d6e6ed", accent: "#9ff3ff" },
    { name: "COASTAL NIGHT", sky_top: "#061b32", sky_bottom: "#236c83", ground: "#123d43", mountain: "#164b5d", accent: "#61ffe0" }
];

let selected_theme = background_themes[0];
let race_running = false;
let race_finished = false;
let last_frame_time = 0;
let race_time = 0;
let distance_travelled = 0;
let car_speed = 0;
let player_position = 0;
let steering_velocity = 0;
let car_tilt = 0;
let battery_temp = game_config.initial_temperature;
let nitro_remaining = 1;
let nitro_active_time = 0;
let boost_time = 0;
let drift_charge = 0;
let drift_boost_time = 0;
let drift_was_pressed = false;
let slip_time = 0;
let slip_direction = 0;
let camera_shake = 0;
let road_curve = 0;
let score = 0;
let passed_hazards = 0;
let sector_records = [];
let current_sector = 0;
let current_sector_start_time = 0;
let hazards = [];
let keys = {};

let sound_enabled = true;
let music_enabled = true;
let music_volume = 0.2475;
let audio_context = null;
let master_gain = null;
let music_gain = null;
let engine_oscillator = null;
let engine_gain = null;
let music_scheduler_timer = null;
let music_next_time = 0;
let music_step = 0;
let noise_buffer = null;
const music_bpm = 124;
const music_chord_roots = [52, 48, 55, 50]; // E minor - C major - G major - Dsus2 계열의 오리지널 진행
const music_chord_intervals = [[0, 7, 12, 15], [0, 7, 12, 16], [0, 7, 12, 16], [0, 7, 12, 14]];
const music_melody_notes = [64, 67, 69, 71, 74, 76]; // E minor pentatonic 계열
const music_melody_patterns = [
    [0, 2, 4, 2, 1, 2, 5, 4],
    [2, 4, 5, 4, 2, 1, 4, 2],
    [0, 2, 4, 5, 4, 2, 1, 2],
    [4, 2, 1, 2, 5, 4, 2, 1]
];

const speed_value = document.getElementById("speed_value");
const temp_value = document.getElementById("temp_value");
const time_value = document.getElementById("time_value");
const sector_value = document.getElementById("sector_value");
const nitro_value = document.getElementById("nitro_value");
const score_value = document.getElementById("score_value");
const drift_charge_value = document.getElementById("drift_charge_value");
const game_message = document.getElementById("game_message");
const start_overlay = document.getElementById("start_overlay");
const result_overlay = document.getElementById("result_overlay");
const sound_button = document.getElementById("sound_button");
const music_button = document.getElementById("music_button");
const music_volume_slider = document.getElementById("music_volume");

function choose_random_theme() {
    selected_theme = background_themes[Math.floor(Math.random() * background_themes.length)];
    document.getElementById("background_name").textContent = selected_theme.name;
}

function get_sector_index(world_distance) {
    return Math.min(2, Math.floor(Math.max(0, world_distance) / sector_length));
}

function get_track_shape(world_distance) {
    const sector_index = get_sector_index(world_distance);
    const local_distance = world_distance - sector_index * sector_length;

    if (sector_index === 0) {
        return { curve: 0, bump: 0, label: "직선 코스" };
    } else if (sector_index === 1) {
        // 사인 곡선을 사용해 커브 시작과 끝이 갑자기 꺾이지 않도록 연결
        const curve_value = Math.sin(local_distance / sector_length * Math.PI * 2);
        return { curve: curve_value * 0.82, bump: 0, label: "커브 코스" };
    } else {
        const bump_value = Math.sin(local_distance * 0.035) * 0.52 + Math.sin(local_distance * 0.081) * 0.22;
        const gentle_curve = Math.sin(local_distance / sector_length * Math.PI) * 0.18;
        return { curve: gentle_curve, bump: bump_value, label: "울퉁불퉁한 코스" };
    }
}

function project_track(world_distance) {
    const relative_distance = world_distance - distance_travelled;
    const depth = Math.max(0, Math.min(1, 1 - relative_distance / visible_distance));
    const shape = get_track_shape(world_distance);
    const y_pos = horizon_y + Math.pow(depth, 1.72) * (canvas_height - horizon_y);
    const center_x = canvas_width / 2 - shape.curve * depth * depth * 172 - Math.sin(world_distance * 0.00125) * depth * 11;
    const half_width = 48 + depth * (road_base_width / 2);

    return { x: center_x, y: y_pos, half_width: half_width, depth: depth, shape: shape, world: world_distance };
}

function make_hazards() {
    // 각 섹터에 장애물과 보상 부스트 패드를 배치
    const hazard_layout = [
        { offset: 250, lane: -0.65, kind: "cone" },
        { offset: 600, lane: 0.55, kind: "oil" },
        { offset: 960, lane: 0.02, kind: "barrier" },
        { offset: 1190, lane: 0.62, kind: "boost" },
        { offset: 1500, lane: -0.58, kind: "oil" },
        { offset: 1810, lane: 0.64, kind: "cone" },
        { offset: 2230, lane: 0.02, kind: "barrier" },
        { offset: 2490, lane: -0.62, kind: "boost" },
        { offset: 2760, lane: 0.62, kind: "barrier" },
        { offset: 3100, lane: -0.58, kind: "oil" },
        { offset: 3480, lane: 0.03, kind: "cone" },
        { offset: 3760, lane: 0.62, kind: "boost" }
    ];

    hazards = hazard_layout.map(function(item) {
        return {
            distance: item.offset,
            lane: item.lane + (Math.random() - 0.5) * 0.08,
            kind: item.kind,
            resolved: false
        };
    });
}

function init_audio() {
    if (audio_context) {
        if (audio_context.state === "suspended") audio_context.resume();
        return;
    }

    const audio_class = window.AudioContext || window.webkitAudioContext;
    if (!audio_class) {
        sound_enabled = false;
        music_enabled = false;
        sound_button.textContent = "SFX: OFF";
        music_button.textContent = "MUSIC: OFF";
        return;
    }

    audio_context = new audio_class();

    // 효과음/엔진음과 배경음을 분리해 각각의 음량을 조절
    master_gain = audio_context.createGain();
    master_gain.gain.value = sound_enabled ? 0.62 : 0;
    master_gain.connect(audio_context.destination);

    music_gain = audio_context.createGain();
    music_gain.gain.value = 0;
    music_gain.connect(audio_context.destination);

    // 드럼에 사용할 짧은 노이즈 버퍼를 한 번만 생성
    const noise_length = audio_context.sampleRate;
    noise_buffer = audio_context.createBuffer(1, noise_length, audio_context.sampleRate);
    const noise_data = noise_buffer.getChannelData(0);
    for (let noise_index = 0; noise_index < noise_length; noise_index++) {
        noise_data[noise_index] = Math.random() * 2 - 1;
    }

    engine_oscillator = audio_context.createOscillator();
    engine_gain = audio_context.createGain();
    const engine_filter = audio_context.createBiquadFilter();
    engine_oscillator.type = "sawtooth";
    engine_oscillator.frequency.value = 55;
    engine_filter.type = "lowpass";
    engine_filter.frequency.value = 420;
    engine_gain.gain.value = 0.0001;
    engine_oscillator.connect(engine_filter);
    engine_filter.connect(engine_gain);
    engine_gain.connect(master_gain);
    engine_oscillator.start();
}

function midi_to_frequency(midi_note) {
    return 440 * Math.pow(2, (midi_note - 69) / 12);
}

function schedule_music_tone(frequency, start_time, duration, waveform, volume, filter_frequency) {
    if (!audio_context || !music_gain) return;

    const oscillator = audio_context.createOscillator();
    const filter_node = audio_context.createBiquadFilter();
    const gain_node = audio_context.createGain();
    oscillator.type = waveform;
    oscillator.frequency.setValueAtTime(frequency, start_time);
    filter_node.type = "lowpass";
    filter_node.frequency.setValueAtTime(filter_frequency || 2200, start_time);
    gain_node.gain.setValueAtTime(0.0001, start_time);
    gain_node.gain.exponentialRampToValueAtTime(Math.max(0.0002, volume), start_time + 0.018);
    gain_node.gain.exponentialRampToValueAtTime(0.0001, start_time + duration);
    oscillator.connect(filter_node);
    filter_node.connect(gain_node);
    gain_node.connect(music_gain);
    oscillator.start(start_time);
    oscillator.stop(start_time + duration + 0.035);
}

function schedule_music_pad(root_note, start_time, bar_index) {
    const chord_intervals = music_chord_intervals[bar_index];
    chord_intervals.forEach(function(interval, chord_index) {
        const oscillator = audio_context.createOscillator();
        const filter_node = audio_context.createBiquadFilter();
        const gain_node = audio_context.createGain();
        oscillator.type = chord_index === 0 ? "triangle" : "sine";
        oscillator.frequency.setValueAtTime(midi_to_frequency(root_note + interval), start_time);
        filter_node.type = "lowpass";
        filter_node.frequency.setValueAtTime(1150, start_time);
        gain_node.gain.setValueAtTime(0.0001, start_time);
        gain_node.gain.linearRampToValueAtTime(0.018, start_time + 0.24);
        gain_node.gain.setValueAtTime(0.018, start_time + 1.35);
        gain_node.gain.exponentialRampToValueAtTime(0.0001, start_time + 1.88);
        oscillator.connect(filter_node);
        filter_node.connect(gain_node);
        gain_node.connect(music_gain);
        oscillator.start(start_time);
        oscillator.stop(start_time + 1.92);
    });
}

function schedule_music_kick(start_time) {
    const oscillator = audio_context.createOscillator();
    const gain_node = audio_context.createGain();
    oscillator.type = "sine";
    oscillator.frequency.setValueAtTime(132, start_time);
    oscillator.frequency.exponentialRampToValueAtTime(48, start_time + 0.13);
    gain_node.gain.setValueAtTime(0.16, start_time);
    gain_node.gain.exponentialRampToValueAtTime(0.0001, start_time + 0.19);
    oscillator.connect(gain_node);
    gain_node.connect(music_gain);
    oscillator.start(start_time);
    oscillator.stop(start_time + 0.21);
}

function schedule_music_noise(start_time, duration, volume, high_frequency) {
    if (!noise_buffer) return;
    const noise_source = audio_context.createBufferSource();
    const filter_node = audio_context.createBiquadFilter();
    const gain_node = audio_context.createGain();
    noise_source.buffer = noise_buffer;
    filter_node.type = "highpass";
    filter_node.frequency.setValueAtTime(high_frequency, start_time);
    gain_node.gain.setValueAtTime(0.0001, start_time);
    gain_node.gain.linearRampToValueAtTime(volume, start_time + 0.006);
    gain_node.gain.exponentialRampToValueAtTime(0.0001, start_time + duration);
    noise_source.connect(filter_node);
    filter_node.connect(gain_node);
    gain_node.connect(music_gain);
    noise_source.start(start_time);
    noise_source.stop(start_time + duration + 0.01);
}

function schedule_music_step(start_time, step_number) {
    const bar_index = Math.floor(step_number / 8) % 4;
    const step_in_bar = step_number % 8;
    const root_note = music_chord_roots[bar_index];
    const sector_index = get_sector_index(distance_travelled);
    const intensity = race_running
        ? 0.68 + Math.min(0.22, car_speed / 1050) + (nitro_active_time > 0 ? 0.1 : 0)
        : 0.60;

    if (step_in_bar === 0) schedule_music_pad(root_note, start_time, bar_index);

    // 베이스는 4박의 짝수 스텝에 배치해 레이싱 리듬을 유지
    if (step_in_bar % 2 === 0) {
        const bass_note = root_note - 12 + ((step_in_bar === 4) ? 7 : 0);
        schedule_music_tone(midi_to_frequency(bass_note), start_time, 0.2, "triangle", 0.055 * intensity, 520);
        if (step_in_bar === 0 || step_in_bar === 4) schedule_music_kick(start_time);
        else schedule_music_noise(start_time, 0.09, 0.025, 1800);
    } else {
        schedule_music_noise(start_time, 0.045, 0.014 * intensity, 6500);
    }

    // 4마디마다 반복되지만 음의 배치가 달라지는 독자적인 짧은 멜로디
    const melody_note_index = music_melody_patterns[bar_index][step_in_bar];
    if (step_in_bar !== 6 || bar_index % 2 === 0) {
        const melody_note = music_melody_notes[melody_note_index];
        schedule_music_tone(midi_to_frequency(melody_note), start_time, 0.17, "triangle", 0.026 * intensity, 2600);
    }

    // 고속 주행과 니트로에서는 하이햇을 조금 더 강조해 속도감을 살림
    if (nitro_active_time > 0 && step_in_bar % 2 === 1) {
        schedule_music_noise(start_time, 0.07, 0.034, 7800);
    }

    // 섹터별 분위기를 살짝 달리해 트랙이 바뀌는 느낌을 음악에도 반영
    if (sector_index === 1 && (step_in_bar === 2 || step_in_bar === 6)) {
        const accent_note = music_melody_notes[(melody_note_index + 2) % music_melody_notes.length] + 12;
        schedule_music_tone(midi_to_frequency(accent_note), start_time, 0.12, "sine", 0.014 * intensity, 3600);
    } else if (sector_index === 2 && step_in_bar % 2 === 1) {
        schedule_music_noise(start_time, 0.055, 0.021 * intensity, 5200);
    }
}

function schedule_background_music() {
    if (!audio_context || !music_enabled || audio_context.state !== "running") return;
    if (music_next_time < audio_context.currentTime - 0.35) {
        music_next_time = audio_context.currentTime + 0.04;
    }

    const schedule_ahead = audio_context.currentTime + 0.12;
    while (music_next_time < schedule_ahead) {
        schedule_music_step(music_next_time, music_step);
        music_step += 1;
        music_next_time += 60 / music_bpm / 2;
    }
}

function start_background_music() {
    if (!music_enabled) return;
    init_audio();
    if (!audio_context || !music_gain) return;
    audio_context.resume();
    music_gain.gain.setTargetAtTime(music_volume * (race_running ? 1 : 0.72), audio_context.currentTime, 0.22);

    if (music_scheduler_timer !== null) return;
    music_step = 0;
    music_next_time = audio_context.currentTime + 0.06;
    music_scheduler_timer = window.setInterval(schedule_background_music, 25);
}

function stop_background_music() {
    if (music_scheduler_timer !== null) {
        window.clearInterval(music_scheduler_timer);
        music_scheduler_timer = null;
    }
    if (music_gain && audio_context) {
        music_gain.gain.setTargetAtTime(0.0001, audio_context.currentTime, 0.12);
    }
}

function update_music_mix() {
    if (!music_gain || !audio_context) return;
    const race_mix = race_running ? 1 : 0.72;
    const target_gain = music_enabled ? music_volume * race_mix : 0.0001;
    music_gain.gain.setTargetAtTime(target_gain, audio_context.currentTime, 0.18);
}

function update_engine_audio() {
    if (!audio_context || !engine_oscillator || !engine_gain) return;

    const now = audio_context.currentTime;
    const target_frequency = 48 + car_speed * 1.12 + (nitro_active_time > 0 || drift_boost_time > 0 ? 28 : 0);
    const target_gain = sound_enabled && race_running ? 0.008 + (car_speed / 230) * 0.019 : 0.0001;
    engine_oscillator.frequency.setTargetAtTime(target_frequency, now, 0.08);
    engine_gain.gain.setTargetAtTime(target_gain, now, 0.12);
}

function play_sfx(sound_kind) {
    if (!sound_enabled || !audio_context || !master_gain) return;

    const now = audio_context.currentTime;
    const oscillator = audio_context.createOscillator();
    const gain_node = audio_context.createGain();
    const filter_node = audio_context.createBiquadFilter();

    let start_frequency = 440;
    let end_frequency = 660;
    let duration = 0.22;
    let wave_type = "triangle";
    let volume = 0.18;

    if (sound_kind === "boost") {
        start_frequency = 260; end_frequency = 980; duration = 0.42; wave_type = "sawtooth"; volume = 0.2;
    } else if (sound_kind === "impact") {
        start_frequency = 150; end_frequency = 48; duration = 0.32; wave_type = "square"; volume = 0.22;
    } else if (sound_kind === "oil") {
        start_frequency = 330; end_frequency = 125; duration = 0.48; wave_type = "triangle"; volume = 0.16;
    } else if (sound_kind === "sector") {
        start_frequency = 520; end_frequency = 820; duration = 0.28; wave_type = "sine"; volume = 0.14;
    } else if (sound_kind === "finish") {
        start_frequency = 440; end_frequency = 1040; duration = 0.65; wave_type = "triangle"; volume = 0.18;
    }

    oscillator.type = wave_type;
    oscillator.frequency.setValueAtTime(start_frequency, now);
    oscillator.frequency.exponentialRampToValueAtTime(Math.max(35, end_frequency), now + duration);
    filter_node.type = "lowpass";
    filter_node.frequency.value = 1600;
    gain_node.gain.setValueAtTime(0.0001, now);
    gain_node.gain.exponentialRampToValueAtTime(volume, now + 0.025);
    gain_node.gain.exponentialRampToValueAtTime(0.0001, now + duration);
    oscillator.connect(filter_node);
    filter_node.connect(gain_node);
    gain_node.connect(master_gain);
    oscillator.start(now);
    oscillator.stop(now + duration + 0.03);
}

function draw_background() {
    const sky_gradient = ctx.createLinearGradient(0, 0, 0, horizon_y);
    sky_gradient.addColorStop(0, selected_theme.sky_top);
    sky_gradient.addColorStop(1, selected_theme.sky_bottom);
    ctx.fillStyle = sky_gradient;
    ctx.fillRect(0, 0, canvas_width, horizon_y + 2);

    ctx.fillStyle = selected_theme.mountain;
    ctx.beginPath();
    ctx.moveTo(0, horizon_y);
    for (let x_pos = 0; x_pos <= canvas_width; x_pos += 25) {
        const peak = 88 + Math.abs(Math.sin(x_pos * 0.009)) * 78 + Math.sin(x_pos * 0.021) * 15;
        ctx.lineTo(x_pos, peak);
    }
    ctx.lineTo(canvas_width, horizon_y);
    ctx.closePath();
    ctx.fill();

    ctx.fillStyle = selected_theme.ground;
    ctx.fillRect(0, horizon_y, canvas_width, canvas_height - horizon_y);

    // 도로 양옆의 표지판과 조명을 원근에 따라 작게 배치
    for (let scenery_index = 0; scenery_index < 13; scenery_index++) {
        const scenery_y = horizon_y + 22 + (scenery_index % 4) * 30;
        const scenery_x = scenery_index % 2 === 0 ? 20 + (scenery_index * 13) % 65 : canvas_width - 35 - (scenery_index * 17) % 70;
        ctx.globalAlpha = 0.18 + (scenery_index % 3) * 0.06;
        ctx.fillStyle = selected_theme.accent;
        ctx.fillRect(scenery_x, scenery_y, 4, 18 + (scenery_index % 4) * 8);
    }
    ctx.globalAlpha = 1;
}

function draw_road() {
    const slice_count = 120;
    const samples = [];

    // 도로의 양쪽 경계를 먼저 연속된 좌표로 계산
    for (let sample_index = 0; sample_index <= slice_count; sample_index++) {
        const depth = sample_index / slice_count;
        const world_distance = distance_travelled + (1 - depth) * visible_distance;
        samples.push(project_track(world_distance));
    }

    // 갓길을 단일 다각형으로 채워 조각 사이의 빈틈을 제거
    ctx.beginPath();
    ctx.moveTo(samples[0].x - samples[0].half_width - 26, samples[0].y);
    for (let sample_index = 1; sample_index < samples.length; sample_index++) {
        const point = samples[sample_index];
        ctx.lineTo(point.x - point.half_width - 26, point.y + 0.5);
    }
    for (let sample_index = samples.length - 1; sample_index >= 0; sample_index--) {
        const point = samples[sample_index];
        ctx.lineTo(point.x + point.half_width + 26, point.y + 0.5);
    }
    ctx.closePath();
    ctx.fillStyle = "#e64e59";
    ctx.fill();

    // 아스팔트도 하나의 연속된 면으로 렌더링
    ctx.beginPath();
    ctx.moveTo(samples[0].x - samples[0].half_width, samples[0].y);
    for (let sample_index = 1; sample_index < samples.length; sample_index++) {
        const point = samples[sample_index];
        ctx.lineTo(point.x - point.half_width, point.y + 0.5);
    }
    for (let sample_index = samples.length - 1; sample_index >= 0; sample_index--) {
        const point = samples[sample_index];
        ctx.lineTo(point.x + point.half_width, point.y + 0.5);
    }
    ctx.closePath();
    const road_gradient = ctx.createLinearGradient(0, horizon_y, 0, canvas_height);
    road_gradient.addColorStop(0, "#3b4655");
    road_gradient.addColorStop(1, "#202a37");
    ctx.fillStyle = road_gradient;
    ctx.fill();

    // 구간별 색상 띠를 갓길 위에 겹쳐 그리되 각 조각을 조금씩 이어지게 처리
    for (let sample_index = 0; sample_index < samples.length - 1; sample_index++) {
        const far_point = samples[sample_index];
        const near_point = samples[sample_index + 1];
        const stripe_on = Math.floor(far_point.world / 115) % 2 === 0;
        ctx.fillStyle = stripe_on ? "#f5f7fb" : "#d94a55";

        const left_outer_far = far_point.x - far_point.half_width - 26;
        const left_inner_far = far_point.x - far_point.half_width;
        const left_outer_near = near_point.x - near_point.half_width - 26;
        const left_inner_near = near_point.x - near_point.half_width;
        ctx.beginPath();
        ctx.moveTo(left_outer_far, far_point.y);
        ctx.lineTo(left_inner_far, far_point.y);
        ctx.lineTo(left_inner_near, near_point.y + 0.7);
        ctx.lineTo(left_outer_near, near_point.y + 0.7);
        ctx.closePath();
        ctx.fill();

        const right_outer_far = far_point.x + far_point.half_width + 26;
        const right_inner_far = far_point.x + far_point.half_width;
        const right_outer_near = near_point.x + near_point.half_width + 26;
        const right_inner_near = near_point.x + near_point.half_width;
        ctx.beginPath();
        ctx.moveTo(right_inner_far, far_point.y);
        ctx.lineTo(right_outer_far, far_point.y);
        ctx.lineTo(right_outer_near, near_point.y + 0.7);
        ctx.lineTo(right_inner_near, near_point.y + 0.7);
        ctx.closePath();
        ctx.fill();
    }

    // 중앙 점선과 도로 양쪽의 연속된 흰색 경계선
    for (let sample_index = 0; sample_index < samples.length - 1; sample_index++) {
        const far_point = samples[sample_index];
        const near_point = samples[sample_index + 1];
        if (Math.floor(far_point.world / 135) % 2 === 0) {
            ctx.strokeStyle = "rgba(245,250,255,0.78)";
            ctx.lineWidth = 2 + near_point.depth * 3.5;
            ctx.beginPath();
            ctx.moveTo(far_point.x, far_point.y);
            ctx.lineTo(near_point.x, near_point.y + 0.4);
            ctx.stroke();
        }
    }

    ctx.strokeStyle = "rgba(255,255,255,0.82)";
    ctx.lineWidth = 2;
    ctx.beginPath();
    samples.forEach(function(point, index) {
        const x_pos = point.x - point.half_width + 3;
        if (index === 0) ctx.moveTo(x_pos, point.y);
        else ctx.lineTo(x_pos, point.y + 0.4);
    });
    ctx.stroke();
    ctx.beginPath();
    samples.forEach(function(point, index) {
        const x_pos = point.x + point.half_width - 3;
        if (index === 0) ctx.moveTo(x_pos, point.y);
        else ctx.lineTo(x_pos, point.y + 0.4);
    });
    ctx.stroke();

    // 울퉁불퉁한 섹터에는 노면 표시를 얇게 추가
    for (let sample_index = 10; sample_index < samples.length - 1; sample_index += 5) {
        const point = samples[sample_index];
        if (get_sector_index(point.world) === 2 && point.depth > 0.36) {
            ctx.strokeStyle = "rgba(255,220,135,0.35)";
            ctx.lineWidth = 1 + point.depth * 2;
            ctx.beginPath();
            ctx.moveTo(point.x - point.half_width * 0.58, point.y - point.shape.bump * point.depth * 7);
            ctx.lineTo(point.x + point.half_width * 0.58, point.y - point.shape.bump * point.depth * 7);
            ctx.stroke();
        }
    }
}

function draw_track_sign() {
    const sector_index = get_sector_index(distance_travelled);
    const sector_info = game_config.track_sectors[sector_index];
    ctx.fillStyle = "rgba(5,12,24,0.72)";
    ctx.fillRect(18, 18, 245, 62);
    ctx.fillStyle = "#69e4ff";
    ctx.font = "bold 18px Arial";
    ctx.fillText(sector_info.name, 32, 43);
    ctx.fillStyle = "#ffffff";
    ctx.font = "14px Arial";
    ctx.fillText(sector_info.type, 32, 65);
}

function draw_hazard(hazard) {
    if (hazard.resolved) return;
    const point = project_track(hazard.distance);
    if (point.depth <= 0.015 || point.depth > 1.02) return;

    const object_x = point.x + hazard.lane * point.half_width * 0.76;
    const scale = 0.25 + point.depth * 0.9;
    const object_size = 12 + point.depth * 28;
    ctx.save();
    ctx.translate(object_x, point.y - 5 * scale);
    ctx.scale(scale, scale);

    if (hazard.kind === "cone") {
        ctx.fillStyle = "#ff8b38";
        ctx.beginPath();
        ctx.moveTo(0, -object_size);
        ctx.lineTo(-object_size * 0.55, object_size * 0.5);
        ctx.lineTo(object_size * 0.55, object_size * 0.5);
        ctx.closePath();
        ctx.fill();
        ctx.fillStyle = "#fff4dc";
        ctx.fillRect(-object_size * 0.32, 2, object_size * 0.64, 4);
    } else if (hazard.kind === "barrier") {
        ctx.fillStyle = "#f04c5c";
        ctx.fillRect(-object_size, -object_size * 0.42, object_size * 2, object_size * 0.9);
        ctx.strokeStyle = "#fff2e8";
        ctx.lineWidth = 5;
        ctx.beginPath();
        ctx.moveTo(-object_size * 0.72, object_size * 0.35);
        ctx.lineTo(-object_size * 0.25, -object_size * 0.35);
        ctx.moveTo(0, object_size * 0.35);
        ctx.lineTo(object_size * 0.47, -object_size * 0.35);
        ctx.stroke();
    } else if (hazard.kind === "oil") {
        ctx.fillStyle = "rgba(16,20,42,0.94)";
        ctx.beginPath();
        ctx.ellipse(0, 0, object_size * 1.2, object_size * 0.47, -0.12, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = "rgba(142,100,255,0.75)";
        ctx.lineWidth = 3;
        ctx.stroke();
    } else if (hazard.kind === "boost") {
        ctx.fillStyle = "rgba(15,215,255,0.25)";
        ctx.fillRect(-object_size * 1.25, -object_size * 0.18, object_size * 2.5, object_size * 0.65);
        ctx.strokeStyle = "#5ffff0";
        ctx.lineWidth = 4;
        for (let arrow_index = -1; arrow_index <= 1; arrow_index++) {
            ctx.beginPath();
            ctx.moveTo(arrow_index * object_size * 0.55 - 5, object_size * 0.28);
            ctx.lineTo(arrow_index * object_size * 0.55 + 3, -object_size * 0.02);
            ctx.lineTo(arrow_index * object_size * 0.55 + 11, object_size * 0.28);
            ctx.stroke();
        }
    }
    ctx.restore();
}

function draw_hazards() {
    // 먼 장애물부터 가까운 장애물 순서로 그려 원근감을 유지
    const visible_hazards = hazards.filter(function(hazard) {
        const relative_distance = hazard.distance - distance_travelled;
        return !hazard.resolved && relative_distance >= 0 && relative_distance <= visible_distance;
    }).sort(function(first, second) {
        return second.distance - first.distance;
    });
    visible_hazards.forEach(draw_hazard);
}

function draw_car() {
    const road_point = project_track(distance_travelled);
    const car_x = road_point.x + player_position * road_point.half_width * 0.76;
    const car_y = canvas_height - 107 + camera_shake * 0.35;
    const boost_active = nitro_active_time > 0 || boost_time > 0 || drift_boost_time > 0;
    const body_gradient = ctx.createLinearGradient(-35, -42, 34, 40);
    body_gradient.addColorStop(0, boost_active ? "#e9fffb" : "#9af2ff");
    body_gradient.addColorStop(0.34, boost_active ? "#4dffe5" : "#16c5ed");
    body_gradient.addColorStop(1, "#08729f");

    ctx.save();
    ctx.translate(car_x, car_y);
    ctx.rotate(car_tilt);

    // 차체 아래 그림자와 바퀴를 먼저 그려 입체적인 층을 만듦
    ctx.fillStyle = "rgba(0,0,0,0.48)";
    ctx.beginPath();
    ctx.ellipse(0, 16, 59, 22, 0, 0, Math.PI * 2);
    ctx.fill();

    const wheel_positions = [
        [-29, -20], [29, -20], [-31, 25], [31, 25]
    ];
    wheel_positions.forEach(function(position, wheel_index) {
        const wheel_x = position[0];
        const wheel_y = position[1];
        ctx.fillStyle = "#080e16";
        ctx.beginPath();
        ctx.roundRect(wheel_x - 7, wheel_y - 13, 14, 27, 5);
        ctx.fill();
        ctx.strokeStyle = "#536477";
        ctx.lineWidth = 2;
        ctx.stroke();
        ctx.fillStyle = wheel_index < 2 ? "#8fa9bb" : "#526d82";
        ctx.beginPath();
        ctx.ellipse(wheel_x, wheel_y - 1, 3.1, 5.2, 0, 0, Math.PI * 2);
        ctx.fill();
    });

    // 후면 윙과 지지대
    ctx.fillStyle = "#101e31";
    ctx.fillRect(-37, 34, 74, 7);
    ctx.fillStyle = "#d7faff";
    ctx.fillRect(-31, 32, 62, 2);
    ctx.fillStyle = "#18334a";
    ctx.fillRect(-21, 26, 5, 10);
    ctx.fillRect(16, 26, 5, 10);

    // 좌우 사이드 포드와 중앙 차체를 연속된 실루엣으로 표현
    ctx.fillStyle = "#08678e";
    ctx.beginPath();
    ctx.moveTo(-22, -24); ctx.lineTo(-31, -14); ctx.lineTo(-30, 19);
    ctx.lineTo(-22, 31); ctx.lineTo(-13, 28); ctx.lineTo(-16, -22);
    ctx.closePath();
    ctx.fill();
    ctx.beginPath();
    ctx.moveTo(22, -24); ctx.lineTo(31, -14); ctx.lineTo(30, 19);
    ctx.lineTo(22, 31); ctx.lineTo(13, 28); ctx.lineTo(16, -22);
    ctx.closePath();
    ctx.fill();

    ctx.fillStyle = body_gradient;
    ctx.beginPath();
    ctx.moveTo(-12, -52);
    ctx.quadraticCurveTo(0, -58, 12, -52);
    ctx.lineTo(20, -35);
    ctx.lineTo(23, -12);
    ctx.lineTo(27, 16);
    ctx.quadraticCurveTo(25, 31, 15, 35);
    ctx.lineTo(-15, 35);
    ctx.quadraticCurveTo(-25, 31, -27, 16);
    ctx.lineTo(-23, -12);
    ctx.lineTo(-20, -35);
    ctx.closePath();
    ctx.fill();
    ctx.strokeStyle = "rgba(226,253,255,0.8)";
    ctx.lineWidth = 2;
    ctx.stroke();

    // 콕핏/윈드실드
    const glass_gradient = ctx.createLinearGradient(0, -39, 0, 2);
    glass_gradient.addColorStop(0, "#b9f7ff");
    glass_gradient.addColorStop(0.35, "#24617f");
    glass_gradient.addColorStop(1, "#10273e");
    ctx.fillStyle = glass_gradient;
    ctx.beginPath();
    ctx.moveTo(-12, -34); ctx.quadraticCurveTo(0, -43, 12, -34);
    ctx.lineTo(10, -9); ctx.quadraticCurveTo(0, -1, -10, -9);
    ctx.closePath();
    ctx.fill();
    ctx.strokeStyle = "rgba(215,250,255,0.8)";
    ctx.lineWidth = 1.5;
    ctx.stroke();

    // 중앙 레이싱 스트라이프와 사이드 디테일
    ctx.strokeStyle = "rgba(255,255,255,0.82)";
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(0, -48); ctx.lineTo(0, -16); ctx.lineTo(0, 24);
    ctx.stroke();
    ctx.fillStyle = "#06273b";
    ctx.fillRect(-21, 4, 5, 17);
    ctx.fillRect(16, 4, 5, 17);

    // 앞쪽 라이트와 뒤쪽 테일램프
    ctx.fillStyle = "#fff4bb";
    ctx.beginPath();
    ctx.ellipse(-14, -43, 4, 2.4, -0.35, 0, Math.PI * 2);
    ctx.ellipse(14, -43, 4, 2.4, 0.35, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = "#ff5367";
    ctx.fillRect(-17, 27, 8, 3);
    ctx.fillRect(9, 27, 8, 3);

    if (boost_active) {
        ctx.globalAlpha = 0.9;
        ctx.fillStyle = "#ffb34f";
        ctx.beginPath(); ctx.moveTo(-10, 39); ctx.lineTo(-5, 62 + Math.random() * 9); ctx.lineTo(0, 39); ctx.fill();
        ctx.beginPath(); ctx.moveTo(5, 39); ctx.lineTo(10, 60 + Math.random() * 10); ctx.lineTo(15, 39); ctx.fill();
        ctx.fillStyle = "#8efffa";
        ctx.beginPath(); ctx.arc(-7, 41, 3, 0, Math.PI * 2); ctx.arc(8, 41, 3, 0, Math.PI * 2); ctx.fill();
        ctx.globalAlpha = 1;
    }
    ctx.restore();
}

function draw_speed_effect() {
    if (car_speed < 65) return;
    const effect_strength = Math.min(1, car_speed / 210);
    ctx.strokeStyle = "rgba(210,241,255," + (0.08 + effect_strength * 0.18) + ")";
    ctx.lineWidth = 1.5 + effect_strength;
    for (let effect_index = 0; effect_index < 28; effect_index++) {
        const offset_x = (effect_index * 83 + race_time * (120 + car_speed * 1.6)) % canvas_width;
        const effect_x = offset_x;
        const effect_y = (effect_index * 47 + race_time * (180 + car_speed * 1.9)) % canvas_height;
        const streak_length = 10 + car_speed * 0.19;
        ctx.beginPath();
        ctx.moveTo(effect_x, effect_y);
        ctx.lineTo(effect_x, effect_y + streak_length);
        ctx.stroke();
    }
}

function draw_game() {
    ctx.save();
    if (camera_shake > 0) {
        ctx.translate((Math.random() - 0.5) * camera_shake, (Math.random() - 0.5) * camera_shake);
    }
    draw_background();
    draw_road();
    draw_hazards();
    draw_speed_effect();
    draw_track_sign();
    draw_car();
    ctx.restore();
}

function update_hud() {
    speed_value.textContent = Math.round(car_speed * 1.5) + " km/h";
    temp_value.textContent = battery_temp.toFixed(1) + "℃";
    time_value.textContent = race_time.toFixed(1) + "s";
    sector_value.textContent = (get_sector_index(distance_travelled) + 1) + " / 3";
    nitro_value.textContent = nitro_remaining > 0 ? "READY" : (nitro_active_time > 0 ? "BOOST" : "USED");
    score_value.textContent = String(score);
    drift_charge_value.textContent = drift_boost_time > 0 ? "BOOST!" : (drift_charge > 0.05 ? Math.round(Math.min(1, drift_charge / 0.75) * 100) + "%" : "READY");

    if (battery_temp < 40) temp_value.style.color = "#78bdff";
    else if (battery_temp <= 80) temp_value.style.color = "#5ce5a0";
    else temp_value.style.color = "#ff626c";
}

function save_sector_record(sector_index) {
    const sector_info = game_config.track_sectors[sector_index];
    sector_records.push({
        name: sector_info.name,
        type: sector_info.type,
        time: (race_time - current_sector_start_time).toFixed(2),
        temperature: battery_temp.toFixed(1)
    });
    current_sector_start_time = race_time;
}

function classify_temperature() {
    if (battery_temp < 40) return "과냉각";
    else if (battery_temp <= 80) return "적합";
    else return "과열";
}

function calculate_grade() {
    if (race_time <= 32) return "S";
    else if (race_time <= 42) return "A";
    else return "B";
}

function finish_race(overheated) {
    if (race_finished) return;
    race_finished = true;
    race_running = false;
    if (engine_gain && audio_context) engine_gain.gain.setTargetAtTime(0.0001, audio_context.currentTime, 0.1);
    update_music_mix();

    const temperature_status = classify_temperature();
    const grade = overheated ? "FAIL" : calculate_grade();
    document.getElementById("result_kicker").textContent = overheated ? "BATTERY OVERHEAT" : "RACE COMPLETE";
    document.getElementById("result_grade").textContent = grade;
    document.getElementById("result_status").textContent = temperature_status;
    document.getElementById("result_temp").textContent = battery_temp.toFixed(1) + "℃";
    document.getElementById("result_time").textContent = race_time.toFixed(2) + "초";
    document.getElementById("result_coolant").textContent = game_config.coolant;

    let description = "";
    if (temperature_status === "과냉각") description = "배터리 온도가 기준보다 낮습니다. 냉각 조건을 다시 조정해 보세요.";
    else if (temperature_status === "적합") description = "배터리 온도가 적정 범위에 있습니다. 냉각 시스템 관리 성공!";
    else description = "배터리 온도가 기준을 초과했습니다. 냉각 성능을 높여 보세요.";
    if (overheated) description = "배터리 온도가 100℃를 넘어 레이스가 중단되었습니다.";
    document.getElementById("result_description").textContent = description;

    let sector_html = "";
    for (let record_index = 0; record_index < sector_records.length; record_index++) {
        const record = sector_records[record_index];
        sector_html += '<div class="sector_result_row"><span><b>' + record.name + '</b> · ' + record.type + '<br>온도 ' + record.temperature + '℃</span><b>' + record.time + '초</b></div>';
    }
    document.getElementById("sector_results").innerHTML = sector_html;
    document.getElementById("result_score").textContent = String(score);
    document.getElementById("result_avoided").textContent = passed_hazards + "개";
    result_overlay.style.display = "flex";
    game_message.textContent = "레이스 종료 — 결과를 확인하세요.";
    play_sfx(overheated ? "impact" : "finish");
}

function handle_hazard_collisions() {
    hazards.forEach(function(hazard) {
        if (hazard.resolved) return;
        const distance_gap = Math.abs(distance_travelled - hazard.distance);
        if (distance_travelled > hazard.distance + 42) {
            hazard.resolved = true;
            if (hazard.kind !== "boost") {
                passed_hazards += 1;
                score += 50;
            }
            return;
        }
        if (distance_gap > 18 || Math.abs(player_position - hazard.lane) > 0.31) return;

        hazard.resolved = true;
        if (hazard.kind === "boost") {
            score += 150;
            car_speed = Math.min(245, car_speed + 46);
            boost_time = 1.3;
            game_message.textContent = "BOOST PAD! 속도와 점수를 획득했습니다.";
            play_sfx("boost");
        } else if (hazard.kind === "oil") {
            score = Math.max(0, score - 30);
            slip_time = 1.7;
            slip_direction = player_position >= hazard.lane ? 1 : -1;
            car_speed = Math.max(35, car_speed - 32);
            camera_shake = 8;
            game_message.textContent = "OIL TRAP! 조향이 잠시 미끄러집니다.";
            play_sfx("oil");
        } else {
            const penalty = hazard.kind === "barrier" ? 78 : 48;
            car_speed = Math.max(25, car_speed - penalty);
            battery_temp += hazard.kind === "barrier" ? 2.5 : 1.2;
            score = Math.max(0, score - (hazard.kind === "barrier" ? 60 : 25));
            camera_shake = 10;
            game_message.textContent = hazard.kind === "barrier" ? "BARRIER 충돌! 속도가 크게 감소했습니다." : "CONE 충돌! 속도가 감소했습니다.";
            play_sfx("impact");
        }
    });
}

function update_physics(delta_time) {
    const accelerate = keys["w"] || keys["arrowup"];
    const brake = keys["s"] || keys["arrowdown"];
    const steer_left = keys["a"] || keys["arrowleft"];
    const steer_right = keys["d"] || keys["arrowright"];
    const drift_pressed = keys["shift"];

    // 드리프트 중 방향을 조절하면 게이지가 차고, SHIFT를 놓을 때 미니 부스트
    if (drift_pressed && Math.abs(steering_velocity) > 0.2 && car_speed > 55) {
        drift_charge = Math.min(0.95, drift_charge + delta_time);
    }
    if (drift_was_pressed && !drift_pressed) {
        if (drift_charge >= 0.48) {
            drift_boost_time = Math.min(1.25, 0.55 + drift_charge * 0.55);
            car_speed = Math.min(245, car_speed + 22);
            score += 70;
            game_message.textContent = "DRIFT BOOST! 코너 탈출 가속 성공!";
            play_sfx("boost");
        }
        drift_charge = 0;
    }
    drift_was_pressed = drift_pressed;

    // 가속 반응을 높이고, 키를 놓으면 관성으로 속도가 서서히 줄어듦
    if (accelerate) car_speed += 158 * delta_time;
    else car_speed -= 17 * delta_time;
    if (brake) car_speed -= 185 * delta_time;

    if (keys[" "] && nitro_remaining > 0 && nitro_active_time <= 0) {
        nitro_active_time = 2.0;
        nitro_remaining = 0;
        play_sfx("boost");
    }
    if (nitro_active_time > 0) {
        car_speed += 82 * delta_time;
        nitro_active_time = Math.max(0, nitro_active_time - delta_time);
    }
    if (drift_boost_time > 0) {
        car_speed += 54 * delta_time;
        drift_boost_time = Math.max(0, drift_boost_time - delta_time);
    }
    boost_time = Math.max(0, boost_time - delta_time);
    const speed_limit = nitro_active_time > 0 || boost_time > 0 || drift_boost_time > 0 ? 250 : 230;
    car_speed = Math.max(0, Math.min(speed_limit, car_speed));

    let steering_input = 0;
    if (steer_left) steering_input -= 1;
    if (steer_right) steering_input += 1;
    if (slip_time > 0) {
        steering_input *= -0.42;
        player_position += slip_direction * 0.28 * delta_time;
        slip_time = Math.max(0, slip_time - delta_time);
    }

    const steering_response = drift_pressed ? 4.6 : 3.3;
    steering_velocity += (steering_input * steering_response - steering_velocity * 2.35) * delta_time;
    const speed_factor = 0.3 + car_speed / 230 * 0.95;
    player_position += steering_velocity * speed_factor * delta_time;
    player_position = Math.max(-1.15, Math.min(1.15, player_position));

    const current_shape = get_track_shape(distance_travelled);
    road_curve += (current_shape.curve - road_curve) * Math.min(1, delta_time * 2.8);
    const target_tilt = -steering_velocity * 0.12 - road_curve * 0.1;
    car_tilt += (target_tilt - car_tilt) * Math.min(1, delta_time * 5.5);

    if (Math.abs(player_position) > 0.9) {
        car_speed = Math.max(25, car_speed - 62 * delta_time);
        game_message.textContent = "TRACK LIMIT! 도로 안쪽으로 복귀하세요.";
    } else if (drift_pressed && Math.abs(steering_velocity) > 0.2) {
        game_message.textContent = "DRIFTING!";
    } else if (nitro_active_time > 0 || boost_time > 0 || drift_boost_time > 0) {
        game_message.textContent = "BOOST!";
    } else if (slip_time > 0) {
        game_message.textContent = "미끄러운 노면! 조향을 조절하세요.";
    } else if (accelerate) {
        game_message.textContent = "가속 중 — 장애물을 피하세요!";
    } else {
        game_message.textContent = "장애물을 피해 안정적으로 주행하세요.";
    }

    distance_travelled += car_speed * 0.58 * delta_time;
    race_time += delta_time;
    handle_hazard_collisions();

    const updated_shape = get_track_shape(distance_travelled);
    if (get_sector_index(distance_travelled) === 2) {
        camera_shake = Math.max(camera_shake * 0.72, Math.abs(updated_shape.bump) * Math.min(7, car_speed / 32));
        car_tilt += updated_shape.bump * 0.0025;
    } else {
        camera_shake *= 0.78;
    }

    const heat_rate = (game_config.battery_output / 100) * (0.65 + car_speed / 230 * 0.75);
    const cooling_rate = game_config.flow_rate * 0.08 * game_config.cooling_efficiency;
    battery_temp += (heat_rate - cooling_rate) * delta_time;

    const next_sector = get_sector_index(distance_travelled);
    if (next_sector > current_sector) {
        save_sector_record(current_sector);
        current_sector = next_sector;
        score += 100;
        play_sfx("sector");
        game_message.textContent = "SECTOR " + (current_sector + 1) + " 진입! 새로운 코스가 시작됩니다.";
    }

    if (battery_temp > 100) {
        finish_race(true);
        return;
    }

    if (distance_travelled >= total_distance) {
        if (sector_records.length < 3) save_sector_record(2);
        score += Math.max(0, Math.round((230 - race_time) * 2));
        finish_race(false);
    }

    update_engine_audio();
}

function game_loop(timestamp) {
    if (!race_running) return;
    if (last_frame_time === 0) last_frame_time = timestamp;
    const delta_time = Math.min((timestamp - last_frame_time) / 1000, 0.035);
    last_frame_time = timestamp;
    update_physics(delta_time);
    draw_game();
    update_hud();
    if (race_running) requestAnimationFrame(game_loop);
}

function start_race() {
    choose_random_theme();
    init_audio();
    if (audio_context && audio_context.state === "suspended") audio_context.resume();

    race_running = true;
    race_finished = false;
    last_frame_time = 0;
    race_time = 0;
    distance_travelled = 0;
    car_speed = 0;
    player_position = 0;
    steering_velocity = 0;
    car_tilt = 0;
    battery_temp = game_config.initial_temperature;
    nitro_remaining = 1;
    nitro_active_time = 0;
    boost_time = 0;
    drift_charge = 0;
    drift_boost_time = 0;
    drift_was_pressed = false;
    slip_time = 0;
    slip_direction = 0;
    camera_shake = 0;
    road_curve = 0;
    score = 0;
    passed_hazards = 0;
    sector_records = [];
    current_sector = 0;
    current_sector_start_time = 0;
    keys = {};
    make_hazards();

    start_overlay.style.display = "none";
    result_overlay.style.display = "none";
    if (music_enabled) start_background_music();
    update_music_mix();
    canvas.focus();
    draw_game();
    update_hud();
    game_message.textContent = "레이스 시작! 장애물을 피하고 부스트 패드를 노리세요.";
    requestAnimationFrame(game_loop);
}

window.addEventListener("keydown", function(event) {
    const key_name = event.key.toLowerCase();
    if (["arrowup", "arrowdown", "arrowleft", "arrowright", " "].includes(key_name)) event.preventDefault();
    keys[key_name] = true;
});

window.addEventListener("keyup", function(event) {
    keys[event.key.toLowerCase()] = false;
});

window.addEventListener("blur", function() {
    for (const key_name in keys) keys[key_name] = false;
    drift_was_pressed = false;
    drift_charge = 0;
});

sound_button.addEventListener("click", function() {
    sound_enabled = !sound_enabled;
    sound_button.textContent = sound_enabled ? "SFX: ON" : "SFX: OFF";
    if (sound_enabled) {
        init_audio();
        if (audio_context && audio_context.state === "suspended") audio_context.resume();
        if (master_gain && audio_context) master_gain.gain.setTargetAtTime(0.62, audio_context.currentTime, 0.08);
        play_sfx("sector");
    } else if (master_gain && audio_context) {
        master_gain.gain.setTargetAtTime(0, audio_context.currentTime, 0.08);
    }
});

music_button.addEventListener("click", function() {
    music_enabled = !music_enabled;
    music_button.textContent = music_enabled ? "MUSIC: ON" : "MUSIC: OFF";
    if (music_enabled) {
        init_audio();
        start_background_music();
        update_music_mix();
    } else {
        stop_background_music();
    }
});

music_volume_slider.addEventListener("input", function() {
    music_volume = Number(music_volume_slider.value) / 100 * 0.45;
    update_music_mix();
});

document.getElementById("start_button").addEventListener("click", start_race);
document.getElementById("restart_button").addEventListener("click", start_race);

choose_random_theme();
make_hazards();
draw_game();
update_hud();
</script>

</body>
</html>
"""

game_html = game_html.replace(
    "__CONFIG__",
    json.dumps(game_config, ensure_ascii=False)
)

components.html(
    game_html,
    height=900,
    scrolling=False
)
