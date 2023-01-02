import pandas as pd
import numpy as np
import globals as gb
import os
class Predictor:
    def __init__(self):
        self.static = True
        print(os.path.abspath(__file__))
        print(gb.DATASET_PATH)
    def init_dataset(self):
        if self.static:
            url = "C:\\_Workspace\\Kaire\\python\\ds\\training_ds.csv"
            # load dataset into Pandas DataFrame
            self.df = pd.read_csv(url, names=['id','stress','location_id','activity','timestamp','duration','day','hour','hr','rmssd','sdrr','stressor_id','shared_time','classification','env_cond','cond'],skiprows=1)
        else:
            from mysqlDb import mysqlConn
            conn = mysqlConn()
            self.df = pd.read_sql('SELECT id,stress,location_id,activity,timestamp,duration,day,hour,hr,rmssd,sdrr,stressor_id,shared_time,env_cond,classification,cond FROM context_history', conn)
        # Separating out the features and target
        #self.features = ['location_id','activity','duration','day','hour','hr','rmssd','sdrr','stressor_id','shared_time','env_cond']
        self.features = ['stress','location_id','activity','duration','day','hour','stressor_id','shared_time','env_cond']
        self.x = self.df.loc[:, self.features].values
        self.y = self.df.loc[:,['classification']].values
 

    def init_dataset_prediction(self):
        if self.static:
            url = "C:\\_Workspace\\Kaire\\python\\ds\\prediction_ds.csv"
            # load dataset into Pandas DataFrame
            self.df = pd.read_csv(url, names=['id','stress','location_id','activity','day','hour','stressor_id','env_cond','shared_time'],skiprows=1)
        else:
            from mysqlDb import mysqlConn
            conn = mysqlConn()
            self.df = pd.read_sql('SELECT * FROM history', conn)
        # Separating out the features and target
        #self.features = ['stress','locationId','activity','duration','day','hour','hrv_mean','hrv_sd','stressorId','shared_time','env_cond']
        self.features = ['location_id','activity','duration','day','hour','stressor_id','shared_time','env_cond']
        self.x = self.df.loc[:, self.features].values
        self.y = self.df.loc[:,['classification']].values 

    def standardize(self):
        # Standardizing the features
        from sklearn.preprocessing import StandardScaler
        self.x = StandardScaler().fit_transform(self.x)

    def reduce_dimension(self):
        from sklearn.decomposition import PCA
        pca = PCA(n_components=1)
        #principalComponents = pca.fit_transform(self.x)
        #self.x = pd.DataFrame(data = principalComponents
        #             , columns = ['principal component 1', 'principal component 2'])

        #self.finalDf = pd.concat([self.x, self.df[['classification']]], axis = 1)
        #from sklearn.model_selection import train_test_split
        #self.x_trainrd, self.x_testrd, self.y_trainrd, self.y_testrd = train_test_split(self.x, self.y, test_size=0.3, shuffle = False, stratify = None) # if size = 0.3, 70% training and 30% test
        #pca = PCA(n_components=6)
        #principalComponents = pca.fit_transform(self.x)
        #self.x = pd.DataFrame(data = principalComponents
         #            , columns = ['principal component 1', 'principal component 2','principal component 3', 'principal component 4','principal component 5', 'principal component 6'])
        
        featuresa = ['duration','day','hour','shared_time']
        a = self.df.loc[:, featuresa].values
        featuresb = ['location_id','activity','stressor_id','env_cond']
        b = self.df.loc[:, featuresb].values
        principalComponents = pca.fit_transform(a)
        a = pd.DataFrame(data = principalComponents, columns = ['principal component 1'])
        principalComponents = pca.fit_transform(b)
        b = pd.DataFrame(data = principalComponents, columns = ['principal component 2'])        
        self.x = pd.concat([a, b], axis = 1)
        #d = pca.fit_transform(c)
        #self.x = pd.DataFrame(data = d, columns = ['principal component 1', 'principal component 2'])
        #self.x = pd.concat([e, self.df[['classification']]], axis = 1)
        #print(self.x)

    def split_dataset(self,size):
        #training dataset
        from sklearn.model_selection import train_test_split
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.x, self.y, test_size=size, shuffle = False, stratify = None) # if size = 0.3, 70% training and 30% test
        #print("##########","Training dataset has ",self.x_train.shape," rows and evaluation dataset has ", self.x_test.shape, "##########")

    def svm_predict(self):
        #SVM
        from sklearn import svm
        print(self.x_train)
        classifier = svm.SVC(kernel='rbf', probability=True) # RBF Kernel
        classifier.fit(self.x_train, self.y_train)
        self.y_pred_svm = classifier.predict(self.x_test)
        self.y_prob_svm = classifier.predict_proba(self.x_test)

    def loocv_predict(self):
        #SVM
        print(self.x.shape[0])
        print(self.y.shape)
        from sklearn import svm
        #print(self.x_train)
        classifier = svm.SVC(kernel='rbf', probability=True) # RBF Kernel
        #self.y_pred_svm = classifier.predict(self.x_test)
        #self.y_prob_svm = classifier.predict_proba(self.x_test)
        from sklearn.model_selection import LeaveOneOut
        from sklearn import model_selection
        loocv = LeaveOneOut()
        # enumerate splits
        y_true, y_pred = list(), list()
        print(self.y.ravel())
        print(self.x)        
        z = model_selection.cross_val_score(classifier, self.x, self.y.ravel(), cv=(self.x.shape[0]-50))
        print(z.shape)
        print(z)
        
        from sklearn import metrics
        print("\n##############\n")
        print("Metrics for SVM")
        print("Metrics")
        print("Accuracy:",round(metrics.accuracy_score(y_true, y_pred),4))
        print("Precision:",round(metrics.precision_score(y_true, y_pred,zero_division=0),4))
        print("Recall:",round(metrics.recall_score(y_true, y_pred),4))
        print("F1:",round(metrics.f1_score(y_true, y_pred,zero_division=0),4))
    
    def rf_predict(self):
        #RF
        from sklearn.ensemble import RandomForestClassifier
        classifier = RandomForestClassifier(max_depth=4, random_state=0) # RBF Kernel
        y = self.y_train.reshape(-1, 1)
        
        np.ravel(self.y_train)
        classifier.fit(self.x_train, self.y_train.ravel())
        self.y_pred_rf = classifier.predict(self.x_test)
        self.y_prob_rf = classifier.predict_proba(self.x_test)

    def show_metrics(self, ):
        #Metrics
        from sklearn import metrics
        print("\n##############\n")
        print("Metrics for SVM")
        print("Metrics")
        print("Accuracy:",round(metrics.accuracy_score(self.y_test, self.y_pred_svm),4))
        print("Precision:",round(metrics.precision_score(self.y_test, self.y_pred_svm,zero_division=0),4))
        print("Recall:",round(metrics.recall_score(self.y_test, self.y_pred_svm),4))
        print("F1:",round(metrics.f1_score(self.y_test, self.y_pred_svm,zero_division=0),4))
        print("\n##############\n")
        print("Metrics for RF")
        print("Metrics")
        print("Accuracy:",round(metrics.accuracy_score(self.y_test, self.y_pred_rf),4))
        print("Precision:",round(metrics.precision_score(self.y_test, self.y_pred_rf,zero_division=0),4))
        print("Recall:",round(metrics.recall_score(self.y_test, self.y_pred_rf),4))
        print("F1:",round(metrics.f1_score(self.y_test, self.y_pred_rf,zero_division=0),4))
        print("\n##############\n")


    def show_graph_std(self):
        import matplotlib.pyplot as plt

        fig = plt.figure(figsize = (8,8))
        ax = fig.add_subplot(1,1,1) 
        ax.set_xlabel('PC1', fontsize = 15)
        ax.set_ylabel('PC2', fontsize = 15)
        ax.set_title('Standardized', fontsize = 20)
        targets = [0, 1]
        colors = ['g', 'r']
        for target, color in zip(targets,colors):
            indicesToKeep = self.finalDf['classification'] == target
            ax.scatter(self.finalDf.loc[indicesToKeep, 'principal component 1']
                       , self.finalDf.loc[indicesToKeep, 'principal component 2']
                       , c = color
                       , s = 50)
        ax.legend(targets)
        ax.grid()
        plt.savefig("img/scatter_sdt.png")
        plt.show()

    def show_graph_nonstd(self):
        from graph import scatter

        img = scatter('Non-Standardized', 'PC1', 'PC2')
        img.build(self.finalDf, 'principal component 1', 'principal component 2','classification')
        img.save("scatter_nonsdt")
        #mg.show()

    def show_probability(self):
        prob = pd.DataFrame(self.y_prob_svm,columns=['probA','probability_svm'])
        del prob["probA"]
        prob_rf = pd.DataFrame(self.y_prob_rf,columns=['probB','probability_rf'])
        del prob_rf["probB"]
        prob['probability_svm'] = prob['probability_svm'].apply(lambda x: round(x*100,2))
        prob_rf = prob_rf.apply(lambda y: round(y*100,2))
        result = pd.concat([self.df.tail(prob.size).reset_index(drop=True),prob], axis=1)
        result = pd.concat([result,prob_rf], axis=1)
        result.to_csv(gb.DATASET_PATH+"result_ds.csv", index=False)
        print(result)

    def show_confusion_matrix(self):
        import matplotlib.pyplot as plt
        from sklearn import metrics

        confusion_matrix = metrics.confusion_matrix(self.y_test, self.y_pred_svm)
        cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, display_labels = [False, True])
        cm_display.plot()
        cm_display.ax_.set_title("Confusion Matrix for SVM")
        plt.savefig("img/confusion_matrix_svm.png")
        plt.show()
        
        confusion_matrix = metrics.confusion_matrix(self.y_test, self.y_pred_rf)
        cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, display_labels = ["non-stressor", "stressor"])
        cm_display.plot()
        cm_display.ax_.set_title("Confusion Matrix for RF")
        plt.savefig("img/confusion_matrix_rf.png")
        plt.show()
        
    def line_graph (self):
        import matplotlib.pyplot as plt
        import numpy as np
        
        url = "C:\\_Workspace\\Kaire\\python\\ds\\linegraph.csv"
        # load dataset into Pandas DataFrame
        self.df = pd.read_csv(url, names=['id','stress','locationId','activity','timestamp','duration','day','hour','hrv_mean','hrv_sd','stressorId','shared_time','env_cond','classification','cond'],skiprows=1)
        self.features = ['duration','hrv_mean','hrv_sd','shared_time']
        self.y = self.df.loc[:, self.features].values
        self.x = self.df.loc[:, ['timestamp']].values          
        # plot lines
        plt.plot(self.x, self.y, label = ['duration','hrv','sdnn','shared_time'])
        plt.legend()
        plt.savefig("img/line_nonstd.png")
        plt.show()
        from sklearn.preprocessing import StandardScaler
        self.y = StandardScaler().fit_transform(self.y)
        plt.plot(self.x, self.y, label = ['duration','hrv','sdnn','shared_time'])
        plt.legend()
        plt.savefig("img/line_std.png")
        plt.show()
        
    def line_graph_feat (self):
        import matplotlib.pyplot as plt
        import numpy as np
        url = "C:\\_Workspace\\Kaire\\python\\ds\\line_ds.csv"
        # load dataset into Pandas DataFrame
        self.df = pd.read_csv(url, names=['id','stress','timestamp','hr','rmssd','sdrr','rr'],skiprows=1)
        self.features = ['stress','hr','rmssd','sdrr','rr']
        self.y = self.df.loc[:, self.features].values
        self.x = self.df.loc[:, ['timestamp']].values
        plt.plot(self.x, self.y, label = ['stress','hr','rmssd','sdrr','rr'])
        plt.legend()
        plt.show()
        from sklearn.preprocessing import StandardScaler
        self.y = StandardScaler().fit_transform(self.y)
        plt.plot(self.x, self.y, label = ['stress','hr','rmssd','sdrr','rr'])
        plt.legend()
        plt.show()
       