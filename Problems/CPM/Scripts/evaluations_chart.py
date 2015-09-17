def evaluation_data():
    eval = {}

    apache = {}
    apache["random_where"] = [8, 8, 16, 16, 16, 16, 16, 16, 16]
    apache["base_line"] = [20, 39, 58, 77, 96, 116, 135, 154, 173]
    apache["exemplar_where"] = [20, 39, 58, 77, 96, 116, 135, 154, 173]
    apache["east_west_where"] = [16, 16, 32, 32, 32, 32, 32, 32, 32]
    eval["apache"] = apache

    BDBJ = {}
    BDBJ["random_where"] = [8, 8, 15, 16, 16, 16, 16, 16, 16]
    BDBJ["base_line"] = [18, 36, 55, 72, 90, 108, 126, 145, 163]
    BDBJ["exemplar_where"] = [18, 36, 55, 72, 90, 108, 126, 145, 163]
    BDBJ["east_west_where"] = [16, 16, 30, 32, 32, 30, 30, 32, 32]
    eval["BDBJ"] = BDBJ

    bdbc = {}
    bdbc["random_where"] = [30, 30, 30, 52, 52, 52, 52, 51, 51]
    bdbc["base_line"] = [256, 512, 768, 1024, 1280, 1536, 1792, 2049, 2305]
    bdbc["exemplar_where"] = [256, 512, 768, 1024, 1280, 1536, 1792, 2049, 2305]
    bdbc["east_west_where"] = [60, 60, 60, 104.6, 105.1, 100.8, 103.7, 102.6, 100.3]
    eval["BDBC"] = bdbc

    sql = {}
    sql["random_where"] = [30, 33, 52, 53, 56, 51, 49, 51, 82]
    sql["base_line"] = [466, 931, 1396, 1862, 2327, 2796, 3258, 3723, 4188]
    sql["exemplar_where"] = [466, 931, 1396, 1862, 2327, 2796, 3258, 3723, 4188]
    sql["east_west_where"] = [60, 65, 104, 103, 102, 103, 103, 101, 161]
    eval["SQL"] = sql


    X264 = {}
    X264["random_where"] = [16, 22, 30, 30, 30, 29, 30, 29, 51]
    X264["base_line"] = [116, 231, 346, 461, 576, 692, 807, 922, 1037]
    X264["exemplar_where"] = [116, 231, 346, 461, 576, 692, 807, 922, 1037]
    X264["east_west_where"] = [32, 45, 59, 60, 60, 60, 60, 59, 108]
    eval["X264"] = X264

    LLVM = {}
    LLVM["random_where"] = [16, 16, 31, 30, 30, 30, 30, 30, 30]
    LLVM["base_line"] = [103, 205, 308, 410, 512, 615, 717, 820, 922]
    LLVM["exemplar_where"] = [103, 205, 308, 410, 512, 615, 717, 820, 922]
    LLVM["east_west_where"] = [32, 31, 60, 59, 60, 58, 58, 60, 59]
    eval["LLVM"] = LLVM

    return eval



import numpy as np
import matplotlib.pyplot as plt

data = evaluation_data()

# print len(data["apache"]["east_west_where"])

left, width = .55, .5
bottom, height = .25, .5
right = left + width
top = bottom + height

index = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90])
bar_width = 2
#
opacity = 0.2
error_config = {'ecolor': '0.3'}
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica'], 'size':9.5})
# rc('text', usetex=True)

f, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(6, 1, sharex='col', sharey='row')

r1 = ax1.bar(index, data["apache"]["exemplar_where"], bar_width,alpha=opacity,color='r',error_kw=error_config)
r2 = ax1.bar(index + bar_width, data["apache"]["random_where"], bar_width,alpha=opacity,color='y',error_kw=error_config)
r3 = ax1.bar(index + 2*bar_width, data["apache"]["east_west_where"], bar_width,alpha=opacity,color='g',error_kw=error_config)
# ax1.set_xlim(5, 50)
# ax1.set_ylim(0, 119)
# ax1.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
ax1.yaxis.offsetText.set_visible(False)


ax1.text(right, 0.5*(bottom+top), 'Apache',
        horizontalalignment='center',
        verticalalignment='center',
        rotation=270,
        fontsize=11,
        transform=ax1.transAxes)


# ax2.set_title('Berkeley DB C')
#r1 = ax1.bar(index, data["BDBC"]["base_line"], bar_width,alpha=opacity,color='b',error_kw=error_config)
r1 = ax2.bar(index, data["BDBC"]["exemplar_where"], bar_width,alpha=opacity,color='r',error_kw=error_config)
r2 = ax2.bar(index + bar_width, data["BDBC"]["random_where"], bar_width,alpha=opacity,color='y',error_kw=error_config)
r3 = ax2.bar(index + 2*bar_width, data["BDBC"]["east_west_where"], bar_width,alpha=opacity,color='g',error_kw=error_config)
# ax2.set_xlim(5, 50)
# ax2.set_ylim(0, 119)
ax2.yaxis.offsetText.set_visible(False)
ax2.text(right, 0.5*(bottom+top), 'BDBC',
        horizontalalignment='center',
        verticalalignment='center',
        rotation=270,
        fontsize=11,
        transform=ax2.transAxes)


