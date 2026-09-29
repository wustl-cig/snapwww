#!/usr/bin/env python3
"""
Rebuild index.html for the SNaP project page.

All numbers live in this file so the results tables (best / second-best
highlighting included) stay consistent with the paper.  Run:

    python3 build_page.py
"""

# ----------------------------------------------------------------------------
# Generic grouped table.
#   groups  : list of group headings (each spans len(metrics) columns)
#   metrics : list of (name, direction) with direction "up", "down" or "one"
#             ("one" = closer to 1 is better, used for the calibration ratio)
#   rows    : (label, cls, nfe, [values])  -- cls is "", "ours" or "degraded"
#   None marks a setting where the method does not apply.
# ----------------------------------------------------------------------------

ARROW = {"up": "&uarr;", "down": "&darr;", "one": "(&rarr;&nbsp;1)"}


def fmt(v, metric):
    if v is None:
        return "&ndash;"
    if isinstance(v, str):
        return v
    if metric in ("PSNR", "FID"):
        return f"{v:.2f}"
    if metric == "&Delta;<sub>cal</sub>":
        return f"{v:.2f}"
    return f"{v:.3f}"


def rank_column(rows, c, direction):
    """Return {row_index: 'best'|'second'} for column c."""
    key = {"up": lambda v: -v, "down": lambda v: v, "one": lambda v: abs(v - 1)}[direction]
    vals = sorted([(key(r[3][c]), i) for i, r in enumerate(rows)
                   if r[1] != "degraded" and isinstance(r[3][c], (int, float))])
    marks = {}
    if not vals:
        return marks
    best = vals[0][0]
    rest = []
    for k, i in vals:
        if k == best:
            marks[i] = "best"
        else:
            rest.append((k, i))
    if rest:
        second = rest[0][0]
        for k, i in rest:
            if k == second:
                marks[i] = "second"
    return marks


def grouped_table(groups, metrics, rows, nfe=True, compact=False):
    nm = len(metrics)
    ncol = len(groups) * nm
    marks = [rank_column(rows, c, metrics[c % nm][1]) for c in range(ncol)]

    cls = "results compact" if compact else "results"
    lead = "<th></th><th></th>" if nfe else "<th></th>"
    out = [f'<table class="{cls}">', "<thead>"]
    if len(groups) > 1 or groups[0]:
        out.append(f'<tr class="groups">{lead}' +
                   "".join(f'<th colspan="{nm}">{g}</th>' for g in groups) + "</tr>")
    out.append('<tr class="metrics"><th>Method</th>' + ("<th>NFE</th>" if nfe else "") +
               "".join(f"<th>{m}{ARROW[d]}</th>" for _ in groups for m, d in metrics) + "</tr>")
    out.append("</thead><tbody>")

    for i, (label, rcls, n, vals) in enumerate(rows):
        classes = [rcls] if rcls else []
        if i > 0 and rcls == "ours" and rows[i - 1][1] != "ours":
            classes.append("sep-top")
        if i == 1 and rows[0][1] == "degraded":
            classes.append("sep-top")
        tr = f' class="{" ".join(classes)}"' if classes else ""
        cells = []
        for c, v in enumerate(vals):
            mark = marks[c].get(i, "")
            td = f' class="{mark}"' if mark else ""
            cells.append(f"<td{td}>{fmt(v, metrics[c % nm][0])}</td>")
        nfe_td = f"<td>{n}</td>" if nfe else ""
        out.append(f"<tr{tr}><td>{label}</td>{nfe_td}" + "".join(cells) + "</tr>")

    out.append("</tbody></table>")
    return "\n".join(out)


def simple_table(headers, rows):
    out = ['<table class="results compact"><thead><tr class="metrics">']
    out += [f"<th>{h}</th>" for h in headers]
    out.append("</tr></thead><tbody>")
    for r in rows:
        tr = ' class="ours"' if "SNaP" in r[0] or "ours" in r[0] else ""
        out.append(f"<tr{tr}>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>")
    out.append("</tbody></table>")
    return "".join(out)


