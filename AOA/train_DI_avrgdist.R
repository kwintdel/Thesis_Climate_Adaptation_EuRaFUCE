#' Calculate Dissimilarity Index of training data
#' @description
#' This function estimates the Dissimilarity Index (DI)
#' within the training data set used for a prediction model.
#' Optionally, the local point density can also be calculated.
#' Predictors can be weighted based on the internal
#' variable importance of the machine learning algorithm used for model training.
#' @note
#' This function is called within \code{\link{aoa}} to estimate the DI and AOA of new data.
#' However, it may also be used on its own if only the DI of training data is of interest,
#' or to facilitate a parallelization of \code{\link{aoa}} by avoiding a repeated calculation of the DI within the training data.
#'
#' @param model A train object created with caret used to extract weights from (based on variable importance) as well as cross-validation folds
#' @param train A data.frame containing the data used for model training. Only required when no model is given
#' @param weight A data.frame containing weights for each variable. Only required if no model is given.
#' @param variables character vector of predictor variables. if "all" then all variables
#' of the model are used or if no model is given then of the train dataset.
#' @param CVtest list or vector. Either a list where each element contains the data points used for testing during the cross validation iteration (i.e. held back data).
#' Or a vector that contains the ID of the fold for each training point.
#' Only required if no model is given.
#' @param CVtrain list. Each element contains the data points used for training during the cross validation iteration (i.e. held back data).
#' Only required if no model is given and only required if CVtrain is not the opposite of CVtest (i.e. if a data point is not used for testing, it is used for training).
#' Relevant if some data points are excluded, e.g. when using \code{\link{nndm}}.
#' @param method Character. Method used for distance calculation. Currently euclidean distance (L2) and Mahalanobis distance (MD) are implemented but only L2 is tested. Note that MD takes considerably longer.
#' @param useWeight Logical. Only if a model is given. Weight variables according to importance in the model?
#' @param useCV Logical. Only if a model is given. Use the CV folds to calculate the DI threshold?
#' @param LPD Logical. Indicates whether the local point density should be calculated or not.
#' @param verbose Logical. Print progress or not?
#' @param algorithm see \code{\link[FNN]{knnx.dist}} and \code{\link[FNN]{knnx.index}}
#' @seealso \code{\link{aoa}}
#' @importFrom graphics boxplot
#' @import ggplot2
#'
#' @return A list of class \code{trainDI} containing:
#'  \item{train}{A data frame containing the training data}
#'  \item{weight}{A data frame with weights based on the variable importance.}
#'  \item{variables}{Names of the used variables}
#'  \item{catvars}{Which variables are categorial}
#'  \item{scaleparam}{Scaling parameters. Output from \code{scale}}
#'  \item{trainDist_avrg}{A data frame with the average distance of each training point to every other point}
#'  \item{trainDist_avrgmean}{The mean of trainDist_avrg. Used for normalizing the DI}
#'  \item{trainDI}{Dissimilarity Index of the training data}
#'  \item{threshold}{The DI threshold used for inside/outside AOA}
#'  \item{trainLPD}{LPD of the training data}
#'  \item{avrgLPD}{Average LPD of the training data}
#'
#'
#'
#' @export train_DI
#'
#' @author
#' Hanna Meyer, Marvin Ludwig, Fabian Schumacher
#'
#' @references Meyer, H., Pebesma, E. (2021): Predicting into unknown space?
#' Estimating the area of applicability of spatial prediction models.
#' \doi{10.1111/2041-210X.13650}
#'
#'
#' @examples
#' \dontrun{
#' library(sf)
#' library(terra)
#' library(caret)
#' library(CAST)
#'
#' # prepare sample data:
#' data("splotdata")
#' splotdata = st_drop_geometry(splotdata)
#'
#' # train a model:
#' set.seed(100)
#' model <- caret::train(splotdata[,6:16],
#'                       splotdata$Species_richness,
#'                       importance=TRUE, tuneLength=1, ntree = 15, method = "rf",
#'                       trControl = trainControl(method="cv", number=5, savePredictions=T))
#' # variable importance is used for scaling predictors
#' plot(varImp(model,scale=FALSE))
#'
#' # calculate the DI of the trained model:
#' DI = trainDI(model=model)
#' plot(DI)
#'
#' #...or calculate the DI and LPD of the trained model:
#' # DI = trainDI(model=model, LPD = TRUE)
#'
#' # the DI can now be used to compute the AOA (here with LPD):
#' studyArea = rast(system.file("extdata/predictors_chile.tif", package = "CAST"))
#' AOA = aoa(studyArea, model = model, trainDI = DI, LPD = TRUE, maxLPD = 1)
#' print(AOA)
#' plot(AOA)
#' plot(AOA$AOA)
#' plot(AOA$LPD)
#' }
#'


