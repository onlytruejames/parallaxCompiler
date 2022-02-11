import parallaxCompiler
import json

inFile = open("example.json", "r")
outFile = open("out.html", "w")

inData = inFile.read()
outData = parallaxCompiler.compile(json.loads(inData))

outFile.write(outData)

inFile.close()
outFile.close()