PSL = [("PSNR", "up"), ("SSIM", "up"), ("LPIPS", "down")]
NAT_TASKS = ["Deblurring", "Super-resolution", "Random inpainting", "Box inpainting"]
_ = None

# ---------------------------------------------------------------- Table 1
CELEBA = [
    ("Degraded",       "degraded", "&ndash;", [27.26, 0.838, 0.214, 11.67, 0.182, 0.859, 11.98, 0.198, 1.070, 22.33, 0.754, 0.217]),
    ("MSE regressor",  "",   1,    [35.74, 0.953, 0.029, 34.17, 0.945, 0.033, 34.42, 0.955, 0.022, _, _, _]),
    ("PnP-GS",         "",   23,   [33.97, 0.924, 0.041, 31.23, 0.890, 0.065, 29.17, 0.874, 0.066, _, _, _]),
    ("DDRM",           "",   20,   [35.02, 0.946, 0.027, 32.24, 0.927, 0.027, 32.40, 0.942, 0.029, _, _, _]),
    ("DiffPIR",        "",   100,  [34.83, 0.938, 0.027, 31.87, 0.892, 0.030, 32.45, 0.924, 0.024, 30.48, 0.918, 0.028]),
    ("OT-ODE",         "",   180,  [32.96, 0.920, 0.029, 31.34, 0.903, 0.027, 28.69, 0.871, 0.049, 29.37, 0.919, 0.038]),
    ("PnP-Flow5",      "",   500,  [34.80, 0.941, 0.046, 31.44, 0.905, 0.056, 33.98, 0.953, 0.021, 31.06, 0.939, 0.043]),
    ("Flower5-OT",     "",   500,  [35.65, 0.954, 0.031, 33.03, 0.931, 0.039, 33.97, 0.952, 0.019, 31.85, 0.952, 0.023]),
    ("DPS",            "",   1000, [34.27, 0.936, 0.019, 32.23, 0.917, 0.023, 33.43, 0.951, 0.013, 30.26, 0.942, 0.022]),
    ("SNaP (M=1)",     "ours", 1,  [32.90, 0.919, 0.018, 31.27, 0.903, 0.023, 31.97, 0.927, 0.018, 30.73, 0.934, 0.021]),
    ("SNaP (M=4)",     "ours", 4,  [34.98, 0.947, 0.022, 33.26, 0.934, 0.023, 33.97, 0.951, 0.015, 32.78, 0.954, 0.018]),
    ("SNaP (M=16)",    "ours", 16, [35.68, 0.954, 0.028, 33.95, 0.943, 0.029, 34.64, 0.957, 0.018, 33.43, 0.959, 0.020]),
    ("SNaP (M=100)",   "ours", 100,[35.91, 0.956, 0.030, 34.16, 0.946, 0.031, 34.84, 0.959, 0.019, 33.69, 0.961, 0.022]),
]

