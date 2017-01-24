#!/usr/bin/python 

################################################### READ ME ################################################### 
#
# This script is for extracting methylation level of specific genomic regions of five samples from McGroger Project.
# Input file type supports coverage file (.cov) extracted from methylation_extractor from bismark suite.
# Output file can be subjected to methylDotPlot.R directly.
#
# author: Guosong Wang (Ph.D student 2nd year), Department of Animal Science, Texas A&M University
# Contact: guosong.wang@tamu.edu
###############################################################################################################

import sys
from optparse import OptionParser


class ExtractPromoterMethyl:

	def call_methyl(self, options):

		samples = []

		inputs = sys.argv[-1].split(',')

		for input in inputs:
			mysample = open(input, 'r')
			samples.append(mysample)

		chrom = options.chromosome
		start = options.start
		end = options.end
		methylationLVL = options.methyl_lvl
		self.output = open(options.output, 'w')

		methylCollections = []

		i = 1

		for sample in samples:

			methylationINFO = ''

			for line in sample:
				line = line.rstrip()
				parts = line.split('\t')
				chromosome = str(parts[0])
				position = int(parts[1])
				if start <= position <= end and chromosome == chrom:
					total = int(parts[2]) + int(parts[3])
					if total != 0:
						percentage = float(parts[2]) / (float(parts[2]) + float(parts[3]))
					else:
						percentage = 0

					if i == 1:

						if percentage >= methylationLVL:
							methylationINFO = methylationINFO + '\t' + 'Y'
						else:
							methylationINFO = methylationINFO + '\t' + 'N'

					else:
						if percentage >= methylationLVL:
							methylationINFO = methylationINFO + '\t' + 'Y'
						else:
							methylationINFO = methylationINFO + '\t' + 'N'

			methylationINFO = methylationINFO.lstrip('\t')
			methylCollections.append(methylationINFO)

			i += 1

			sample.close()

		print>>self.output, 'status' + '\t' + 'sample' + '\t' + 'position'

		n = 1

		for collection in methylCollections:

			details = collection.split('\t')
			total_positions = len(details)
			for x in range(0, total_positions):
				print>>self.output, str(details[x]) + '\t' + str(n) + '\t' + str(x + 1)

			n += 1

		self.output.close()

	def get_plot(self, options):

		readfile = open(options.output, 'r')
		position_numbers = []
		for line in readfile:
			if not line.startswith('status'):
				parts = line.split('\t')
				position_numbers.append(int(parts[-1]))

		max_number = max(position_numbers)

		self.rscript = open(options.path + 'methyl_dot.R', 'w')

		print>>self.rscript, 'library(ggplot2)\n'

		read_file = "data<-read.table(file='" + str(options.output) + "',sep = '\t',header=T,row.names=NULL)\n"
		print>>self.rscript, read_file

		print>>self.rscript, "colnames(data) <- c('status', 'sample', 'position')"
		print>>self.rscript, 'data$sample <- ((data$sample - 1)/' + str(len(sys.argv[-1].split(','))) + ') + 1'
		print>>self.rscript, 'p <- ggplot(data, aes(position, sample, shape = status)) + geom_point(position = "identity", size = 10) + scale_shape_manual(values = c(1, 19))'
		print>>self.rscript, 'p <- p + ylim(0.8, %s)' % str((len(sys.argv[-1].split(',')) * 0.2) + 1.2)
		print>>self.rscript, 'p <- p + theme_bw()  + theme(legend.position = "none")'
		print>>self.rscript, 'p <- p + theme(axis.title.x=element_blank(), axis.text.x=element_blank(), axis.ticks.x=element_blank())'
		print>>self.rscript, 'p <- p + theme(axis.title.y=element_blank(), axis.text.y=element_blank(), axis.ticks.y=element_blank())'

		heights = float(len(sys.argv[-1].split(','))) * 0.6
		width = float(max_number) * 0.4
		plot_saving = 'ggsave(filename = "' + str(options.path) + 'Methyl_Dot.png", width = ' + str(width) + ', height = ' + str(heights) + ')'
		print>>self.rscript, plot_saving

		self.rscript.close()


def main():
	usage = "Usage: %prog [options] input [input1,input2,input3...]"
	parser = OptionParser(usage=usage)
	parser.add_option('-o', '--output', action='store', type='string', dest='output',
	                  help='FULL PATH of output file containing methylation information for the desired region. ')
	parser.add_option('-c', '--chromosome', action='store', type='string', dest='chromosome',
	                  help='Define your desired chromosome. ')
	parser.add_option('-s', '--start', action='store', type='int', dest='start',
	                  help='Define the start position of your desired region. ')
	parser.add_option('-e', '--end', action='store', type='int', dest='end',
	                  help='Define the end position of your desired region. ')
	parser.add_option('-l', '--level', action='store', type='float', dest='methyl_lvl',
	                  help='Define the level of methylation to be consider as methylated site. Range: 0 to 1. ')
	parser.add_option('-r', '--rscript', action='store_true', dest='verbose',
	                  help='Whether to call plotting function or not. (Default=OFF)')
	parser.add_option('-p', '--path', action='store', type='string', dest='path',
	                  help='Define the path for rscript and plot storing. Must be a directory ended with a "/".  ')
	(options, args) = parser.parse_args()

	ExtractPromoterMethyl().call_methyl(options)

	if options.verbose:
		ExtractPromoterMethyl().get_plot(options)


if __name__ == '__main__':

	try:
		main()
	except KeyboardInterrupt:
		sys.stderr.write("User interrupts me! See you!\n")
		sys.exit(0)
