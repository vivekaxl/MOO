

import os

def read_file_return_list(filename):
    return open("../"+filename, "r").readlines()

def get_dataset(filename):
    convert_names = {"CPM_APACHE": "../../../Problems/CPM/data/Apache_AllMeasurements.csv",
                     "CPM_BDBC": "../../../Problems/CPM/data/BDBC_AllMeasurements.csv",
                     "CPM_BDBJ": "../../../Problems/CPM/data/BDBJ_AllMeasurements.csv",
                     "CPM_LLVM": "../../../Problems/CPM/data/LLVM_AllMeasurements.csv",
                     "CPM_SQL": "../../../Problems/CPM/data/SQL_AllMeasurements.csv",
                     "cpm_X264": "../../../Problems/CPM/data/x264_AllMeasurements.csv"
                     }
    filename = convert_names[filename]
    temp_list = open(filename, "r").readlines()[1:]
    temp_list = [t.replace("\r\n", "") for t in temp_list]
    # content = [[[",".join(map(str, t[:-1])), t[-1]] for t in line.split(",")] for line in temp_list]
    content = {}
    rank_list = []
    for t in temp_list:
        temp = t.replace("Y","1").replace("N", "0").split(",")
        content[",".join(temp[:-1])] = float(temp[-1])
        rank_list.append(int(float(temp[-1])))

    return content, sorted(rank_list)


def get_ranks(file_names):
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

    count = 0
    ranks = defaultdict(list)
    for key in file_dict.keys():
        content = []
        for f in file_dict[key]: content.extend(read_file_return_list(f))
        dataset, rank_list = get_dataset(file_names[-1])
        transform_content = [c.split(":")[0].replace(" ", "") for c in content]

        for tc in transform_content:
            if key in ranks.keys():
                try:
                    ranks[key].extend([rank_list.index(int(float(dataset[tc])))])
                except:
                    count += 1
                    pass
            else:
                # print "> "*10
                # try:
                try:
                    ranks[key] = [rank_list.index(int(float(dataset[tc])))]
                except:
                    print tc
                    count += 1
                    pass

    # print len(ranks.keys())
    # raw_input()
    best_scores = []
    for key in ranks.keys():
        # print key, ranks[key]
        best_scores.append(sorted(ranks[key])[0])
    # raw_input()
    print "count: ", count
    return best_scores

if __name__ == "__main__":
    file_names = ["CPM_BDBJ",]# "cpm_X264", "CPM_APACHE", "CPM_BDBC", "CPM_LLVM", "CPM_SQL",]
    for file_name in file_names:
        print file_name, get_ranks([file_name])