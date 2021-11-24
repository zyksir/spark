from collections import deque
def loadGraphFromFile(filename):
    rddId2Info, src2dest, dest2src = {}, {}, {}
    with open(filename) as f:
        for line in f:
            line = line.strip().split("\t")
            rddId = int(line[0])
            parentIDList = list(map(int, line[1].split(","))) if line[1] else []
            name, recomputeCount, totalUsedCount = line[2], int(line[4]), int(line[5])
            rddId2Info[rddId] = (name, recomputeCount, totalUsedCount)
            for pid in parentIDList:
                if pid not in src2dest:
                    src2dest[pid] = []
                src2dest[pid].append(rddId)
                if rddId not in dest2src:
                    dest2src[rddId] = []
                dest2src[rddId].append(pid)
    return rddId2Info, src2dest, dest2src

rddId2Info, src2dest, dest2src = loadGraphFromFile("./core/test214/WordCountRDDInfo.txt")
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



