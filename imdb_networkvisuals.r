############################################
#bringing things in
############################################


#initial installs
#####
rm(list = ls())
library(NetPathMiner)
library(readr)
library(igraph)
library(ggraph)
library(RColorBrewer)


#setting things up
#####
##set working directory
#setwd(location of folder where edge/vertices files are)
setwd("C:/Users/")


##reading in the files
edge_file <- read.csv("edges.csv", header = T)
vertex_file <- read.csv("vertices.csv", header = T)

##creating data frames
edges <- data.frame(edge_file)
vertices <- data.frame(vertex_file)


##creating a graph object
film_person_graph_original <- graph_from_data_frame(edges, directed = FALSE,vertices = vertices)


##removing loops and edges that are connected multiple times
##theoretically, this shouldn't change anything
film_person_graph <- simplify(film_person_graph_original)


#making a bipartite graph
#####
##adding a graph attribute on vertices to signify which group they're in (for this, film or person)
V(film_person_graph)$type <- bipartite.mapping(film_person_graph)$type


##making films and people different colors on the overall plot
V(film_person_graph)$color = ifelse(V(film_person_graph)$type, 'blue','green')
V(film_person_graph)$frame.color <-  "gray"
V(film_person_graph)$size <- 2

##splitting overall graph to two bipartite graphs
g.bp <- bipartite.projection(film_person_graph)

###actually making those graphs
g.films_all <- (g.bp$proj1)
g.people_all <- (g.bp$proj2)


##getting rid of isolates on graphs
g.films <- delete.vertices(g.films_all, which(degree(g.films_all)==0))
g.people <- delete.vertices(g.people_all, which(degree(g.people_all)==0))


############################################
#just some basic stats
############################################


# ##stats about big network
# print(paste0('num vertices: ', gorder(g.films_all)))
# print(paste0('num edges: ', gsize(g.films_all)))
# edge_density(g.films_all)
# hist(degree(g.films_all), breaks = seq(0,20,2))

# for (att in vertex_attr_names(g.films_all)) {
#   print(att)
#   print(summary(vertex_attr(g.films_all, att)))
#   freq <- table(vertex_attr(g.films_all, att))
#   print(freq[order(freq, decreasing = TRUE)][1:5])
# }
# 
# 
# ratings = vertex_attr(g.films_all, 'rating')
# imdb_ratings = vertex_attr(g.films_all, 'imdb_rating')
# plot(ratings, imdb_ratings,
#      xlim = c(0,10), ylim = c(0,10),
#      main = paste0('intercept= ', round(coefficients(lm(imdb_ratings~ratings)),2)[1], ' ',
#                    'slope= ', round(coefficients(lm(imdb_ratings~ratings)),2)[2])
# )
# par(xpd=FALSE)
# abline(coef = c(0,1), col = 'red')
# abline(lm(imdb_ratings~ratings), col = 'blue')


##stats about network without isolates
###basics
print(paste0('num vertices: ', gorder(g.films)))
print(paste0('num edges: ', gsize(g.films)))
###more basics
edge_density(g.films)
hist(degree(g.films), breaks = seq(0,20,2))
##attribute specific
for (att in vertex_attr_names(g.films)) {
  print(att)
  print(summary(vertex_attr(g.films, att)))
  freq <- table(vertex_attr(g.films, att))
  print(freq[order(freq, decreasing = TRUE)][1:5])
}


##plotting my ratings v imdb's
ratings = vertex_attr(g.films, 'rating')
imdb_ratings = vertex_attr(g.films, 'imdb_rating')
plot(ratings, imdb_ratings,
     xlim = c(0,10), ylim = c(0,10),
     main = paste0('intercept= ', round(coefficients(lm(imdb_ratings~ratings)),2)[1], ' ',
                   'slope= ', round(coefficients(lm(imdb_ratings~ratings)),2)[2])
)
par(xpd=FALSE)
abline(coef = c(0,1), col = 'red')
abline(lm(imdb_ratings~ratings), col = 'blue')


############################################
#visualizing the networks
############################################


#simple
plot(g.films_all)
plot(g.films)


##prettying the film plot
V(g.films)$label.cex <- .4
V(g.films)$size <- 2
V(g.films)$label.dist <- .5
V(g.films)$label.degree <- pi/2


