import re
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import NullFormatter
from itertools import chain

TIME_RE = re.compile(r"^\d{2}:\d{2}-\d{2}:\d{2}$")


def parse_table_with_time(text: str, col_names: list[str]):
    lines = [ln.strip() for ln in text.strip().splitlines() if ln.strip()]
    times = []
    cols = {k: [] for k in col_names}
    for ln in lines:
        parts = re.split(r"\s+|\t+", ln.strip())
        time_idx = None
        for i, p in enumerate(parts):
            if TIME_RE.match(p):
                time_idx = i
                break
        if time_idx is None:
            continue
        values = parts[time_idx + 1 :]
        if len(values) < len(col_names):
            raise ValueError(f"Row has too few numeric columns: {ln}")
        values = values[-len(col_names) :]
        times.append(parts[time_idx])
        for k, v in zip(col_names, values):
            cols[k].append(float(v.replace(",", ".")))
    return times, cols


PV_PROFILE_DATA = r"""
PV generation profile	Sweeping SRE	Simultaneous SRE	Dynamic SRE
1	1	00:00-00:15	0.00	10.31	0.00	3.05
2	1	00:15-00:30	0.00	10.31	0.00	2.89
3	1	00:30-00:45	0.00	10.31	0.00	2.78
4	1	00:45-01:00	0.00	10.31	0.00	2.66
5	2	01:00-01:15	0.00	10.31	0.00	2.23
6	2	01:15-01:30	0.00	10.31	0.00	2.16
7	2	01:30-01:45	0.00	10.31	0.00	2.10
8	2	01:45-02:00	0.00	10.31	0.00	2.05
9	3	02:00-02:15	0.00	10.31	0.00	2.26
10	3	02:15-02:30	0.00	10.31	0.00	2.23
11	3	02:30-02:45	0.00	10.31	0.00	2.21
12	3	02:45-03:00	0.00	10.31	0.00	2.19
13	4	03:00-03:15	0.00	10.31	0.00	1.94
14	4	03:15-03:30	0.00	10.31	0.00	1.93
15	4	03:30-03:45	0.00	10.31	0.00	1.93
16	4	03:45-04:00	0.00	10.31	0.00	1.92
17	5	04:00-04:15	0.00	10.31	0.00	1.86
18	5	04:15-04:30	0.00	10.31	0.00	1.88
19	5	04:30-04:45	0.00	10.31	0.00	1.90
20	5	04:45-05:00	0.00	10.31	0.00	1.93
21	6	05:00-05:15	0.01	10.31	0.00	2.19
22	6	05:15-05:30	0.07	10.31	0.02	2.19
23	6	05:30-05:45	0.38	10.31	0.13	2.18
24	6	05:45-06:00	1.46	10.31	0.48	2.05
25	7	06:00-06:15	2.93	10.31	0.97	1.01
26	7	06:15-06:30	4.56	10.31	1.51	1.28
27	7	06:30-06:45	6.58	10.31	2.17	1.69
28	7	06:45-07:00	9.36	10.31	3.09	2.34
29	8	07:00-07:15	12.94	10.31	4.27	3.90
30	8	07:15-07:30	17.38	10.31	5.74	5.23
31	8	07:30-07:45	22.37	10.31	7.38	6.74
32	8	07:45-08:00	27.66	10.31	9.13	8.33
33	9	08:00-08:15	32.94	10.31	10.87	9.92
34	9	08:15-08:30	38.34	10.31	12.65	11.55
35	9	08:30-08:45	43.59	10.31	14.38	13.13
36	9	08:45-09:00	48.65	10.31	16.05	14.65
37	10	09:00-09:15	53.95	10.31	17.80	16.25
38	10	09:15-09:30	58.61	10.31	19.34	17.65
39	10	09:30-09:45	62.93	10.31	20.77	18.95
40	10	09:45-10:00	66.70	10.31	22.01	20.09
41	11	10:00-10:15	70.08	10.31	23.13	21.10
42	11	10:15-10:30	73.58	10.31	24.28	22.16
43	11	10:30-10:45	75.92	10.31	25.05	22.86
44	11	10:45-11:00	77.75	10.31	25.66	23.41
45	12	11:00-11:15	79.59	10.31	26.27	23.97
46	12	11:15-11:30	80.94	10.31	26.71	24.37
47	12	11:30-11:45	81.93	10.31	27.04	24.67
48	12	11:45-12:00	82.46	10.31	27.21	24.83
49	13	12:00-12:15	82.64	10.31	27.27	24.88
50	13	12:15-12:30	82.57	10.31	27.25	24.87
51	13	12:30-12:45	82.52	10.31	27.23	24.85
52	13	12:45-13:00	81.79	10.31	26.99	24.63
53	14	13:00-13:15	81.54	10.31	26.91	24.55
54	14	13:15-13:30	81.25	10.31	26.81	24.47
55	14	13:30-13:45	80.82	10.31	26.67	24.34
56	14	13:45-14:00	80.44	10.31	26.55	24.22
57	15	14:00-14:15	79.68	10.31	26.29	23.99
58	15	14:15-14:30	80.22	10.31	26.47	24.16
59	15	14:30-14:45	77.44	10.31	25.55	23.32
60	15	14:45-15:00	76.05	10.31	25.09	22.90
61	16	15:00-15:15	74.45	10.31	24.57	22.42
62	16	15:15-15:30	72.55	10.31	23.94	21.85
63	16	15:30-15:45	70.74	10.31	23.34	21.30
64	16	15:45-16:00	68.59	10.31	22.63	20.65
65	17	16:00-16:15	66.54	10.31	21.96	20.04
66	17	16:15-16:30	63.76	10.31	21.04	19.20
67	17	16:30-16:45	60.43	10.31	19.94	18.20
68	17	16:45-17:00	56.79	10.31	18.74	17.10
69	18	17:00-17:15	52.91	10.31	17.46	15.93
70	18	17:15-17:30	48.95	10.31	16.15	14.74
71	18	17:30-17:45	45.01	10.31	14.85	13.55
72	18	17:45-18:00	41.08	10.31	13.56	12.37
73	19	18:00-18:15	36.24	10.31	11.96	10.01
74	19	18:15-18:30	31.59	10.31	10.43	8.62
75	19	18:30-18:45	26.71	10.31	8.81	7.17
76	19	18:45-19:00	22.01	10.31	7.26	5.80
77	20	19:00-19:15	17.56	10.31	5.80	4.39
78	20	19:15-19:30	13.56	10.31	4.48	3.46
79	20	19:30-19:45	10.26	10.31	3.38	2.78
80	20	19:45-20:00	7.69	10.31	2.54	2.35
81	21	20:00-20:15	5.47	10.31	1.80	3.47
82	21	20:15-20:30	3.55	10.31	1.17	3.51
83	21	20:30-20:45	1.92	10.31	0.63	3.64
84	21	20:45-21:00	0.79	10.31	0.26	3.82
85	22	21:00-21:15	0.22	10.31	0.07	2.75
86	22	21:15-21:30	0.02	10.31	0.01	2.75
87	22	21:30-21:45	0.00	10.31	0.00	2.75
88	22	21:45-22:00	0.00	10.31	0.00	2.77
89	23	22:00-22:15	0.00	10.31	0.00	2.95
90	23	22:15-22:30	0.00	10.31	0.00	2.84
91	23	22:30-22:45	0.00	10.31	0.00	2.71
92	23	22:45-23:00	0.00	10.31	0.00	2.56
93	24	23:00-23:15	0.00	10.31	0.00	2.08
94	24	23:15-23:30	0.00	10.31	0.00	1.96
95	24	23:30-23:45	0.00	10.31	0.00	1.85
96	24	23:45-00:00	0.00	10.31	0.00	1.76
"""

