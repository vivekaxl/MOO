

import os

def read_file_return_list(filename):
    return open("../"+filename, "r").readlines()

def get_dataset(filename):
    convert_names = {"CPM_APACHE": "../../../Problems/CPM/data/Apache_AllMeasurements.csv",
                     "CPM_BDBC": "../../../Problems/CPM/data/BDBC_AllMeasurements.csv",
                     "CPM_BDBJ": "../../../Problems/CPM/data/BDBJ_AllMeasurements.csv",
                     "CPM_LLVM": "../../../Problems/CPM/data/LLVM_AllMeasurements.csv",
                     "CPM_SQL": "../../../Problems/CPM/data/SQL_AllMeasurements.csv",
                     "CPM_X264": "../../../Problems/CPM/data/x264_AllMeasurements.csv"
                     }
    filename = convert_names[filename]
    temp_list = open(filename, "r").readlines()[1:]
    temp_list = [t.replace("\r\n", "") for t in temp_list]
    # content = [[[",".join(map(str, t[:-1])), t[-1]] for t in line.split(",")] for line in temp_list]
    content = []
    for t in temp_list:
        temp = t.replace("Y","1").replace("N", "0").split(",")
        content.append([",".join(temp[:-1]), float(temp[-1])])

    content = sorted(content, key=lambda x:x[-1])
    return content



# file_names = ["CPM_BDBC_", "CPM_LLVM", "CPM_SQL", "cpm_X264", "CPM_BDBJ_", "CPM_APACHE", ]
file_names = ["CPM_SQL"]#, "CPM_BDBC", ]
# file_names = [ "CPM_BDBC", ]

algorithms = [ "GALE"]
list_of_files = os.listdir("..")

from collections import defaultdict
file_dict = defaultdict(list)
for file_name in file_names:
    for file in list_of_files:
        if file_name in file:
            for algorithm in algorithms:
                if algorithm in file:
                    file_dict[file_name + "#" + algorithm + "#" + file.split("_")[3]].append(file)

for key in file_dict.keys():
    print key, len(file_dict[key])
#
content = []
for f in file_dict["CPM_SQL#GALE#0"]:
    content.extend(read_file_return_list(f))
for c in content:
    print c

print os.getcwd()
get_dataset(file_names[-1])

# for c in content:
#     print c
#
#
# # adding all algorithms together
#
# PERFORMANCE = 0
# GALE = 1
# DE = 2
# NSGAII = 3
#
# for file_name in file_names:
#     maps_content = defaultdict(list)
#     full_content = []
#     for key in [f for f in file_dict.keys() if file_name in f]:
#         print ">> ", key
#         for file in file_dict[key]:
#             file = "../" + file
#             full_content.extend(open(file, "r").readlines())
#         print "Length of full_content: ", len(full_content)
#
#     # print full_content
#
#
#     full_content_dict = defaultdict(list)
#     for s_c in set(full_content):
#         temp = s_c.replace('\n', '').replace(' ', '').split(":")
#         full_content_dict[temp[-1]].append(temp[0])
#         if temp[0] in maps_content.keys():
#             # try:
#             #     assert(maps_content[temp[0]][PERFORMANCE] == temp[-1]), "Something' wrong"
#             # except:
#             #     # Due to different training datasets sometimes the performance scores are different
#             # print maps_content[temp[0]][PERFORMANCE], temp[-1], temp[0]
#             continue
#         else: maps_content[temp[0]] = [temp[-1]]
#     #     if temp[0] in maps_content.keys(): maps_content[temp[0]].append(temp[-1])
#     #     else:
#     #         maps_content[temp[0]] = []
#     #         maps_content[temp[0]].append(temp[-1])
#     #
#     # import numpy as np
#     # for key in maps_content.keys():
#     #     print key,
#     #     print np.percentile([int(float(c)) for c in maps_content[key]], 25),
#     #     print np.percentile([int(float(c)) for c in maps_content[key]], 50),
#     #     print np.percentile([int(float(c)) for c in maps_content[key]], 75)
#
#     print "Length of the full content: ", len(set(full_content))
#     print "Unique entries: ", len(maps_content.keys())
#
#     # for key in [f for f in file_dict.keys() if file_name in f]:
#     #     content = []
#     #     print key
#     #     for file in file_dict[key]:
#     #         file = "../" + file
#     #         content.extend(open(file, "r").readlines())
#     #     # print len(content)
#     #     set_content = set(content)
#     #     # print len(set_content)
#     #
#     #     content_dict = defaultdict(list)
#     #     for s_c in set_content:
#     #         temp = s_c.replace('\n', '').replace(' ', '').split(":")
#     #         # content_dict[temp[-1]].append(temp[0])
#     #         # print temp[0], temp[1], maps_content[temp[0]]
#     #         name_from_filename = key.split('#')[-1]
#     #         if name_from_filename == 'NSGAII':
#     #             print '.',
#     #             maps_content[temp[0]][NSGAII] = 1
#     #         elif name_from_filename == 'DE':
#     #             print "+",
#     #             maps_content[temp[0]][DE] = 1
#     #         elif name_from_filename == 'GALE':
#     #             print "#",
#     #             maps_content[temp[0]][GALE] = 1
#     #         else:
#     #             assert(True == False), "Something's wrong"
#     #             print "Dead"
#     #             exit()
#             # if maps_content[temp[0]][PERFORMANCE] == temp[-1]
#     # print len(content_dict[str(float(min([int(float(p)) for p in content_dict.keys()])))])
#     # print str(float(min([int(float(p)) for p in content_dict.keys()])))
#     # import pdb
#     # pdb.set_trace()
#     # for c in content_dict[str(float(min([int(float(p)) for p in content_dict.keys()])))]:
#     #     print ','.join([str(int(float(cc))) for cc in c.split(',')]), min([int(float(p)) for p in content_dict.keys()])
#
#
#
#     min_score = str(float(min([float(maps_content[content][PERFORMANCE]) for content in maps_content.keys()])))
#     print min_score
#     useful = [content  for content in maps_content.keys() if min_score == maps_content[content][PERFORMANCE]]
#     # print useful
#
#     print len(useful)
#     for content in useful:
#         print ','.join([str(cc) for cc in content.split(',')]), " : ",  float(maps_content[content][0])