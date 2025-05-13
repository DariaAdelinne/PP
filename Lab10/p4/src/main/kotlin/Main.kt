package com.pp.laborator

import java.io.File
import java.util.concurrent.Executors
import java.util.concurrent.TimeUnit

fun main(args: Array<String>) {
    // 1) preluam calea directorului din args sau folosim implicit "Fisiere"
    val dirPath = if (args.isNotEmpty()) args[0] else "Fisiere"
    val dir = File(dirPath)
    if (!dir.isDirectory) {
        println("Eroare: $dirPath nu e un director valid.")
        return
    }

    // 2) listam toate fisierele din director
    val files = dir.listFiles { f -> f.isFile } ?: emptyArray()
    if (files.isEmpty()) {
        println("Nu exista fisiere in $dirPath.")
        return
    }

    // 3) cream un thread-pool fix cu 4 thread-uri
    val poolSize = 4
    val pool = Executors.newFixedThreadPool(poolSize)

    println("Incep procesarea a ${files.size} fisiere pe $poolSize thread-uri...\n")

    // 4) pentru fiecare fisier, submit-iam un Runnable care il proceseaza
    files.forEach { file ->
        pool.submit {
            // exemplu de lucru: citim continutul si afisam numarul de linii
            val lines = file.readLines()
            println("Thread ${Thread.currentThread().name} -> '${file.name}' are ${lines.size} linii")
        }
    }

    // 5) nu mai acceptam sarcini noi si asteptam finalizarea
    pool.shutdown()
    pool.awaitTermination(1, TimeUnit.MINUTES)

    println("\nToate fisierele au fost procesate.")
}