HOUSEHOLD_LOAD_DATA = r"""
Reference household load	Sweeping SRE	Simultaneous SRE	Dynamic SRE
00:00-00:15	25.98	36.29	25.98	29.02
00:15-00:30	24.63	34.94	24.63	27.52
00:30-00:45	23.68	33.99	23.68	26.46
00:45-01:00	22.71	33.02	22.71	25.38
01:00-01:15	21.99	32.31	21.99	24.23
01:15-01:30	21.29	31.60	21.29	23.45
01:30-01:45	20.65	30.96	20.65	22.74
01:45-02:00	20.19	30.50	20.19	22.24
02:00-02:15	19.91	30.23	19.91	22.17
02:15-02:30	19.68	29.99	19.68	21.91
02:30-02:45	19.48	29.79	19.48	21.69
02:45-03:00	19.34	29.65	19.34	21.53
03:00-03:15	19.36	29.67	19.36	21.30
03:15-03:30	19.24	29.56	19.24	21.17
03:30-03:45	19.20	29.52	19.20	21.13
03:45-04:00	19.18	29.49	19.18	21.10
04:00-04:15	19.54	29.85	19.54	21.39
04:15-04:30	19.75	30.06	19.75	21.62
04:30-04:45	20.03	30.35	20.03	21.94
04:45-05:00	20.31	30.62	20.31	22.24
05:00-05:15	21.14	31.45	21.14	23.33
05:15-05:30	21.33	31.65	21.36	23.52
05:30-05:45	22.07	32.38	22.19	24.25
05:45-06:00	22.63	32.94	23.11	24.68
06:00-06:15	24.42	34.73	25.38	25.43
06:15-06:30	25.43	35.74	26.94	26.71
06:30-06:45	26.21	36.52	28.38	27.90
06:45-07:00	26.89	37.20	29.97	29.22
07:00-07:15	27.68	38.00	31.95	31.58
07:15-07:30	28.16	38.48	33.90	33.40
07:30-07:45	28.38	38.69	35.76	35.12
07:45-08:00	28.22	38.54	37.35	36.55
08:00-08:15	28.02	38.33	38.89	37.94
08:15-08:30	28.11	38.42	40.76	39.66
08:30-08:45	28.09	38.40	42.47	41.21
08:45-09:00	28.10	38.41	44.15	42.75
09:00-09:15	28.31	38.62	46.11	44.55
09:15-09:30	28.45	38.76	47.79	46.10
09:30-09:45	28.43	38.74	49.19	47.38
09:45-10:00	28.34	38.66	50.36	48.43
10:00-10:15	28.35	38.66	51.48	49.46
10:15-10:30	28.65	38.97	52.93	50.81
10:30-10:45	29.06	39.37	54.11	51.92
10:45-11:00	29.47	39.79	55.13	52.88
11:00-11:15	30.30	40.61	56.57	54.27
11:15-11:30	31.30	41.61	58.01	55.67
11:30-11:45	32.14	42.45	59.18	56.81
11:45-12:00	32.59	42.91	59.81	57.42
12:00-12:15	33.04	43.35	60.31	57.92
12:15-12:30	33.04	43.36	60.29	57.91
12:30-12:45	32.73	43.04	59.96	57.58
12:45-13:00	32.49	42.80	59.48	57.11
13:00-13:15	32.16	42.48	59.07	56.72
13:15-13:30	31.90	42.21	58.71	56.36
13:30-13:45	31.51	41.82	58.18	55.85
13:45-14:00	31.24	41.56	57.79	55.47
14:00-14:15	30.92	41.24	57.22	54.92
14:15-14:30	30.80	41.12	57.28	54.96
14:30-14:45	30.46	40.78	56.02	53.78
14:45-15:00	30.49	40.80	55.59	53.39
15:00-15:15	30.66	40.97	55.23	53.08
15:15-15:30	30.70	41.02	54.64	52.55
15:30-15:45	30.83	41.14	54.17	52.13
15:45-16:00	31.14	41.45	53.77	51.79
16:00-16:15	31.86	42.18	53.82	51.90
16:15-16:30	32.48	42.79	53.52	51.68
16:30-16:45	33.25	43.56	53.19	51.45
16:45-17:00	34.26	44.57	53.00	51.36
17:00-17:15	35.51	45.82	52.97	51.44
17:15-17:30	36.88	47.19	53.03	51.62
17:30-17:45	38.03	48.34	52.88	51.58
17:45-18:00	39.26	49.58	52.82	51.63
18:00-18:15	40.52	50.83	52.48	50.53
18:15-18:30	41.54	51.85	51.96	50.16
18:30-18:45	42.49	52.80	51.30	49.66
18:45-19:00	43.20	53.51	50.46	49.00
19:00-19:15	43.35	53.66	49.14	47.73
19:15-19:30	43.45	53.76	47.93	46.91
19:30-19:45	43.44	53.75	46.82	46.22
19:45-20:00	43.38	53.69	45.91	45.72
20:00-20:15	43.08	53.39	44.88	46.55
20:15-20:30	42.52	52.83	43.69	46.03
20:30-20:45	41.91	52.22	42.54	45.55
20:45-21:00	41.39	51.71	41.65	45.21
21:00-21:15	40.90	51.21	40.97	43.64
21:15-21:30	40.17	50.48	40.18	42.92
21:30-21:45	39.98	50.30	39.98	42.73
21:45-22:00	40.33	50.64	40.33	43.10
22:00-22:15	40.16	50.47	40.16	43.10
22:15-22:30	38.63	48.94	38.63	41.46
22:30-22:45	36.89	47.20	36.89	39.59
22:45-23:00	34.92	45.23	34.92	37.48
23:00-23:15	32.93	43.24	32.93	35.01
23:15-23:30	31.00	41.31	31.00	32.95
23:30-23:45	29.40	39.71	29.40	31.25
23:45-00:00	27.89	38.20	27.89	29.65
"""

