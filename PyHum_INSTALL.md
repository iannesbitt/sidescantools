# How to install PyHum on your Linux box
### A step-by-step guide
*August 12, 2017*

## 1. Install Anaconda

**Note:** When prompted, allow the installer to add the Anaconda bin folder to your PATH variable by inserting a line at the end of your `.bashrc` file.

```
wget http://repo.continuum.io/archive/Anaconda2-4.4.0-Linux-x86_64.sh
bash Anaconda2-4.4.0-Linux-x86_64.sh
```

## 2. Install dependencies
```
conda install nomkl basemap
conda install -c conda-forge basemap-data-hires
pip install numpy==1.11.3
```

## 3. Edit the `_pyhum_correct.py` file
```
cd $HOME/anaconda2/lib/python2.7/site-packages/PyHum/
nano _pyhum_correct.py
```

Comment out lines with the following code:
```
plt.axis('normal'); plt.axis('tight')
```

In my case, these were on lines 829, 848, and 867.