# ax3.set_title('Berkeley DB Java')
#r1 = ax1.bar(index, data["BDBJ"]["base_line"], bar_width,alpha=opacity,color='b',error_kw=error_config)
r1 = ax3.bar(index, data["BDBJ"]["exemplar_where"], bar_width,alpha=opacity,color='r',error_kw=error_config)
r2 = ax3.bar(index + bar_width, data["BDBJ"]["random_where"], bar_width,alpha=opacity,color='y',error_kw=error_config)
r3 = ax3.bar(index + 2*bar_width, data["BDBJ"]["east_west_where"], bar_width,alpha=opacity,color='g',error_kw=error_config)
# ax3.set_ylim(0, 119)
# ax3.set_xlim(5, 50)
ax3.yaxis.offsetText.set_visible(False)
ax3.text(right, 0.5*(bottom+top), 'BDBJ',
        horizontalalignment='center',
        verticalalignment='center',
        rotation=270,
        fontsize=11,
        transform=ax3.transAxes)


# ax4.set_title('LLVM')
#r1 = ax1.bar(index, data["LLVM"]["base_line"], bar_width,alpha=opacity,color='b',error_kw=error_config)
r1 = ax4.bar(index, data["LLVM"]["exemplar_where"], bar_width,alpha=opacity,color='r',error_kw=error_config)
r2 = ax4.bar(index + bar_width, data["LLVM"]["random_where"], bar_width,alpha=opacity,color='y',error_kw=error_config)
r3 = ax4.bar(index + 2*bar_width, data["LLVM"]["east_west_where"], bar_width,alpha=opacity,color='g',error_kw=error_config)
# ax4.set_xlim(5, 50)
# ax4.set_ylim(0, 119)
ax4.yaxis.offsetText.set_visible(False)
ax4.text(right, 0.5*(bottom+top), 'LLVM',
        horizontalalignment='center',
        verticalalignment='center',
        rotation=270,
        fontsize=11,
        transform=ax4.transAxes)



#r1 = ax1.bar(index, data["SQL"]["base_line"], bar_width,alpha=opacity,color='b',error_kw=error_config)
r1 = ax5.bar(index, data["SQL"]["exemplar_where"], bar_width,alpha=opacity,color='r',error_kw=error_config)
r2 = ax5.bar(index + bar_width, data["SQL"]["random_where"], bar_width,alpha=opacity,color='y',error_kw=error_config)
r3 = ax5.bar(index + 2*bar_width, data["SQL"]["east_west_where"], bar_width,alpha=opacity,color='g',error_kw=error_config)
# ax5.set_xlim(5, 50)
# ax5.set_ylim(0, 119)
ax5.yaxis.offsetText.set_visible(False)
ax5.text(right, 0.5*(bottom+top), 'SQL',
        horizontalalignment='center',
        verticalalignment='center',
        rotation=270,
        fontsize=11,
        transform=ax5.transAxes)

# ax6.set_title('X264')
#r1 = ax1.bar(index, data["X264"]["base_line"], bar_width,alpha=opacity,color='b',error_kw=error_config)
r1 = ax6.bar(index, data["X264"]["exemplar_where"], bar_width,alpha=opacity,color='r',error_kw=error_config)
r2 = ax6.bar(index + bar_width, data["X264"]["random_where"], bar_width,alpha=opacity,color='y',error_kw=error_config)
r3 = ax6.bar(index + 2*bar_width, data["X264"]["east_west_where"], bar_width,alpha=opacity,color='g',error_kw=error_config)
# ax6.set_xlim(5, 50)
# ax6.set_ylim(0, 119)
ax6.yaxis.offsetText.set_visible(False)
ax6.text(right, 0.5*(bottom+top), 'X264',
        horizontalalignment='center',
        verticalalignment='center',
        rotation=270,
        fontsize=11,
        transform=ax6.transAxes)



plt.figlegend([ r1, r2, r3], [ "Where Exemplar", "Where Random",  "Where East West"], frameon=False, loc='lower center', bbox_to_anchor=(0.5, -0.0145), fancybox=True, ncol=2)
f.text(0.04, 0.5, 'Time Saved(%)', va='center', rotation='vertical', fontsize=11)
plt.xticks([15, 25, 35, 45], ['10', '20', '40', '80'])
f.set_size_inches(6.0, 8.5)
f.subplots_adjust(wspace=0, hspace=0)
# plt.ylabel("Time saved(%)", fontsize=11)
# plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
# plt.tight_layout()
# plt.show()
plt.savefig('evaluation_graph.eps', format='eps')