pv_cols = ["PV generation profile", "Sweeping SRE", "Simultaneous SRE", "Dynamic SRE"]
hh_cols = ["Reference household load", "Sweeping SRE", "Simultaneous SRE", "Dynamic SRE"]

pv_time, pv = parse_table_with_time(PV_PROFILE_DATA, pv_cols)
hh_time, hh = parse_table_with_time(HOUSEHOLD_LOAD_DATA, hh_cols)

if len(pv_time) != len(hh_time):
    raise ValueError("PV and household tables have different lengths.")
if len(pv_time) == 0:
    raise ValueError("No profile rows parsed. Did you paste the PV/HOUSEHOLD tables correctly?")

n = len(pv_time)
x = list(range(n))

years = [2030, 2035, 2040, 2045, 2050]
ref_demand = [4469.86, 5242.57, 6057.14, 6791.00, 7316.72]
high_swe_total_demand = [4543.33, 5457.20, 6358.92, 7096.05, 7689.97]

sre_demand = {
    "Low scenario (7.7% SRE)": {"DYN": [23.21, 47.33, 61.74, 69.66, 80.78], "SIM": [19.47, 39.21, 49.51, 55.18, 63.09], "SWE": [19.47, 38.70, 49.07, 54.82, 62.12]},
    "Average scenario (17.2% SRE)": {"DYN": [46.55, 95.82, 123.45, 138.75, 160.66], "SIM": [43.50, 88.88, 112.93, 126.29, 145.52], "SWE": [43.50, 87.16, 111.27, 124.47, 140.84]},
    "High scenario (33% SRE)": {"DYN": [85.92, 182.38, 237.70, 272.04, 314.93], "SIM": [83.45, 176.70, 228.42, 260.37, 301.94], "SWE": [83.45, 169.36, 218.02, 247.17, 276.34]},
}

