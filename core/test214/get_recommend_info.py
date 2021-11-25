from collections import deque
import collections
import copy
def loadGraphFromFile(filename):
    rddId2Info, src2dest, dest2src = {}, {}, {}
    with open(filename) as f:
        for line in f:
            line = line.strip().split("\t")
            rddId = int(line[0])
            parentIDList = list(map(int, line[1].split(","))) if line[1] else []
            name, recomputeCount, totalUsedCount = line[2], int(line[4]), int(line[5])
            rddId2Info[rddId] = [name, recomputeCount, totalUsedCount]
            for pid in parentIDList:
                if pid not in src2dest:
                    src2dest[pid] = []
                src2dest[pid].append(rddId)
                if rddId not in dest2src:
                    dest2src[rddId] = []
                dest2src[rddId].append(pid)
    return rddId2Info, src2dest, dest2src

def get_ancesters(rddId2Info, src2dest, dest2src):
    leafNode = set(dest2src.keys()).difference(set(src2dest.keys()))
    rdd2AncestorNodes = {}
    queue = deque(leafNode)
    def dfs(node):
        if node in rdd2AncestorNodes:
            return rdd2AncestorNodes[node]
        rdd2AncestorNodes[node] = set([node])
        for parentRDD in dest2src.get(node, []):
            dfs(parentRDD)
            rdd2AncestorNodes[node] |= rdd2AncestorNodes[parentRDD]
        return rdd2AncestorNodes[node]
    for node in leafNode:
        dfs(node)
    return rdd2AncestorNodes

rddId2Info, src2dest, dest2src = loadGraphFromFile("CovidInfo_Nopersist.txt")
rdd2AncestorNodes = get_ancesters(rddId2Info, src2dest, dest2src)

def simpleThresholdRecommendation(threshold, rddId2Info):
    res = []
    for key in rddId2Info:
        if rddId2Info[key][1] >= threshold:
            res.append(key)
    return res

def computationCostRecommendation(threshold, rddId2Info):
    res = []
    for key in rddId2Info:
        c = rddId2Info[key][1]
        f = len(rdd2AncestorNodes[key])
        if c * f >= threshold:
            #print(key, c * f)
            res.append(key)
    return res

def onlyChild(threshold, method, rddId2Info):
    # rdds_recompute_count_dict = {}
    # for key in rddId2Info:
    #     recompute_times = rddId2Info[key][1]
    #     if recompute_times >= threshold:
    #         rdds_recompute_count_dict[recompute_times] = rdds_recompute_count_dict.get(recompute_times, []) + [key]
    # for key in rdds_recompute_count_dict:
    #     rdds_recompute_count_dict[key].sort(reverse=True)

    # For each iteration, only persist the child with largest rdd id among the rdds that have recompute count larger than specific threshold.
    rddId2Info = copy.deepcopy(rddId2Info)
    rdds_threshold = method(threshold, rddId2Info)
    rdds_threshold.sort()
    while rdds_threshold:
        child = rdds_threshold.pop()
        parents = rdd2AncestorNodes[child]
        for parent in parents:
            val = rddId2Info[parent][1] - rddId2Info[child][1]
            if val >= 0:
                rddId2Info[parent][1] = val
        rddId2Info[child][1] = 0
        rdds_threshold = method(threshold, rddId2Info)
        rdds_threshold.sort()
        print(f"Persist rdd id {child} and Name {rddId2Info[child][0]}")

if __name__ == "__main__":
    rddIds = simpleThresholdRecommendation(2, rddId2Info)
    nameList = [rddId2Info[child][0] for child in rddIds]
    print(f"Persist with method 1: {rddIds}, {nameList}")
    rddIds = computationCostRecommendation(5, rddId2Info)
    nameList = [rddId2Info[child][0] for child in rddIds]
    print(f"Persist with method 2: {rddIds}, {nameList}")
    print("Persist with method 1 with improvement:")
    onlyChild(2, simpleThresholdRecommendation, rddId2Info)
    print("Persist with method 2 with improvement:")
    onlyChild(5, computationCostRecommendation, rddId2Info)