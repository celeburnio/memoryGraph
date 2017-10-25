#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import plotly
from plotly.graph_objs import *

processList = []
processList.append("tniISManager")
processList.append("networkManager")
processList.append("tniListenerKey")
processList.append("tniMediaPlayer")
processList.append("httpproxy")
processList.append("profileManager")
processList.append("bwManager")
processList.append("epgManager")
processList.append("cdvrManager")
processList.append("patchManager")
processList.append("audiences")
processList.append("drmManager")
processList.append("qualityMeasure")
processList.append("infopush_clien")
processList.append("friendlyReset")
processList.append("tr69")
processList.append("WidgetManager")

#####################
# class definitions #
#####################


class ProcessStats:
        name = ""
        pid = 0
        timestamp = []
        nThreads = []
        IncThreads = []
        VmSize = []
        IncVmSize = []
        VmRSS = []
        IncVmSize = []
        VmData = []
        IncVmData = []
        VmLib = []
        VmPte = []

        def __init__(self, process):
                self.name = process
                self.pid = 0
                self.timestamp = []
                self.nThreads = []
                self.IncThreads = []
                self.VmSize = []
                self.IncVmSize = []
                self.VmRSS = []
                self.IncVmSize = []
                self.VmData = []
                self.IncVmData = []
                self.VmLib = []
                self.VmPte = []


class GlobalMemoryStats:
        timestamp = []
        totalFree = []
        free = []
        cached = []
        swap = []
        tmp = []

        def __init__(self, name):
                self.name = name
                self.timestamp = []
                self.totalFree = []
                self.free = []
                self.cached = []
                self.swap = []
                self.tmp = []

##############################
# functions to proccess text #
##############################


def eraseSpaces(text):
        spaces = 0
        aux = ""
        i = 0
        while i < len(text):
                if (text[i] == ' '):
                        if (spaces == 0):
                                spaces = 1
                                aux += text[i]
                else:
                        spaces = 0
                        aux += text[i]
                i += 1
        return aux


def eraseParenthesis(text):
        aux = ""
        aux = text.replace('(', '')
        aux = aux.replace(')', '')
        return aux


def formatLine(text):
        aux = ""
        aux = text.replace('\t', '')
        aux = aux.replace('#', '')
        aux = eraseSpaces(aux)
        aux = aux.lstrip()
        aux = eraseParenthesis(aux)
        return aux.replace(' ', ',')


def searchProcess(process):
        if process in processList:
                return True

        print "The process available are the following:"
        print processList
        return False


def extracDataForProcess(process, paintGraph=True):
        filenameForExcelProcess = "format_" + process + "_" + arguments.logsFile
        filenameForExcelProcess = filenameForExcelProcess.replace('.txt', '.csv')
        filenameGraphForProcess = "graph_" + process + "_" + arguments.logsFile
        filenameGraphForProcess = filenameGraphForProcess.replace('.txt', '.html')

        processStats = ProcessStats(process)
        header = "Time,process,pid,nThreads,IncThreads,VmSize,IncVmSize,VmRSS,IncVmRSS,VmData,IncVmData,VmLib,VmPte\n"

        search_words = ['MEMORY STATUS', (process + "  ")]
        with open(arguments.logsFile) as oldfile, open('aux_process.txt', 'w') as newfile:
                for line in oldfile:
                        if any(word in line for word in search_words):
                                newfile.write(line)

        oldfile.close()
        newfile.close()

        newfile = open('aux_process.txt', 'r')

        excelfileForProcess = open(filenameForExcelProcess, 'w')
        excelfileForProcess.write(header)
        for line in newfile:
                if (line.count('MEMORY STATUS') == 1):
                        aux = line.replace('=', '')
                        aux = aux.replace(',', '')
                        aux = aux.replace('MEMORY STATUS:', '')
                        aux = aux.replace('#', '')
                        aux = aux.replace('\n', '')
                        aux = aux.lstrip()
                        aux = aux.rstrip()
                        excelfileForProcess.write(aux + ',')
                        processStats.timestamp.append(aux)
                        continue
                excelfileForProcess.write(formatLine(line))
                aux = formatLine(line)
                array_aux = []
                array_aux = aux.split(',')
                processStats.pid = array_aux[1]
                processStats.nThreads.append(array_aux[2])
                processStats.IncThreads.append(array_aux[3])
                processStats.VmSize.append(array_aux[4])
                processStats.IncVmSize.append(array_aux[5])
                processStats.VmRSS.append(array_aux[6])
                processStats.IncVmSize.append(array_aux[7])
                processStats.VmData.append(array_aux[8])
                processStats.IncVmData.append(array_aux[9])
                processStats.VmLib.append(array_aux[10])
                processStats.VmPte.append(array_aux[11])

        excelfileForProcess.close()
        newfile.close()

        os.remove('aux_process.txt')

        if paintGraph is True:
                plotTitle = process + " process VmData"

                trace1 = {
                        "x": processStats.timestamp,
                        "y": processStats.VmData,
                        "mode": "lines",
                        "name": "Process Memory",
                        "text": processStats.VmData,
                        "type": "scatter"
                }

                data = Data([trace1])

                layout = {
                        "autosize": True,
                        "dragmode": "zoom",
                        "hovermode": "closest",
                        "title": plotTitle,
                        "xaxis": {
                                "autorange": True,
                                "range": [0, len(processStats.timestamp)],
                                "title": "Time",
                                "type": "category",
                                "tickangle": 330
                        },
                        "yaxis": {
                                "autorange": True,
                                "range": [min(processStats.VmData), max(processStats.VmData)],
                                "title": "VmData",
                                "type": "liner"
                        }
                }
                fig = Figure(data=data, layout=layout)
                plotly.offline.plot(fig, filename=filenameGraphForProcess)
        else:
                return processStats