sre_total_demand = {
    "LOW_DYN": [4496.71, 5291.91, 6123.12, 6843.85, 7401.65],
    "LOW_SIM": [4493.92, 5281.69, 6100.03, 6830.50, 7373.80],
    "LOW_SWE": [4483.18, 5288.49, 6121.96, 6855.17, 7398.46],
    "AVG_DYN": [4520.06, 5328.42, 6165.30, 6907.01, 7456.11],
    "AVG_SIM": [4515.11, 5315.30, 6147.60, 6894.02, 7438.07],
    "AVG_SWE": [4506.36, 5351.23, 6200.72, 6949.83, 7502.34],
    "HIGH_DYN": [4557.01, 5390.67, 6254.65, 7042.96, 7614.79],
    "HIGH_SIM": [4557.02, 5380.47, 6239.56, 7032.32, 7593.35],
}

sre_costs_additional = {
    "Low scenario (7.7% SRE)": {"DYN": [1.48, 4.41, 8.43, 13.24, 18.65], "SIM": [1.10, 3.22, 6.01, 9.10, 12.69], "SWE": [1.55, 4.51, 8.38, 13.15, 18.29]},
    "Average scenario (17.2% SRE)": {"DYN": [3.13, 9.30, 17.41, 26.58, 37.26], "SIM": [2.81, 8.25, 15.21, 22.89, 31.90], "SWE": [3.48, 10.24, 19.17, 30.08, 42.06]},
    "High scenario (33% SRE)": {"DYN": [6.40, 19.17, 36.11, 54.98, 77.18], "SIM": [6.10, 18.22, 34.08, 51.55, 72.31], "SWE": [6.70, 20.02, 37.77, 59.36, 82.87]},
}

