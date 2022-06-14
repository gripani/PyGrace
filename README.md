Usage:
```python
    from PyGrace.gracereader import GraceReader
    import os.path as osp 
    import matplotlib.pyplot as plt 

    files_dict = { 
        label1 : osp.join('...'),
        label2 : osp.join('...'),
        label3 : osp.join('...')
    }

    for label, xvg_path in files_dict.items():
        grace = GraceReader(xvg_path, label)
        grace.read()
        grace.clean()
        grace.plot()
    
    plt.legend(loc='upper left', bbox_to_anchor=(1.01, 1.))
    plt.tight_layout()
    plt.show()
```
