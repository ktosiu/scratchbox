import os
import sys
import argparse
import math
import matplotlib
matplotlib.use("agg")

import psycopg2

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import seaborn as sns

from matplotlib.backends.backend_pdf import PdfPages 

#sns.set(context="paper", font="monospace")
sns.set(context="paper")
#sns.set(context="paper", font_scale=.5)
#sns.set()

#  numjobs | iodepth | read_iops 
fiodata = [
(       1 ,       1 ,     18352),
(       1 ,       2 ,     41528),
(       1 ,       4 ,     86342),
(       1 ,       8 ,    167628),
(       1 ,      16 ,    284939),
(       1 ,      32 ,    325982),
(       1 ,      64 ,    328639),
(       1 ,     128 ,    259234),
(       1 ,     256 ,    328308),
(       1 ,     512 ,    266221),
(       1 ,    1024 ,    311454),
(       1 ,    2048 ,    307397),
(       2 ,       1 ,     42806),
(       2 ,       2 ,     87006),
(       2 ,       4 ,    167914),
(       2 ,       8 ,    307142),
(       2 ,      16 ,    485305),
(       2 ,      32 ,    527752),
(       2 ,      64 ,    535940),
(       2 ,     128 ,    535056),
(       2 ,     256 ,    523688),
(       2 ,     512 ,    544151),
(       2 ,    1024 ,    503716),
(       4 ,       1 ,     83410),
(       4 ,       2 ,    162540),
(       4 ,       4 ,    297679),
(       4 ,       8 ,    494102),
(       4 ,      16 ,    790088),
(       4 ,      32 ,    981115),
(       4 ,      64 ,    937745),
(       4 ,     128 ,    827291),
(       4 ,     256 ,    734552),
(       4 ,     512 ,    966878),
(       8 ,       1 ,    157897),
(       8 ,       2 ,    294023),
(       8 ,       4 ,    513018),
(       8 ,       8 ,    805836),
(       8 ,      16 ,    975725),
(       8 ,      32 ,   1000456),
(       8 ,      64 ,   1002497),
(       8 ,     128 ,   1002905),
(       8 ,     256 ,    997535),
(      16 ,       1 ,    281924),
(      16 ,       2 ,    477645),
(      16 ,       4 ,    808522),
(      16 ,       8 ,    987589),
(      16 ,      16 ,   1001280),
(      16 ,      32 ,   1002019),
(      16 ,      64 ,    990349),
(      16 ,     128 ,    989386),
(      32 ,       1 ,    437690),
(      32 ,       2 ,    581477),
(      32 ,       4 ,    691755),
(      32 ,       8 ,    961569),
(      32 ,      16 ,    974202),
(      32 ,      32 ,    978152),
(      32 ,      64 ,    965226),
(      64 ,       1 ,    486324),
(      64 ,       2 ,    777399),
(      64 ,       4 ,    983578),
(      64 ,       8 ,   1000864),
(      64 ,      16 ,   1000836),
(      64 ,      32 ,    997395),
(     128 ,       1 ,    891782),
(     128 ,       2 ,    997428),
(     128 ,       4 ,   1001181),
(     128 ,       8 ,   1001091),
(     128 ,      16 ,   1000121),
(     256 ,       1 ,    999859),
(     256 ,       2 ,   1002155),
(     256 ,       4 ,   1002339),
(     256 ,       8 ,   1001701),
(     512 ,       1 ,    930063),
(     512 ,       2 ,   1000178),
(     512 ,       4 ,   1000574),
(    1024 ,       1 ,   1982197),
(    1024 ,       2 ,    992985),
(    2048 ,       1 ,   1001428),
]