ref_cost = [411.138, 465.042, 487.826, 526.795, 554.718]
high_swe_total_cost = [417.839, 478.364, 505.574, 548.385, 578.225]

abs_totals_cost = {
    "LOW_DYN": [412.613, 467.974, 491.849, 531.607, 560.125],
    "LOW_SIM": [412.241, 467.157, 490.614, 529.892, 558.307],
    "LOW_SWE": [412.687, 468.000, 491.699, 531.560, 559.864],
    "AVG_DYN": [414.269, 471.210, 495.933, 535.968, 565.394],
    "AVG_SIM": [413.948, 470.485, 494.787, 534.467, 563.731],
    "AVG_SWE": [414.613, 471.803, 496.758, 537.711, 566.695],
    "HIGH_DYN": [417.542, 477.805, 504.764, 545.667, 576.917],
    "HIGH_SIM": [417.239, 477.163, 503.680, 544.272, 575.473],
}

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Open Sans", "DejaVu Sans", "Arial"]

colors = {"DYN": "#E18B6B", "SIM": "#78B43D", "SWE": "#5B84B1"}
linestyles = {"DYN": "-", "SIM": ":", "SWE": (0, (8, 3))}
markers = {"DYN": "o", "SIM": "o", "SWE": "o"}
scenario_labels = {"DYN": "Dynamic", "SIM": "Simultaneous", "SWE": "Sweeping"}

pv_color = "#666666"
ref_color = "#666666"

fig = plt.figure(figsize=(22, 13))
gs = fig.add_gridspec(3, 4, height_ratios=[1.10, 1.55, 1.55], wspace=0.22, hspace=0.35)

ax_pv = fig.add_subplot(gs[0, 0:2])
ax_hh = fig.add_subplot(gs[0, 2:4])
ax_d0 = fig.add_subplot(gs[1, 0])
ax_d1 = fig.add_subplot(gs[1, 1])
ax_d2 = fig.add_subplot(gs[1, 2])
ax_d3 = fig.add_subplot(gs[1, 3])
ax_c0 = fig.add_subplot(gs[2, 0])
ax_c1 = fig.add_subplot(gs[2, 1])
ax_c2 = fig.add_subplot(gs[2, 2])
ax_c3 = fig.add_subplot(gs[2, 3])