train_DI <- function(train = NULL,
                    variables = "all",
                    weight = NA,
                    CVtest = NULL,
                    sample_percentage = 0.1
                    ){

  # get parameters if they are not provided in function call----
  model = NA
  CVtrain = NULL
  useCV =TRUE
  verbose = FALSE
  weight <- user_weights(weight, variables)
  
  # Function to log verbose output to debugging.txt
    log_to_file <- function(message) {
      cat(message, file = "test_averagedist.txt", append = TRUE)
    }
    
  if(verbose){
    log_to_file("started trainDI")
  }

  # get CV folds from model or from parameters
  folds <-  aoa_get_folds(model,CVtrain,CVtest,useCV)
  CVtest <- folds[[2]]
  CVtrain <- folds[[1]]
  if(verbose){
    log_to_file(paste("CVtrain: ", CVtrain, "\n"))
    log_to_file(paste("CVtest: ", CVtest, "\n"))
  }


  # check for input errors -----
  if(nrow(train)<=1){stop("at least two training points need to be specified")}

  # reduce train to specified variables
  train <- train[,na.omit(match(variables, names(train)))]
  if(verbose){
    log_to_file(paste("train after selected variables: ", train, "\n"))
  }

  #train_backup <- train

  # convert categorial variables
  catupdate <- aoa_categorial_train(train, variables, weight)

  train <- catupdate$train
  weight <- catupdate$weight

  # scale train
  train <- scale(train)
  if(verbose){
    log_to_file(paste("train_scaled: ", train, "\n"))
  }

  # make sure all variables have variance
  if (any(apply(train, 2, FUN=function(x){all(is.na(x))}))){
    stop("some variables in train seem to have no variance")
  }

  # save scale param for later
  scaleparam <- attributes(train)


  # multiply train data with variable weights (from variable importance)
  if(!inherits(weight, "error")&!is.null(unlist(weight))){
    train <- sapply(1:ncol(train),function(x){train[,x]*unlist(weight[x])})
  }

  if(verbose){
    log_to_file(paste("multiplied by weights: ", train, "\n"))
  }

  # calculate average mean distance between training data

  trainDist_avrg <- c()
  trainDist_min <- c()

    # ------------------------------------------------------------------------------
    # Sample a subset of the data for distance matrix calculation
    set.seed(42)  # For reproducibility
    sample_size <- ceiling(nrow(train) * sample_percentage)
    sample_indices <- sample(seq_len(nrow(train)), size = sample_size, replace = FALSE)
    train_sample <- train[sample_indices, ]
    if(verbose){
      log_to_file(paste("train sample: ", train_sample, "\n"))
    }
    
    # ------------------------------------------------------------------------------
    # === 1. Compute Distance Matrix for the Sampled Data ===
    # Instead of using makeCluster, we use mclapply to run threads on Linux.
    if (verbose) {
      log_to_file(paste("Start distance calculation on", sample_percentage,
                        "portion of the data\n"))
    }
    
    # Compute the full pairwise distance matrix using dist()
    sampleDist <- as.matrix(dist(train_sample))
    if(verbose){
      log_to_file(paste("sampleDist: ", sampleDist, "\n"))
    }

    if(verbose){
      log_to_file(paste("sampleDist complete: ", sampleDist, "\n"))
    } 
    
    
    # Compute the average distance from the sample distance matrix.
    trainDist_avrg <- rowMeans(sampleDist, na.rm = TRUE)
    trainDist_avrgmean <- mean(trainDist_avrg, na.rm = TRUE)
    if (verbose) {
      log_to_file(paste("Calculation of average distances done: ", trainDist_avrgmean, "\n"))
    }
    
    

  aoa_results = list(
    weight = weight,
    variables = variables,
    scaleparam = scaleparam,
    trainDist_avrg = trainDist_avrg,
    trainDist_avrgmean = trainDist_avrgmean,
    sample_percentage = sample_percentage,
    catvars = catupdate$catvars
  )

  class(aoa_results) = "trainDI"

  return(aoa_results)
}


################################################################################
# Helper functions
################################################################################
# Encode categorial variables