# ---------------------------------------------------------------- Table 6
AFHQ = [
    ("Degraded",       "degraded", "&ndash;", [24.39, 0.532, 0.543, 11.98, 0.212, 0.900, 13.25, 0.214, 1.091, 21.57, 0.736, 0.214]),
    ("MSE regressor",  "",   1,          [29.82, 0.806, 0.289, 29.16, 0.817, 0.201, 33.23, 0.915, 0.066, _, _, _]),
    ("PnP-GS",         "",   23,         [28.39, 0.787, 0.387, 24.44, 0.639, 0.411, 29.89, 0.841, 0.123, _, _, _]),
    ("PnP-Flow5",      "",   "500&ndash;2500", [29.01, 0.785, 0.312, 28.01, 0.791, 0.167, 34.47, 0.933, 0.044, 27.14, 0.900, 0.127]),
    ("DDRM",           "",   20,         [29.01, 0.784, 0.194, 27.09, 0.781, 0.186, 32.20, 0.907, 0.064, _, _, _]),
    ("DiffPIR",        "",   100,        [28.89, 0.773, 0.187, 23.16, 0.635, 0.291, 31.76, 0.881, 0.053, 27.71, 0.880, 0.059]),
    ("OT-ODE",         "",   180,        [27.82, 0.735, 0.126, 26.71, 0.737, 0.108, 29.98, 0.849, 0.086, 24.47, 0.873, 0.095]),
    ("Flower5-OT",     "",   "500&ndash;2500", [29.73, 0.801, 0.264, 27.09, 0.767, 0.272, 34.41, 0.932, 0.047, 27.32, 0.922, 0.067]),
    ("DPS",            "",   1000,       [25.90, 0.661, 0.148, 25.98, 0.694, 0.144, 32.06, 0.896, 0.036, 26.78, 0.900, 0.054]),
    ("SNaP (M=1)",     "ours", 1,        [26.25, 0.674, 0.159, 26.07, 0.703, 0.130, 30.48, 0.853, 0.066, 26.46, 0.891, 0.054]),
    ("SNaP (M=4)",     "ours", 4,        [28.33, 0.750, 0.157, 28.07, 0.777, 0.120, 32.38, 0.896, 0.052, 28.49, 0.914, 0.047]),
    ("SNaP (M=16)",    "ours", 16,       [29.09, 0.779, 0.231, 28.77, 0.802, 0.157, 33.04, 0.909, 0.056, 29.32, 0.922, 0.056]),
    ("SNaP (M=100)",   "ours", 100,      [29.32, 0.788, 0.320, 28.99, 0.810, 0.187, 33.25, 0.913, 0.058, 29.53, 0.925, 0.069]),
]

# ---------------------------------------------------------------- Table 2
FIDCAL = [
    ("MSE regressor",  "",     1,    [22.06, _,    24.76, _,    _,     _]),
    ("DDRM",           "",     20,   [20.26, 0.31, 18.94, 0.19, _,     _]),
    ("Flower1-OT",     "",     100,  [17.86, 0.23, 23.79, 0.24, 18.72, 0.24]),
    ("DPS",            "",     1000, [18.25, 0.64, 19.94, 0.67, 15.42, 2.15]),
    ("SNaP (M=1)",     "ours", 1,    [15.80, 1.03, 16.80, 0.99, 15.53, 1.08]),
]

# ---------------------------------------------------------------- Table 3
MRI = [
    ("Zero-filled",    "", "&ndash;", [25.35, 0.791, 25.37, 0.793, 21.98, 0.694, 21.99, 0.694]),
    ("Wavelet+&ell;<sub>1</sub>", "", "&ndash;", [26.57, 0.672, 27.75, 0.768, 23.02, 0.551, 23.81, 0.643]),
    ("TV",             "", "&ndash;", [26.19, 0.798, 26.27, 0.799, 22.62, 0.689, 22.66, 0.691]),
    ("MSE regressor",  "", 1,    [33.80, 0.909, 33.85, 0.912, 30.71, 0.875, 30.73, 0.878]),
    ("DiffPIR",        "", 100,  [29.84, 0.709, 30.01, 0.719, 26.14, 0.642, 26.31, 0.655]),
    ("CSGM",           "", 1000, [27.74, 0.734, 32.39, 0.802, 27.74, 0.733, 28.33, 0.754]),
    ("DPS",            "", 1000, [28.81, 0.646, 29.83, 0.669, 24.89, 0.575, 25.17, 0.574]),
    ("DAPS",           "", 1000, [31.55, 0.818, 32.44, 0.782, 27.31, 0.749, 28.01, 0.714]),
    ("PnP-DM",         "", 1000, [32.16, 0.778, 33.39, 0.786, 27.18, 0.701, 29.00, 0.712]),
    ("SNaP (M=1)",     "ours", 1,  [32.06, 0.889, 32.89, 0.899, 28.10, 0.818, 29.14, 0.845]),
    ("SNaP (M=4)",     "ours", 4,  [32.68, 0.904, 33.80, 0.919, 29.06, 0.843, 29.88, 0.864]),
    ("SNaP (M=16)",    "ours", 16, [32.85, 0.908, 34.05, 0.924, 29.34, 0.850, 30.09, 0.869]),
]

# ---------------------------------------------------------------- Table 4