ax_pv.plot(x, pv["PV generation profile"], color=pv_color, linewidth=3, label="PV generation profile (typical day)")
ax_pv.plot(x, pv["Sweeping SRE"], color=colors["SWE"], linestyle=linestyles["SWE"], linewidth=2)
ax_pv.plot(x, pv["Simultaneous SRE"], color=colors["SIM"], linestyle=linestyles["SIM"], linewidth=2)
ax_pv.plot(x, pv["Dynamic SRE"], color=colors["DYN"], linestyle=linestyles["DYN"], linewidth=2)
ax_pv.set_xlim(0, n - 1)
ax_pv.set_xlabel("time", fontsize=11)
ax_pv.set_ylabel("generation or demand", fontsize=11)
ax_pv.tick_params(axis="x", which="both", labelbottom=False)
ax_pv.tick_params(axis="y", labelleft=False)
ax_pv.legend(frameon=False, loc="upper left", fontsize=9)

ax_hh.plot(x, hh["Reference household load"], color=ref_color, linewidth=3, label="Reference household load (typical weekday)")
ax_hh.plot(x, hh["Sweeping SRE"], color=colors["SWE"], linestyle=linestyles["SWE"], linewidth=2)
ax_hh.plot(x, hh["Simultaneous SRE"], color=colors["SIM"], linestyle=linestyles["SIM"], linewidth=2)
ax_hh.plot(x, hh["Dynamic SRE"], color=colors["DYN"], linestyle=linestyles["DYN"], linewidth=2)
ax_hh.set_xlim(0, n - 1)
ax_hh.set_xlabel("time", fontsize=11)
ax_hh.set_ylabel("generation or demand", fontsize=11)
ax_hh.tick_params(axis="x", which="both", labelbottom=False)
ax_hh.tick_params(axis="y", labelleft=False)
ax_hh.legend(frameon=False, loc="upper left", fontsize=9)

ax_d0.plot(years, ref_demand, label="Reference", color=ref_color, linestyle="-", marker="o", linewidth=2, markersize=5)
ax_d0.plot(years, high_swe_total_demand, label="Maximum SRE", color=colors["SWE"], linestyle=linestyles["SWE"], marker="o", linewidth=2, markersize=5)

for key, values in sre_total_demand.items():
    c = colors["DYN"] if "DYN" in key else colors["SIM"] if "SIM" in key else colors["SWE"]
    ax_d0.plot(years, values, linestyle="None", marker="o", color=c, markersize=4, alpha=0.9)

pct_inc_d = [(h - r) / r * 100 for r, h in zip(ref_demand, high_swe_total_demand)]
ymin, ymax = ax_d0.get_ylim()
y_offset = 0.015 * (ymax - ymin)
for x_year, y_val, p in zip(years, high_swe_total_demand, pct_inc_d):
    ax_d0.text(x_year, y_val + y_offset, f"+{p:.1f}%", ha="center", va="bottom", fontsize=10, fontweight="bold", color=colors["SWE"], clip_on=False)

ax_d0.set_title("Overall view: demand", fontsize=12, fontweight="normal")
ax_d0.set_ylabel("Total electricity demand [TWh/yr]", fontsize=12)
ax_d0.set_xticks(years)
ax_d0.legend(frameon=False, loc="upper left")

demand_titles = ["Low scenario (7.7% SRE)", "Average scenario (17.2% SRE)", "High scenario (33% SRE)"]
demand_axes = [ax_d1, ax_d2, ax_d3]

for ax, title in zip(demand_axes, demand_titles):
    data = sre_demand[title]
    for scen in ["DYN", "SIM", "SWE"]:
        ax.plot(years, data[scen], color=colors[scen], linestyle=linestyles[scen], marker=markers[scen], markersize=5, linewidth=2)
    ax.set_title(title, fontsize=12, fontweight="normal")
    ax.set_xticks(years)