def totalFreeGraph(logFile, paintGraph=True):
        filenameForExcel = "format_" + logFile
        filenameForExcel = filenameForExcel.replace('.txt', '.csv')
        filneameForGraph = "graph_" + logFile
        filneameForGraph = filneameForGraph.replace('.txt', '.html')

        search_words = ['MEMORY STATUS', "TOTAL FREE", "TOTAL Tmp"]
        with open(logFile) as oldfile, open('aux_totalMemory.txt', 'w') as newfile:
                for line in oldfile:
                        if any(word in line for word in search_words):
                                newfile.write(line)

        oldfile.close()
        newfile.close()

        logsFile = open('aux_totalMemory.txt', 'r')
        excelFile = open(filenameForExcel, 'w')
        excelFile.write("Time,TotalFree,Free,Cached,Swap,Tmp\n")
        # ================== MEMORY STATUS: 2016/10/28 16:38:28 =========================================
        # TOTAL FREE:             705656, Free:           592956, Cached:                 112700, Swap:                    0
        # TOTAL Tmp Size: 13668 KB
        globalMemoryStats = GlobalMemoryStats(logFile)
        for line in logsFile:
                aux = line.replace('=', '')
                aux = aux.replace(',', '')
                if (aux.count('MEMORY STATUS') == 1):
                        aux = aux.replace('MEMORY STATUS:', '')
                        aux = aux.replace('#', '')
                        aux = aux.replace('\n', '')
                        aux = aux.lstrip()
                        aux = aux.rstrip()
                        excelFile.write(aux + ',')
                        globalMemoryStats.timestamp.append(aux)
                        continue
                if (aux.count('TOTAL FREE') == 1):
                        aux = aux.replace(':', '')
                        aux = aux.replace('TOTAL FREE', '')
                        aux = aux.replace('Free', '')
                        aux = aux.replace('Cached', '')
                        aux = aux.replace('Swap', '')
                        aux = aux.replace('\n', '')
                        excelFile.write(formatLine(aux) + ',')
                        aux = formatLine(aux)
                        array_aux = aux.split(',')
                        globalMemoryStats.totalFree.append(array_aux[0])
                        globalMemoryStats.free.append(array_aux[1])
                        globalMemoryStats.cached.append(array_aux[2])
                        globalMemoryStats.swap.append(array_aux[3])
                        continue
                if (aux.count('TOTAL Tmp Size') == 1):
                        aux = aux.replace(':', '')
                        aux = aux.replace('TOTAL Tmp Size', '')
                        aux = aux.replace('KB', '')
                        excelFile.write(formatLine(aux))
                        globalMemoryStats.tmp.append(aux)
                        continue

        excelFile.close()
        logsFile.close()
        os.remove('aux_totalMemory.txt')

        if paintGraph is True:
                trace1 = {
                        "x": globalMemoryStats.timestamp,
                        "y": globalMemoryStats.totalFree,
                        "mode": "lines",
                        "name": "TotalFree",
                        "text": globalMemoryStats.totalFree,
                        "type": "scatter",
                }

                data = Data([trace1])

                layout = {
                        "autosize": True,
                        "dragmode": "zoom",
                        "hovermode": "closest",
                        "title": "TotelFree memory",
                        "xaxis": {
                                "autorange": True,
                                "range": [0, len(globalMemoryStats.timestamp)],
                                "title": "Time",
                                "type": "category",
                                "tickangle": 330
                        },
                        "yaxis": {
                                "autorange": True,
                                "range": [min(globalMemoryStats.totalFree), max(globalMemoryStats.totalFree)],
                                "title": "TotalFree",
                                "type": "liner"
                        }
                }
                fig = Figure(data=data, layout=layout)
                plotly.offline.plot(fig, filename=filneameForGraph)
        else:
                return globalMemoryStats