fiodata = [
(       1 ,       1 ,     94322),
(       1 ,       2 ,    171948),
(       1 ,       4 ,    347958),
(       1 ,       8 ,    359882),
(       1 ,      16 ,    356767),
(       1 ,      32 ,    354846),
(       1 ,      64 ,    365027),
(       1 ,     128 ,    268822),
(       1 ,     256 ,    267973),
(       1 ,     512 ,    267755),
(       1 ,    1024 ,    346422),
(       1 ,    2048 ,    256029),
(       2 ,       1 ,    180885),
(       2 ,       2 ,    307324),
(       2 ,       4 ,    560328),
(       2 ,       8 ,    587587),
(       2 ,      16 ,    554131),
(       2 ,      32 ,    593888),
(       2 ,      64 ,    584018),
(       2 ,     128 ,    599387),
(       2 ,     256 ,    581384),
(       2 ,     512 ,    624826),
(       2 ,    1024 ,    519263),
(       4 ,       1 ,    282609),
(       4 ,       2 ,    485195),
(       4 ,       4 ,    731077),
(       4 ,       8 ,    772753),
(       4 ,      16 ,    795268),
(       4 ,      32 ,    799985),
(       4 ,      64 ,    795733),
(       4 ,     128 ,    708861),
(       4 ,     256 ,    775120),
(       4 ,     512 ,    786552),
(       8 ,       1 ,    374258),
(       8 ,       2 ,    516459),
(       8 ,       4 ,    788354),
(       8 ,       8 ,    800599),
(       8 ,      16 ,    797281),
(       8 ,      32 ,    794830),
(       8 ,      64 ,    799381),
(       8 ,     128 ,    788781),
(       8 ,     256 ,    791217),
(      16 ,       1 ,    511783),
(      16 ,       2 ,    774668),
(      16 ,       4 ,    799963),
(      16 ,       8 ,    797998),
(      16 ,      16 ,    800113),
(      16 ,      32 ,    787551),
(      16 ,      64 ,    800688),
(      16 ,     128 ,    739068),
(      32 ,       1 ,    499097),
(      32 ,       2 ,    759083),
(      32 ,       4 ,    721749),
(      32 ,       8 ,    770760),
(      32 ,      16 ,    787587),
(      32 ,      32 ,    779526),
(      32 ,      64 ,    766722),
(      64 ,       1 ,    647519),
(      64 ,       2 ,    766156),
(      64 ,       4 ,    770139),
(      64 ,       8 ,    776497),
(      64 ,      16 ,    770786),
(      64 ,      32 ,    746461),
(     128 ,       1 ,    800271),
(     128 ,       2 ,    803035),
(     128 ,       4 ,    799044),
(     128 ,       8 ,    795593),
(     128 ,      16 ,    786748),
(     256 ,       1 ,    807286),
(     256 ,       2 ,    805624),
(     256 ,       4 ,    800623),
(     256 ,       8 ,    768156),
(     512 ,       1 ,    806983),
(     512 ,       2 ,    805636),
(     512 ,       4 ,    797635),
(    1024 ,       1 ,    801922),
(    1024 ,       2 ,    806616),
(    2048 ,       1 ,    889158),
]

fiodata_q995 = [
(       1 ,       1 ,        21),
(       1 ,       2 ,        25),
(       1 ,       4 ,        21),
(       1 ,       8 ,        43),
(       1 ,      16 ,        81),
(       1 ,      32 ,       159),
(       1 ,      64 ,       221),
(       1 ,     128 ,       708),
(       1 ,     256 ,      1416),
(       1 ,     512 ,      2864),
(       1 ,    1024 ,      4704),
(       1 ,    2048 ,     11456),
(       2 ,       1 ,        23),
(       2 ,       2 ,        25),
(       2 ,       4 ,        29),
(       2 ,       8 ,        59),
(       2 ,      16 ,       122),
(       2 ,      32 ,       153),
(       2 ,      64 ,       318),
(       2 ,     128 ,       612),
(       2 ,     256 ,      1112),
(       2 ,     512 ,      2128),
(       2 ,    1024 ,      5600),
(       4 ,       1 ,        28),
(       4 ,       2 ,        34),
(       4 ,       4 ,        41),
(       4 ,       8 ,       163),
(       4 ,      16 ,       153),
(       4 ,      32 ,      1004),
(       4 ,      64 ,       604),
(       4 ,     128 ,      5984),
(       4 ,     256 ,      7264),
(       4 ,     512 ,     13632),
(       8 ,       1 ,        44),
(       8 ,       2 ,       116),
(       8 ,       4 ,        85),
(       8 ,       8 ,       143),
(       8 ,      16 ,       294),
(       8 ,      32 ,       892),
(       8 ,      64 ,      1288),
(       8 ,     128 ,      2448),
(       8 ,     256 ,      7328),
(      16 ,       1 ,       102),
(      16 ,       2 ,       120),
(      16 ,       4 ,       231),
(      16 ,       8 ,       652),
(      16 ,      16 ,       676),
(      16 ,      32 ,      2544),
(      16 ,      64 ,      5344),
(      16 ,     128 ,     24448),
(      32 ,       1 ,       209),
(      32 ,       2 ,       302),
(      32 ,       4 ,       510),
(      32 ,       8 ,       804),
(      32 ,      16 ,      3120),
(      32 ,      32 ,      7776),
(      32 ,      64 ,     11456),
(      64 ,       1 ,       219),
(      64 ,       2 ,       434),
(      64 ,       4 ,      1144),
(      64 ,       8 ,      6560),
(      64 ,      16 ,     20608),
(      64 ,      32 ,     28544),
(     128 ,       1 ,       482),
(     128 ,       2 ,       692),
(     128 ,       4 ,      7008),
(     128 ,       8 ,      9664),
(     128 ,      16 ,     16320),
(     256 ,       1 ,       644),
(     256 ,       2 ,      2896),
(     256 ,       4 ,      8160),
(     256 ,       8 ,     51456),
(     512 ,       1 ,      2992),
(     512 ,       2 ,     10048),
(     512 ,       4 ,     59648),
(    1024 ,       1 ,      7264),
(    1024 ,       2 ,     12736),
(    2048 ,       1 ,     48896),
]

