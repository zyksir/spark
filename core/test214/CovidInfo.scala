sc.enableCacheHelper()
val inputFile = "./core/test214/covid19_cases.txt"
val covidCaseData = sc.textFile(inputFile).
  filter(!_.contains("Date")).
  map(line => line.split(",")).
  setName("covidCaseData")
val countryNum = covidCaseData.map(line => line(1)).distinct().count
println(f"We got data from $countryNum countries ")
var avgNewCasesPerCountry = covidCaseData.
  map(line => (line(1), line(2).toInt)).
  mapValues((_, 1)).
  reduceByKey((x, y) => (x._1 + y._1, x._2 + y._2)).
  mapValues(x => x._1 / x._2).setName("avgNewCasesPerCountry")
avgNewCasesPerCountry.foreach(println)

val newDeathsPerDay = covidCaseData.
  map(line => (line(0), line(3).toInt)).
  reduceByKey(_+_).setName("newDeathsPerDay")
newDeathsPerDay.foreach(println)

println("Total Deaths before 12/25/2020:")
println(newDeathsPerDay.filter(_._1 < "12/25/2020").map(_._2).reduce(_ + _))
println("Dates with Deaths lower than 3000:")
newDeathsPerDay.filter(_._2 < 3000).collect().foreach(println)
println("Total Deaths in Dec 2020: \n")
println(newDeathsPerDay.map(_._2).reduce(_+_))

var allRDDIno = sc.AllRDDStorageInfo()
import java.io._
val pw = new PrintWriter(new File("./core/test214/CovidInfo_Nopersist.txt" ))
allRDDIno.sortWith(_.id < _.id).
  foreach(x => pw.write(f"${x.id}\t${x.parentIds.mkString(",")}\t${x.name}\t${x.isCached}\t${x.recomputeCount}\t${x.totalUsedCount}\n"))
pw.close