aoa_categorial_train <- function(train, variables, weight){
  # Ensure default contrast settings to avoid missing contrast functions
  options(contrasts = c("contr.treatment", "contr.poly"))
  
  # Identify all categorical variables (factors or characters)
  catvars <- tryCatch(names(train)[which(sapply(train[,variables], class) %in% c("factor", "character"))],
                      error = function(e) e)
  
  # Include LC_CORINE as a categorical variable, even though it is numeric
  if("LC_CORINE" %in% names(train) && is.numeric(train$LC_CORINE)) {
    train$LC_CORINE <- factor(train$LC_CORINE, levels = unique(train$LC_CORINE))  # Ensure levels are set
    contrasts(train$LC_CORINE) <- contr.treatment(length(unique(train$LC_CORINE)))  # Explicitly define contrasts
    catvars <- c(catvars, "LC_CORINE")  # Add to categorical variables list
  }
  
  if (!inherits(catvars, "error") & length(catvars) > 0){
    message("Warning: predictors contain categorical variables. The integration is currently still under development. Please check results carefully!")
    
    for (catvar in catvars){
      # Drop unused factor levels in the train dataset
      train[, catvar] <- droplevels(train[, catvar])
      
      # Create dummy variables for the categorical variable with explicitly set contrasts
      dvi_train <- predict(caret::dummyVars(paste0("~", catvar), data = train, fullRank = TRUE), train)
      train <- data.frame(train, dvi_train)
      
      if (!inherits(weight, "error")){
        addweights <- data.frame(t(rep(weight[, which(names(weight) == catvar)], ncol(dvi_train))))
        names(addweights) <- colnames(dvi_train)
        weight <- data.frame(weight, addweights)
      }
    }
    
    if (!inherits(weight, "error")){
      weight <- weight[, -which(names(weight) %in% catvars)]
    }
    train <- train[, -which(names(train) %in% catvars)]
  }
  
  return(list(train = train, weight = weight, catvars = catvars))
}




# check user weight input
# make sure this function outputs a data.frame with
# one row and columns named after the variables

user_weights = function(weight, variables){

  # list input support
  if(inherits(weight, "list")){
    # check if all list entries are in variables
    weight = as.data.frame(weight)
  }


  #check if manually given weights are correct. otherwise ignore (set to 1):
  if(nrow(weight)!=1  || !all(variables %in% names(weight))){
    message("variable weights are not correctly specified and will be ignored. See ?aoa")
    weight <- t(data.frame(rep(1,length(variables))))
    names(weight) <- variables
  }
  weight <- weight[,na.omit(match(variables, names(weight)))]
  if (any(weight<0)){
    weight[weight<0]<-0
    message("negative weights were set to 0")
  }

  return(weight)

}




# Get folds from train object


aoa_get_folds <- function(model, CVtrain, CVtest, useCV){
  ### if folds are to be extracted from the model:
  if (useCV&!is.na(model)[1]){
    if(tolower(model$control$method)!="cv"){
      message("note: Either no model was given or no CV was used for model training. The DI threshold is therefore based on all training data")
    }else{
      CVtest <- model$control$indexOut
      CVtrain <- model$control$index
    }
  }
  ### if folds are specified manually:
  if(is.na(model)[1]){

    if(!is.null(CVtest)&!is.list(CVtest)){ # restructure input if CVtest only contains the fold ID
      tmp <- list()
      for (i in unique(CVtest)){
        tmp[[i+1]] <- which(CVtest==i)
      }
      CVtest <- tmp
    }

    if(is.null(CVtest)&is.null(CVtrain)){
      message("note: No model and no CV folds were given. The DI threshold is therefore based on all training data")
    }else{
      if(is.null(CVtest)){ # if CVtest is not given, then use the opposite of CVtrain
        CVtest <- lapply(CVtrain,function(x){which(!sort(unique(unlist(CVtrain)))%in%x)})
      }else{
        if(is.null(CVtrain)){ # if CVtrain is not given, then use the opposite of CVtest
          CVtrain <- lapply(CVtest,function(x){which(!sort(unique(unlist(CVtest)))%in%x)})
        }
      }
    }

  }
  if(!is.na(model)[1]&useCV==FALSE){
    message("note: useCV is set to FALSE. The DI threshold is therefore based on all training data")
    CVtrain <- NULL
    CVtest <- NULL
  }
  return(list(CVtrain,CVtest))
}


