import org.apache.spark._
import org.apache.spark.SparkContext._
import org.slf4j.{Logger, LoggerFactory}

sc.enableCacheHelper()
sc.setEnableCacheThreshold(0)
val gradeFile = "./core/test214/grades.csv"
val gradeData = spark.sparkContext.textFile(gradeFile)
val studentCount = gradeData.map(line => line.split(",")(1)).distinct().count
val coursesCount = gradeData.map(line => line.split(",")(2)).distinct().count
println("\nCourses Average Score: \n")
var averageGrade = gradeData.
  filter(!_.contains("Name")).
  map(line => (line.split(",")(2), line.split(",")(3).toInt)).
  mapValues((_, 1)).
  reduceByKey((x, y) => (x._1 + y._1, x._2 + y._2)).
  mapValues(x => x._1 / x._2)
averageGrade.foreach(println)
val averageData = gradeData.
  filter(!_.contains("Name")).
  map(line => line.split(",")).
  map(line => ((line(0), line(1)), line(3).toInt)).
  mapValues((_, 1)).
  reduceByKey((x, y) => (x._1 + y._1, x._2 + y._2)).
  mapValues(x => x._1/x._2)
println("\nStudent grade lower than 87: \n")
averageData.filter(_._2 < 87).collect().foreach(println)
println("\nStudent grade lower than 91: \n")
averageData.filter(_._2 > 91).collect().foreach(println)
var allRDDIno = sc.AllRDDStorageInfo()
allRDDIno.map(x => (x.recomputeCount, x.totalUsedCount, x.name, x.parentIds, x.id))
