import numpy as np
from src.data_utils import read_pkl
from scipy import stats
import matplotlib.pyplot as plt
from src.theory_utils import nCr



def plot_erormat(err_gcpc, lambdas, Npatts):
    print(err_gcpc.shape)
    #plt.figure(figsize=(5, 10))
    #plt.figure()
    #plt.imshow(np.mean(err_gcpc[:,:], axis=2), interpolation='nearest', aspect='auto')  #avg error over 100 trials
    #m = np.mean(err_gcpc[:,:], axis=2)
    #plt.plot(m[8])
    plt.imshow(err_gcpc[:,:,0], interpolation='nearest', aspect='auto')
    #plt.plot(err_gcpc[18,:,0]*Npatts)
    plt.colorbar()
    plt.ylabel("number of place cells")
    plt.xlabel("number of patterns")
    plt.title(f"Cleanup Error (single trial), lambdas={lambdas}")
    plt.show()
    exit()


def process_data(filename, results_dir, errthresh=0.03, error="err_gcpc",all_caps=False):
  fname = f"{results_dir}/{filename}" 

  data = read_pkl(fname)
  err_gcpc = data[error]
  Np_lst = data["Np_lst"]
  nruns = data["nruns"]
  Npos = data["Npos"]
  Ng = data["Ng"]
  lambdas = data["lambdas"]
  Npatts_lst=data["Npatts_lst"]

  # Npatts = np.arange(1,Npos+1)
  #plot_erormat(err_gcpc, lambdas, Npatts)
  #exit()
  #err_gcpc = np.mean(err_gcpc, axis=2)

  capacity = -1*np.ones((len(Np_lst), nruns))
  valid = err_gcpc <= errthresh   # bool
  for Np in range(len(Np_lst)):
    # # Original conservative
    for r in range(nruns):
      lst = np.argwhere(valid[Np,:,r] == False)
      #lst = np.argwhere(valid[Np,:] == False)
      if len(lst) == 0:
        #print("full capacity")
        capacity[Np,r] = Npos
      else:      
        bef_err = lst[0]-1
        bef_err = bef_err*(bef_err>0)  #Don't want to return -1 if lst[0]=0
        capacity[Np,r] = Npatts_lst[bef_err]
    
    # # relaxed capacity
    # for r in range(nruns):
    #     lst = np.argwhere(valid[Np,:,r] == True)
    #   # print(valid[Np,:,r] == True)
    #   # print(len(lst))
    #     if len(lst) == 0:
    #         capacity[Np,r] = 0
    #     else: 
    #         capacity[Np,r] = lst[-1] +1   
   #    capacity[Np,r] = lst[-1] 
 
  avg_cap = np.mean(capacity, axis=1)     # mean error over runs
  std_cap = np.std(capacity, axis=1)     # std dev over runs
  #std_cap = stats.sem(capacity, axis=1)   # std error of the mean


  # avg_cap = capacity[:,1]     # individual runs
  # std_cap = 0    # individual runs
  if all_caps:
    return avg_cap, std_cap, Np_lst, Ng, lambdas, capacity
  else:
    return avg_cap, std_cap, Np_lst, Ng, lambdas



