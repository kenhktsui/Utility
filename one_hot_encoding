# data1 being the input; newdata being the output

e <- new.env()
for (i in 2:dim(data1)[2]) 
{
if(nlevels(data1[,i])==1)
{print("Only 1 level")}
else if(nlevels(data1[,i])==2)
{
datacol1 <- c()
for (j in 1:dim(data1)[1])
{
if (data1[j,i]==levels(data1[,i])[1]) {datacol1[j]=1} else {datacol1[j]=0}
}
assign(paste("dummy",names(data1)[i], sep = ""),datacol1,env = e)
rm(datacol1)
}
else
{
ncat <- nlevels(data1[,i])
datacol2 <- matrix(0,ncol=ncat,nrow=dim(data1)[1])
x <- matrix(0,ncol=1,nrow=dim(data1)[1])
x <- data1[,i]
levels(x)<- 1:ncat
for (j in 1:dim(data1)[1])
{
datacol2[j,x[j]]=1
}
datacol2 <- datacol2[,-1] #remove first column to avoid multicolinearity
assign(paste("dummy",names(data1)[i], sep = ""),datacol2,env = e)
rm(datacol2)
rm(x)
}
}

length(ls(env = e)[grep("dummy", ls(env = e))])
listtostack <- ls(env = e)[grep("dummy", ls(env = e))]
X <- do.call(cbind.data.frame, mget(listtostack,envir= e))
Y <- data1[,1]

newdata<-cbind(Y,X)