fiodata_cpu = [
(       1 ,       1 , 100. - 98.16084493023791),
(       1 ,       2 , 100. - 97.84800419858618),
(       1 ,       4 , 100. - 97.62869261035327),
(       1 ,       8 , 100. - 97.59764074874718),
(       1 ,      16 , 100. - 97.6279156632031),
(       1 ,      32 , 100. - 97.63191396673473),
(       1 ,      64 , 100. - 97.55685790407041),
(       1 ,     128 , 100. - 96.55816362817693),
(       1 ,     256 , 100. - 96.5650124364253),
(       1 ,     512 , 100. - 96.57254054525644),
(       1 ,    1024 , 100. - 97.64165722393344),
(       1 ,    2048 , 100. - 96.53334621073621),
(       2 ,       1 , 100. - 97.33804213743788),
(       2 ,       2 , 100. - 96.63790821480055),
(       2 ,       4 , 100. - 95.75287987744183),
(       2 ,       8 , 100. - 95.01626323782055),
(       2 ,      16 , 100. - 94.52887903281557),
(       2 ,      32 , 100. - 94.28227828812061),
(       2 ,      64 , 100. - 94.74520551011925),
(       2 ,     128 , 100. - 94.92334036965794),
(       2 ,     256 , 100. - 94.28272461465112),
(       2 ,     512 , 100. - 95.19926074208026),
(       2 ,    1024 , 100. - 94.27330091798757),
(       4 ,       1 , 100. - 95.54826540978787),
(       4 ,       2 , 100. - 93.98916774393491),
(       4 ,       4 , 100. - 93.2182074049883),
(       4 ,       8 , 100. - 92.23545402187861),
(       4 ,      16 , 100. - 92.49616749447759),
(       4 ,      32 , 100. - 92.24360748820752),
(       4 ,      64 , 100. - 92.16003010766052),
(       4 ,     128 , 100. - 91.60931082167122),
(       4 ,     256 , 100. - 91.90989286421647),
(       4 ,     512 , 100. - 91.55716622427285),
(       8 ,       1 , 100. - 91.62428633308778),
(       8 ,       2 , 100. - 91.70524051884725),
(       8 ,       4 , 100. - 90.08591302638469),
(       8 ,       8 , 100. - 90.13541318605947),
(       8 ,      16 , 100. - 90.27315098847242),
(       8 ,      32 , 100. - 88.73864586990169),
(       8 ,      64 , 100. - 89.11848118189488),
(       8 ,     128 , 100. - 88.66417468097926),
(       8 ,     256 , 100. - 88.97497517384768),
(      16 ,       1 , 100. - 83.67569534494261),
(      16 ,       2 , 100. - 85.60517583480356),
(      16 ,       4 , 100. - 86.43797914165638),
(      16 ,       8 , 100. - 87.27819892403565),
(      16 ,      16 , 100. - 85.69876661950889),
(      16 ,      32 , 100. - 86.36904992613299),
(      16 ,      64 , 100. - 87.54653495208301),
(      16 ,     128 , 100. - 88.5566950388041),
(      32 ,       1 , 100. - 81.53890320332965),
(      32 ,       2 , 100. - 84.12121876567119),
(      32 ,       4 , 100. - 89.27573742211611),
(      32 ,       8 , 100. - 88.67091201628786),
(      32 ,      16 , 100. - 83.52344367362488),
(      32 ,      32 , 100. - 86.77161727778572),
(      32 ,      64 , 100. - 86.13829453071288),
(      64 ,       1 , 100. - 62.49856981313625),
(      64 ,       2 , 100. - 81.17726021464149),
(      64 ,       4 , 100. - 79.60525436447176),
(      64 ,       8 , 100. - 82.4055234892324),
(      64 ,      16 , 100. - 81.58470725368774),
(      64 ,      32 , 100. - 81.40261421678558),
(     128 ,       1 , 100. - 66.42865322030633),
(     128 ,       2 , 100. - 66.72950247349442),
(     128 ,       4 , 100. - 71.79945413004677),
(     128 ,       8 , 100. - 78.62599368407578),
(     128 ,      16 , 100. - 79.7777744977493),
(     256 ,       1 , 100. - 61.80726005104632),
(     256 ,       2 , 100. - 63.25710380803527),
(     256 ,       4 , 100. - 67.59534126459104),
(     256 ,       8 , 100. - 77.23567382329742),
(     512 ,       1 , 100. - 58.58889796845559),
(     512 ,       2 , 100. - 62.25960049931128),
(     512 ,       4 , 100. - 67.87435768812952),
(    1024 ,       1 , 100. - 60.482178798426474),
(    1024 ,       2 , 100. - 58.785170230930675),
(    2048 ,       1 , 100. - 80.09729724538914),
]


