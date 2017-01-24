library(ggplot2)

data<-read.table(file='/data/macee77aggie/test.txt',sep = '	',header=T,row.names=NULL)

colnames(data) <- c('status', 'sample', 'position')

		data$sample <- ((data$sample - 1)/5) + 1

		p <- ggplot(data, aes(position, sample, shape = status)) + geom_point(position = 'identity', size = 12) +
		scale_shape_manual(values = c(1, 19))

		p <- p + ylim(0.8, 2.0)

		p <- p + theme_bw()  + theme(legend.position = "none")

		p <- p + theme(axis.title.x=element_blank(), axis.text.x=element_blank(), axis.ticks.x=element_blank())

		p <- p + theme(axis.title.y=element_blank(), axis.text.y=element_blank(), axis.ticks.y=element_blank())

		p <- p + main('Methylation Status Dot Plot')
 
ggsave(filename = "/data/macee77aggie/test.png", width = 10, height = 1.2)