def cost_table(title, methods, nfe, time, slow):
    head = ('<table class="results compact"><thead>'
            f'<tr class="groups"><th></th><th colspan="{len(methods)}">{title}</th></tr>'
            '<tr class="metrics"><th>Metric</th>' +
            "".join(f"<th>{m}</th>" for m in methods) + "</tr></thead><tbody>")
    last = len(methods) - 1

    def row(name, vals, f):
        cells = []
        for i, v in enumerate(vals):
            td = ' class="best"' if i == last else ""
            cells.append(f"<td{td}>{f(v)}</td>")
        return f"<tr><td>{name}</td>" + "".join(cells) + "</tr>"

    body = (row("NFE &darr;", nfe, str) +
            row("Time / sample (s) &darr;", time, str) +
            row("Slowdown vs. SNaP", slow, lambda v: v))
    return head + body + "</tbody></table>"


COST_CELEBA = cost_table("CelebA, Gaussian deblurring",
                         ["DPS", "OT-ODE", "Flower", "DDRM", "SNaP"],
                         [1000, 180, 100, 20, 1],
                         ["27.014", "6.575", "2.614", "0.360", "0.012"],
                         ["2251&times;", "548&times;", "218&times;", "30&times;", "&ndash;"])
COST_MRI = cost_table("fastMRI brain, multi-coil &times;8",
                      ["CSGM", "DAPS", "PnP-DM", "DPS", "SNaP"],
                      [1000, 1000, 1000, 1000, 1],
                      ["127.78", "96.28", "92.02", "76.07", "0.227"],
                      ["563&times;", "424&times;", "405&times;", "335&times;", "&ndash;"])

# ---------------------------------------------------------------- Table 5
SOURCE = simple_table(
    ["Source", "M=1 &middot; PSNR &uarr;", "LPIPS &darr;", "M=100 &middot; PSNR &uarr;", "LPIPS &darr;",
     "&Delta;<sub>cal</sub> (&rarr;&nbsp;1)"],
    [["N(0, I)", "35.85", "0.030", "35.86", "0.030", "0.00"],
     ["N(0, &tau;&sup2;I)", "35.83", "0.030", "35.84", "0.030", "0.00"],
     ["<b>N(m<sub>y</sub>, &tau;&sup2;W)&mdash;ours</b>", "32.90", "<b>0.018</b>", "<b>35.91</b>", "0.030", "<b>1.03</b>"]])

# ---------------------------------------------------------------- Table 7
NOISE = simple_table(
    ["Test noise &sigma;<sub>n</sub>", "PSNR &uarr;", "SSIM &uarr;", "LPIPS &darr;", "Input PSNR", "Gain"],
    [["0.01", "34.29", "0.940", "0.020", "29.96", "+4.33"],
     ["0.02", "34.15", "0.939", "0.019", "29.62", "+4.53"],
     ["0.03", "33.89", "0.936", "0.018", "29.12", "+4.77"],
     ["0.04", "33.50", "0.930", "0.017", "28.52", "+4.98"],
     ["0.05 &dagger; <span class='muted'>(training noise)</span>", "32.90", "0.919", "0.018", "27.81", "+5.09"]])

# ---------------------------------------------------------------- Table 8


def m_sweep(groups, data):
    """data: {M: [9 values]}  -> compact table with M rows, three groups of PSNR/SSIM/LPIPS."""
    rows = [(f"M = {m}", "", None, v) for m, v in data.items()]
    t = grouped_table(groups, PSL, rows, nfe=False, compact=True)
    return t.replace("<th>Method</th>", "<th>Draws</th>")


def _plain(t):
    # sweep tables compare settings, not methods: drop best/second highlighting
    return t.replace(' class="best"', "").replace(' class="second"', "")


TAU = _plain(m_sweep(["&tau; = 0.15", "&tau; = 0.5", "&tau; = 1.0"], {
    1:   [32.941, 0.9198, 0.0190, 32.922, 0.9187, 0.0186, 32.512, 0.9060, 0.0244],
    4:   [34.966, 0.9463, 0.0209, 34.948, 0.9457, 0.0181, 34.588, 0.9385, 0.0197],
    16:  [35.688, 0.9537, 0.0275, 35.663, 0.9532, 0.0234, 35.323, 0.9475, 0.0249],
    100: [35.913, 0.9558, 0.0300, 35.885, 0.9553, 0.0256, 35.552, 0.9500, 0.0273],
}))