def plot_fio_aio_heatmap(data, ax, cmap=None, vmin=None, vmax=None):
    xticklabels = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]
    yticklabels = list(reversed(xticklabels))
    heatmap_data = np.ndarray(shape=(12,12), dtype=float, order='F')
    heatmap_data.fill(0)

    for d in data:
        numjobs = int(math.log(d[0], 2))
        iodepth = 11- int(math.log(d[1], 2))
        read_iops = d[2]
        heatmap_data[iodepth][numjobs] = int(read_iops)

    sns.heatmap(heatmap_data, ax=ax, cmap=cmap, vmin=vmin, vmax=vmax, annot=True, annot_kws={"size": 5}, fmt="g", xticklabels=xticklabels, yticklabels=yticklabels)


def create_report_page(data, outfile):
    pdf = PdfPages(outfile) 

    fig_width_cm = 21                         # A4 page
    fig_height_cm = 29.7
    inches_per_cm = 1 / 2.54              # Convert cm to inches
    fig_width = fig_width_cm * inches_per_cm # width in inches
    fig_height = fig_height_cm * inches_per_cm       # height in inches
    fig_size = [fig_width, fig_height] 

    allplots = 3  # This is the variable number of subplots 

    fig, axarr = plt.subplots(allplots, 1)
    fig.set_size_inches(fig_size) 


    #ax.set(xlabel="number of workers", ylabel="IO Depth")
    #for plot in range(allplots):
    #    axarr[plot].plot(x + plot, y) 

    #plt.title('IOPS for random 4kB writes (async. IO): single Intel P3700 NVMe as block device', ax=axarr[0])

    cmap = sns.diverging_palette(h_neg=210, h_pos=350, s=90, l=30, as_cmap=True)
    #cmap2 = sns.blend_palette(["firebrick", "palegreen"], 8) 
    #for ax in axarr:
    plot_fio_aio_heatmap(data['iops'], axarr[0], cmap=None)
    plot_fio_aio_heatmap(data['latency_q995'], axarr[1], cmap="copper_r")
    plot_fio_aio_heatmap(data['cpu_idle'], axarr[2], cmap="jet", vmin=0, vmax=100)
    #sns.heatmap(data, ax=ax, annot=True, annot_kws={"size": 5}, fmt="g", xticklabels=xticklabels)
    #plt.xlabel = xticklabels
    #plt.ylabel = yticklabels
    #Spectral, summer, coolwarm, Wistia_r, pink_r, Set1, Set2, Set3,
    # brg_r, Dark2, prism, PuOr_r, afmhot_r, terrain_r, PuBuGn_r, RdPu,
    # gist_ncar_r, gist_yarg_r, Dark2_r, YlGnBu, RdYlBu, hot_r, gist_rainbow_r,
    # gist_stern, PuBu_r, cool_r, cool, gray, copper_r, Greens_r, GnBu, gist_ncar,
    # spring_r, gist_rainbow, gist_heat_r, Wistia, OrRd_r, CMRmap, bone,
    # gist_stern_r, RdYlGn, Pastel2_r, spring, terrain, YlOrRd_r, Set2_r,
    # winter_r, PuBu, RdGy_r, spectral, rainbow, flag_r, jet_r, RdPu_r,
    # gist_yarg, BuGn, Paired_r, hsv_r, bwr, cubehelix, Greens, PRGn,
    # gist_heat, spectral_r, Paired, hsv, Oranges_r, prism_r, Pastel2,
    # Pastel1_r, Pastel1, gray_r, jet, Spectral_r, gnuplot2_r, gist_earth,
    # YlGnBu_r, copper, gist_earth_r, Set3_r, OrRd, gnuplot_r, ocean_r, brg,
    # gnuplot2, PuRd_r, bone_r, BuPu, Oranges, RdYlGn_r, PiYG, CMRmap_r, YlGn,
    # binary_r, gist_gray_r, Accent, BuPu_r, gist_gray, flag, bwr_r, RdBu_r, BrBG,
    # Reds, Set1_r, summer_r, GnBu_r, BrBG_r, Reds_r, RdGy, PuRd, Accent_r,
    # Blues, autumn_r, autumn, cubehelix_r, nipy_spectral_r, ocean, PRGn_r,
    # Greys_r, pink, binary, winter, gnuplot, RdYlBu_r, hot, YlOrBr, coolwarm_r,
    # rainbow_r, Purples_r, PiYG_r, YlGn_r, Blues_r, YlOrBr_r, seismic, Purples,
    # seismic_r, RdBu, Greys, BuGn_r, YlOrRd, PuOr, PuBuGn, nipy_spectral, afmhot
    #fig.savefig("test3.pdf", figsize=(11.69,8.27))

    pdf.savefig()
    pdf.close() 