def twoFilesGrapgh(file1, file2):
        trace1 = {
                "x": file1.timestamp,
                "y": file1.totalFree,
                "mode": "lines",
                "name": file1.name,
                "text": file1.totalFree,
                "type": "scatter",
        }
        trace2 = {
                "x": file1.timestamp,
                "y": file2.totalFree,
                "mode": "lines",
                "name": file2.name,
                "text": file2.totalFree,
                "type": "scatter",
        }
        data = Data([trace1, trace2])

        layout = {
                "autosize": True,
                "dragmode": "zoom",
                "hovermode": "closest",
                "title": "TotelFree memory comparation",
                "xaxis": {
                        "autorange": True,
                        "range": [0, len(max(file1.timestamp, file2.timestamp))],
                        "title": "Time",
                        "type": "category",
                        "tickangle": 330
                },
                "yaxis": {
                        "autorange": True,
                        "range": [min(file1.totalFree, file2.totalFree), max(file1.totalFree, file2.totalFree)],
                        "title": "TotalFree",
                        "type": "liner"
                }
        }
        fig = Figure(data=data, layout=layout)
        plotly.offline.plot(fig, filename="twoFilesComparation.html")


def totalFreeAndProcessGraph(globalMemoryStats, processToPaintStats):
        trace1 = {
                "x": globalMemoryStats.timestamp,
                "y": globalMemoryStats.totalFree,
                "mode": "lines",
                "name": globalMemoryStats.name,
                "type": "scatter",
        }
        trace2 = {
                "x": processToPaintStats.timestamp,
                "y": processToPaintStats.VmData,
                "mode": "lines",
                "name": processToPaintStats.name,
                "type": "scatter",
                "yaxis": "y2"
        }
        data = Data([trace1, trace2])

        layout = {
                "title": "TotelFree memory comparation",
                "xaxis": {
                        "autorange": True,
                        "range": [0, len(max(globalMemoryStats.timestamp, processToPaintStats.timestamp))],
                        "title": "Time",
                        "type": "category",
                        "tickangle": 330
                },
                "yaxis": {
                        "autorange": True,
                        "range": [min(globalMemoryStats.totalFree), max(globalMemoryStats.totalFree)],
                        "side": "left",
                        "title": "TotalFree",
                        "type": "liner"
                },
                "yaxis2": {
                        "autorange": True,
                        "range": [min(processToPaintStats.VmData), max(processToPaintStats.VmData)],
                        "title": processToPaintStats.name + " VmData",
                        "overlaying": 'y',
                        "side": "right",
                        "type": "liner"
                }
 
        }
        fig = Figure(data=data, layout=layout)
        filenameForGraph=globalMemoryStats.name + "_Vs_" + processToPaintStats.name + ".html"
        plotly.offline.plot(fig, filename=filenameForGraph)


if __name__ == "__main__":
        from argparse import ArgumentParser

        parser = ArgumentParser()
        parser.add_argument("logsFile", help="Log file to analyze.", type=str)
        parser.add_argument("--process", help="If you want to see the graph of one process", choices=processList, type=str)
        parser.add_argument("--compare", help="Log file from other stb to compare", type=str)
        parser.add_argument("--compareProcess", help="If you want to paint the graph of one process with the totalFree", type=str)
        arguments = parser.parse_args()

        if (arguments.process):
                if (searchProcess(arguments.process)):
                        extracDataForProcess(arguments.process, True)
                else:
                        print "There is no process " + arguments.process
        elif (arguments.compare):
                file1 = totalFreeGraph(arguments.logsFile, False)
                file2 = totalFreeGraph(arguments.compare, False)
                twoFilesGrapgh(file1, file2)

        elif (arguments.compareProcess):
            if kk:


                if (searchProcess(arguments.compareProcess)):
                        processToPaintStats = extracDataForProcess(arguments.compareProcess, False)
                        globalMemoryStats = totalFreeGraph(arguments.logsFile, False)
                        totalFreeAndProcessGraph(globalMemoryStats, processToPaintStats)

                else:
                        print "There is no process " + arguments.compareProcess
 
        else:
                totalFreeGraph(arguments.logsFile, True)