# ---------------------------------------------------------------- Table 10
STEPS = _plain(m_sweep(["k = 1", "k = 2", "k = 4", "k = 8"], {
    1:   [32.941, 0.9198, 0.0190, 33.084, 0.9211, 0.0172, 33.037, 0.9205, 0.0172, 32.992, 0.9200, 0.0173],
    4:   [34.966, 0.9463, 0.0209, 35.044, 0.9469, 0.0206, 35.001, 0.9465, 0.0206, 34.942, 0.9458, 0.0210],
    16:  [35.688, 0.9537, 0.0275, 35.729, 0.9540, 0.0275, 35.688, 0.9536, 0.0276, 35.621, 0.9529, 0.0281],
    100: [35.913, 0.9558, 0.0300, 35.943, 0.9561, 0.0302, 35.902, 0.9557, 0.0303, 35.833, 0.9550, 0.0308],
}))

# ---------------------------------------------------------------- Table 12
NULLFLOW = simple_table(
    ["Test &sigma;<sub>n</sub>", "NullFlow &middot; PSNR &uarr;", "SSIM &uarr;", "LPIPS &darr;",
     "SNaP &middot; PSNR &uarr;", "SSIM &uarr;", "LPIPS &darr;"],
    [["0.00", "<b>33.50</b>", "<b>0.977</b>", "<b>0.012</b>", "31.37", "0.947", "0.025"],
     ["0.01", "<b>33.27</b>", "<b>0.970</b>", "<b>0.012</b>", "31.35", "0.947", "0.024"],
     ["0.02", "<b>32.65</b>", "<b>0.952</b>", "<b>0.016</b>", "31.30", "0.946", "0.023"],
     ["0.05", "30.11", "0.855", "0.055", "<b>30.74</b>", "<b>0.934</b>", "<b>0.021</b>"]])

# ---------------------------------------------------------------- Table 11
VFM = simple_table(
    ["Method", "Aligned operator (parity) &middot; MMD&sup2; &darr;", "Rotated operator &middot; MMD&sup2; &darr;"],
    [["<b>SNaP</b>", "<b>0.0027 &plusmn; 0.0003</b>", "<b>0.0171 &plusmn; 0.0012</b>"],
     ["VFM (joint)", "0.0109 &plusmn; 0.0007", "0.0737 &plusmn; 0.0199"],
     ["VFM (frozen &theta;)", "0.0102 &plusmn; 0.0003", "0.1900 &plusmn; 0.0015"]])

# ----------------------------------------------------------------------------

TABLES = {
    "CELEBA":   grouped_table(NAT_TASKS, PSL, CELEBA),
    "AFHQ":     grouped_table(NAT_TASKS, PSL, AFHQ),
    "FIDCAL":   grouped_table(["Gaussian deblurring", "Super-resolution", "Box inpainting"],
                              [("FID", "down"), ("&Delta;<sub>cal</sub>", "one")], FIDCAL),
    "MRI":      grouped_table(["&times;4 &middot; 20 dB", "&times;4 &middot; 30 dB",
                               "&times;8 &middot; 20 dB", "&times;8 &middot; 30 dB"],
                              [("PSNR", "up"), ("SSIM", "up")], MRI),
    "COST_CELEBA": COST_CELEBA,
    "COST_MRI":    COST_MRI,
    "SOURCE":   SOURCE,
    "NOISE":    NOISE,
    "TAU":      TAU,
    "STEPS":    STEPS,
}

with open("template.html", encoding="utf-8") as f:
    page = f.read()

for key, html_table in TABLES.items():
    tag = f"<!--TABLE_{key}-->"
    assert tag in page, f"placeholder {tag} missing from template.html"
    page = page.replace(tag, html_table)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(page)

print("index.html written ({:,} bytes)".format(len(page)))
