library(igraph)
rm(list = ls())

gen_class <- graph (edges=c('Amy','Jason',
                     'Amy','Victoria',
                     'Jason','Steph',
                     'Jason','Mary',
                     'Jason','Victoria',
                     'Victoria','Andre',
                     'Victoria','Mary',
                     'Jo','Steph',
                     'Amy','Jo',
                     'Amy','Steph',
                     'Andre','Amy',
                     'Jo','Jason',
                     'Jason','Andre',
                     'Mary','Amy'),
             directed=F)

plot(gen_class, vertex.label.color = 'black', vertex.label.dist = 2, vertex.label.degree = pi/2)

ppl <- c('Amy','Victoria','Andre','Jason','Mary','Jo','Steph')
tbl <- c('Table11','Table11','Table11','Table12','Table12','Table12','Table13')
lunch_df <- data.frame(ppl,tbl)

class_lunch1 <- graph_from_data_frame(lunch_df, directed = FALSE)

V(class_lunch1)$type <- V(class_lunch1)$name %in% lunch_df[,2]


V(class_lunch1)$color <- ifelse(V(class_lunch1)$type,'blue','red')
V(class_lunch1)$shape <- ifelse(V(class_lunch1)$type,'square','circle')


plot(class_lunch1, vertex.label.color = 'black', vertex.label.dist = 2, vertex.label.degree = pi/2)


ppl <- c('Jason','Amy','Mary','Victoria','Andre','Steph','Jo')
tbl <- c('Table21','Table21','Table21','Table22','Table22','Table23','Table23')
lunch_df <- data.frame(ppl,tbl)

class_lunch2 <- graph_from_data_frame(lunch_df, directed = FALSE)

V(class_lunch2)$type <- V(class_lunch2)$name %in% lunch_df[,2]


V(class_lunch2)$color <- ifelse(V(class_lunch2)$type,'blue','red')
V(class_lunch2)$shape <- ifelse(V(class_lunch2)$type,'square','circle')


plot(class_lunch2, vertex.label.color = 'black', vertex.label.dist = 2, vertex.label.degree = pi/2)


ppl <- c('Jason','Amy','Mary','Victoria','Andre','Steph','Jo','Amy','Victoria','Andre','Jason','Mary','Jo','Steph')
tbl <- c('Table11','Table11','Table11','Table12','Table12','Table12','Table13','Table21','Table21','Table21','Table22','Table22','Table23','Table23')

lunch_df <- data.frame(ppl,tbl)

class_lunch <- graph_from_data_frame(lunch_df, directed = FALSE)

V(class_lunch)$type <- V(class_lunch)$name %in% lunch_df[,2]

V(class_lunch)$color <- ifelse(V(class_lunch)$type,'blue','red')
V(class_lunch)$shape <- ifelse(V(class_lunch)$type,'square','circle')

class_lunch <- simplify(class_lunch)
plot(class_lunch, layout = layout_nicely, vertex.size = 6, vertex.label.color = 'black', vertex.label.dist = 1.5, vertex.label.degree = pi/2)

g.bp <- bipartite.projection(class_lunch)

g.people <- (g.bp$proj1)
plot(g.people, vertex.label.color = 'black', vertex.label.dist = 2, vertex.label.degree = pi/2)