##there's a lot of layout algorithms
# plot(g.films, layout = layout.reingold.tilford(g.films, circular =T))
# plot(g.films, layout = layout.fruchterman.reingold(g.films, niter = 1000))
# plot(g.films, layout = layout_with_kk(g.films))
plot(g.films, layout = layout_nicely(g.films))


####
#communities
############################################


#finding communities based on a specific clustering method, but there are others
comms <- cluster_walktrap(g.films)


##adding communities to graph
g.films = set_vertex_attr(g.films,'community',,comms$membership)
##increasing strength and choosing a layout algorithm
g.layout <- layoutVertexByAttr(g.films, "community", cluster.strength = 250, layout = layout_with_fr)


## simple plotting with the communities highlighted
plot(comms, g.films, layout = g.layout)
#plotting with the communities denoted by vertex color, but not highlighted
plot(g.films, layout = g.layout, vertex.colors = membership(comms))


##actually finding which communities have with films
interesting_comms <- V(g.films)["Porco Rosso(1992)","Eraserhead(1977)"]$community
##ranking communities by size
comm_sizes <- table(vertex_attr(g.films, 'community'))[order(table(vertex_attr(g.films, 'community')), decreasing = TRUE)]


##making graphs of communities
g.films_larger_comm <- delete.vertices(g.films, which(V(g.films)$community!=rownames(comm_sizes)[1]))
g.films_miyazaki <- delete.vertices(g.films, which(V(g.films)$community!=interesting_comms[1]))
g.films_lynch <- delete.vertices(g.films, which(V(g.films)$community!=interesting_comms[2]))

potential_titles = c('Large Networks',"Miyazaki's Network",'Lynchian Network', 'Film Network')

##just so you don't have to rename stuff
g.now <- g.films_larger_comm
main_title = potential_titles[1]
#g.now <- g.films_miyazaki
#main_title = potential_titles[2]
#g.now <- g.films_lynch
#main_title = potential_titles[3]
#g.now <- g.films
#main_title = potential_titles[4]


#slightly prettying this graph
V(g.now)$label.dist <- .5
V(g.now)$label.degree <- pi/2
V(g.now)$label.cex = .5
V(g.now)$size <- 5


##stats
###basics
edge_density(g.now)
hist(degree(g.now), breaks = seq(0,20,2))
###attribute specific
for (att in vertex_attr_names(g.now)) {
  print(att)
  print(summary(vertex_attr(g.now, att)))
  freq <- table(vertex_attr(g.now, att))
  print(freq[order(freq, decreasing = TRUE)][1:5])
}
#looking at all films in the community
V(g.now)$name
#plotting the community
plot(g.now, layout = layout_nicely(g.now), main=main_title)



#plotting the community, but with color
color_type = as.integer(V(g.now)$rating)
clrs = brewer.pal(length(unique(color_type)), 'RdYlGn')

plot(g.now, 
     layout = layout_nicely(g.now),
     vertex.color = clrs[as.factor(color_type)],
     main = main_title)

legend('bottom',bty='n',legend = levels(as.factor(color_type)),
       fill=clrs,horiz = TRUE,border = NA, cex = .5)



#adding size based on film age
color_type = as.integer(V(g.now)$rating)
clrs = brewer.pal(length(unique(color_type)), 'RdYlGn')

size_on_age = -(V(g.now)$age - (max(V(g.now)$age) + 5))

plot(g.now, 
     layour = layout_nicely(g.now),
     vertex.color = clrs[as.factor(color_type)],
     vertex.size = size_on_age/6,
     main = main_title)

legend('bottom',bty='n',legend = levels(as.factor(color_type)),
       fill=clrs,horiz = TRUE,border = NA, cex = .5)



#applying formatting to the overall film graph
color_type = as.integer(V(g.films)$rating)
clrs = brewer.pal(length(unique(color_type)), 'RdYlGn')

size_on_age = -(V(g.films)$age - (max(V(g.films)$age) + 2))

plot(g.films, 
     layout = layout_nicely(g.films),
     vertex.color = clrs[as.factor(color_type)],
     vertex.size = size_on_age/10)

legend('bottom',bty='n',legend = levels(as.factor(color_type)),
       fill=clrs,horiz = TRUE,border = NA, cex = .5)
