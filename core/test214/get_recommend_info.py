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

rddId2Info, src2dest, dest2src = loadGraphFromFile("WordCountRDDInfo.txt")
rdd2AncestorNodes = get_ancesters(rddId2Info, src2dest, dest2src)

def method1(threahold, rddId2Info):
    res = []
    for key in rddId2Info:
        if rddId2Info[key][1] >= threahold:
            res.append(key)
    return res

def method2(threahold, rddId2Info):
    res = []
    for key in rddId2Info:
        c = rddId2Info[key][1]
        f = len(rdd2AncestorNodes[key])
        if c * f >= threahold:
            #print(key, c * f)
            res.append(key)
    return res

def method3(threahold, method, rddId2Info):
    # rdds_recompute_count_dict = {}
    # for key in rddId2Info:
    #     recompute_times = rddId2Info[key][1]
    #     if recompute_times >= threahold:
    #         rdds_recompute_count_dict[recompute_times] = rdds_recompute_count_dict.get(recompute_times, []) + [key]
    # for key in rdds_recompute_count_dict:
    #     rdds_recompute_count_dict[key].sort(reverse=True)

    # For each iteration, only persist the child with largest rdd id among the rdds that have recompute count larger than specific threahold.
    rddId2Info = copy.deepcopy(rddId2Info)
    rdds_threahold = method(threahold, rddId2Info)
    rdds_threahold.sort()
    while rdds_threahold:
        child = rdds_threahold.pop()
        parents = rdd2AncestorNodes[child]
        for parent in parents:
            val = rddId2Info[parent][1] - rddId2Info[child][1]
            if val >= 0:
                rddId2Info[parent][1] = val
        rddId2Info[child][1] = 0
        rdds_threahold = method(threahold, rddId2Info)
        rdds_threahold.sort()
        print("Persist rdd id:", child)

def main():
    print("Persist with method 1:",method1(2, rddId2Info))
    print("Persist with method 2:",method2(5, rddId2Info))
    print("Persist with method 1 with improvement:")
    method3(2, method1, rddId2Info)
    print("Persist with method 2 with improvement:")
    method3(5, method2, rddId2Info)

main()