def get_test_result(conn, test_id, ioengine="aio", blocksize=4, iomode="randread", indicator="read_iops"):

    if indicator == "read_iops":
        sel = "round((result->'jobs'->0->'read'->'iops')::text::float)"

    elif indicator == "read_latency_q995":
        sel = "round((result->'jobs'->0->'read'->'clat'->'percentile'->'99.500000')::text::float)"

    elif indicator == "write_iops":
        sel = "round((result->'jobs'->0->'write'->'iops')::text::float)"

    elif indicator == "write_latency_q995":
        sel = "round((result->'jobs'->0->'write'->'clat'->'percentile'->'99.500000')::text::float)"

    elif indicator == "cpu_idle":
        sel = "(cpu_load->'idle')::text::float"

    else:
        raise Exception("unknown indicator {}".format(indicator))

    sql = """
        select
            numjobs,
            iodepth,
            {0} as indicator
        from
            perf.tbl_storage_test_result
        where
            test_id = %s
            and ioengine = %s
            and iomode = %s
            and blocksize = %s
    """.format(sel)

    res = []
    cur = conn.cursor()
    cur.execute(sql, (test_id, ioengine, iomode, blocksize))
    for numjobs, iodepth, indicator in cur.fetchall():
        res.append([numjobs, iodepth, indicator])

    return res


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    # target database
    #
    parser.add_argument("--pghost", type=str, default="localhost", help='PostgreSQL database server.')
    parser.add_argument("--pgport", type=int, default=5434, help='PostgreSQL database server listening port.')
    parser.add_argument("--pgdb", type=str, default="adr", help='PostgreSQL database name.')
    parser.add_argument("--pguser", type=str, default="oberstet", help='PostgreSQL database user.')
    parser.add_argument("--pgpassword", type=str, default=os.environ.get('PGPASSWORD', None), help='PostgreSQL database user password.')

    # parse cmd line args
    #
    args = parser.parse_args()

    # connect to DB
    #
    conn = psycopg2.connect(host=args.pghost, port=args.pgport, database=args.pgdb, user=args.pguser, password=args.pgpassword)
    conn.autocommit = True

    data = {
        'iops': fiodata,
        'latency_q995': fiodata_q995,
        'cpu_idle': fiodata_cpu
    }

    data['iops'] = get_test_result(conn, test_id=1, indicator="read_iops", ioengine="aio", blocksize=4, iomode="randread")
    data['latency_q995'] = get_test_result(conn, test_id=1, indicator="read_latency_q995", ioengine="aio", blocksize=4, iomode="randread")
    data['cpu_idle'] = get_test_result(conn, test_id=1, indicator="cpu_idle", ioengine="aio", blocksize=4, iomode="randread")

    create_report_page(data, "outfile.pdf")
