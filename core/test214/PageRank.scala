sc.enableCacheHelper()
val iters = 10
val lines = spark.sparkContext.textFile("./core/test214/pagerank_data.txt")
val links = lines.map{ s =>
    val parts = s.split("\\s+")
    (parts(0), parts(1))
}.distinct().groupByKey() //.cache()
var ranks = links.mapValues(v => 1.0)

for (i <- 1 to iters) {
    val contribs = links.join(ranks).values.flatMap{ case (urls, rank) =>
    val size = urls.size
    urls.map(url => (url, rank / size))
    }
    ranks = contribs.reduceByKey(_ + _).mapValues(0.15 + 0.85 * _)
}

val output = ranks.collect()
output.foreach(tup => println(s"${tup._1} has rank:  ${tup._2} ."))

var allRDDIno = sc.AllRDDStorageInfo()
import java.io._
val pw = new PrintWriter(new File("./core/test214/PageRankRDDInfo_Nopersist.txt" ))
allRDDIno.sortWith(_.id < _.id).
  foreach(x => pw.write(f"${x.id}\t${x.parentIds.mkString(",")}\t${x.name}\t${x.isCached}\t${x.recomputeCount}\t${x.totalUsedCount}\n"))
pw.close