max_demand_add = max(max(chain.from_iterable(sre_demand[sc][k] for k in ["DYN", "SIM", "SWE"])) for sc in sre_demand)
ylim_d = (int(max_demand_add / 50) + 1) * 50
for ax in demand_axes:
    ax.set_ylim(0, ylim_d)

ax_d1.set_ylabel("Additional demand [TWh/yr]", fontsize=12, labelpad=2)
ax_d1.yaxis.set_label_coords(-0.0915, 0.5)
ax_d1.tick_params(axis="y", pad=2)
for ax in [ax_d2, ax_d3]:
    ax.tick_params(axis="y", which="major", left=True, labelleft=False)
    ax.yaxis.set_major_formatter(NullFormatter())
    ax.spines["left"].set_visible(True)

ax_c0.plot(years, ref_cost, label="Reference", color=ref_color, linestyle="-", marker="o", linewidth=2, markersize=5)
ax_c0.plot(years, high_swe_total_cost, label="Maximum SRE", color=colors["SWE"], linestyle=linestyles["SWE"], marker="o", linewidth=2, markersize=5)

for key, values in abs_totals_cost.items():
    c = colors["DYN"] if "DYN" in key else colors["SIM"] if "SIM" in key else colors["SWE"]
    ax_c0.plot(years, values, linestyle="None", marker="o", color=c, markersize=4, alpha=0.9)

pct_inc_c = [(h - r) / r * 100 for r, h in zip(ref_cost, high_swe_total_cost)]
ymin, ymax = ax_c0.get_ylim()
y_offset = 0.015 * (ymax - ymin)
for x_year, y_val, p in zip(years, high_swe_total_cost, pct_inc_c):
    ax_c0.text(x_year, y_val + y_offset, f"+{p:.1f}%", ha="center", va="bottom", fontsize=10, fontweight="bold", color=colors["SWE"], clip_on=False)

ax_c0.set_title("Overall view: costs", fontsize=12, fontweight="normal")
ax_c0.set_ylabel("Total system costs [bn€/yr]", fontsize=12)
ax_c0.set_xticks(years)
ax_c0.legend(frameon=False, loc="upper left")

cost_titles = ["Low scenario (7.7% SRE)", "Average scenario (17.2% SRE)", "High scenario (33% SRE)"]
cost_axes = [ax_c1, ax_c2, ax_c3]

for ax, title in zip(cost_axes, cost_titles):
    data = sre_costs_additional[title]
    for scen in ["DYN", "SIM", "SWE"]:
        ax.plot(years, data[scen], color=colors[scen], linestyle=linestyles[scen], marker=markers[scen], markersize=5, linewidth=2)
    ax.set_title(title, fontsize=12, fontweight="normal")
    ax.set_xticks(years)

max_cost_add = max(max(chain.from_iterable(sre_costs_additional[sc][k] for k in ["DYN", "SIM", "SWE"])) for sc in sre_costs_additional)
ylim_c = 90 if max_cost_add <= 90 else (int(max_cost_add / 10) + 1) * 10
for ax in cost_axes:
    ax.set_ylim(0, ylim_c)

ax_c1.set_ylabel("Additional costs [bn€]", fontsize=12)
for ax in [ax_c2, ax_c3]:
    ax.tick_params(axis="y", which="major", left=True, labelleft=False)
    ax.yaxis.set_major_formatter(NullFormatter())
    ax.spines["left"].set_visible(True)

legend_handles = [
    Line2D([], [], color=colors["DYN"], linestyle=linestyles["DYN"], marker=markers["DYN"], label=scenario_labels["DYN"]),
    Line2D([], [], color=colors["SIM"], linestyle=linestyles["SIM"], marker=markers["SIM"], label=scenario_labels["SIM"]),
    Line2D([], [], color=colors["SWE"], linestyle=linestyles["SWE"], marker=markers["SWE"], label=scenario_labels["SWE"]),
]

fig.subplots_adjust(right=0.84)
fig.legend(handles=legend_handles, loc="center left", bbox_to_anchor=(0.86, 0.5), frameon=False)

plt.show()